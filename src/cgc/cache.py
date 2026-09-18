"""CGC POSIX private-directory cache, atomic publication and lifetime writer lock."""
from contextlib import contextmanager
import json
import os
from pathlib import Path
import stat
import uuid

from .engine import StateError, validate_state
from .quota import _decode, QuotaError

# Two bounded observations/evaluations retain diagnostics and last-known-good evidence.
MAX_CACHE_BYTES = 262144


class CacheError(StateError):
    pass


def _safe_file(fd):
    s = os.fstat(fd)
    if not stat.S_ISREG(s.st_mode) or s.st_uid != os.geteuid() or s.st_nlink != 1 or s.st_mode & 0o077:
        raise CacheError('UNSAFE_CACHE')


class Cache:
    """All I/O anchored to a no-follow directory descriptor; fixed basenames only."""
    def __init__(self, directory, *, create=False):
        self.directory = Path(directory)
        self.create = create
        self.fd = None
        self.lock_fd = None

    def __enter__(self):
        if os.name != 'posix':
            raise CacheError('UNSUPPORTED_PLATFORM')
        path = self.directory.absolute()
        if '..' in path.parts:
            raise CacheError('UNSAFE_CACHE')
        fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
        try:
            for i, part in enumerate(path.parts[1:]):
                final = i == len(path.parts) - 2
                if final and self.create:
                    try:
                        os.mkdir(part, 0o700, dir_fd=fd)
                    except FileExistsError:
                        pass
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = child
            s = os.fstat(fd)
            if s.st_uid != os.geteuid() or s.st_mode & 0o077:
                raise CacheError('UNSAFE_CACHE')
            self.fd = fd
            return self
        except (OSError, StateError):
            os.close(fd)
            raise CacheError('UNSAFE_CACHE') from None

    def __exit__(self, *args):
        if self.lock_fd is not None:
            os.close(self.lock_fd)
            self.lock_fd = None
        os.close(self.fd)
        self.fd = None

    @contextmanager
    def writer(self):
        import fcntl
        if self.lock_fd is not None:
            raise CacheError('WRITER_BUSY')
        fd = None
        try:
            fd = os.open('writer.lock', os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600, dir_fd=self.fd)
            _safe_file(fd)
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, StateError):
            if fd is not None:
                os.close(fd)
            raise CacheError('WRITER_BUSY') from None
        self.lock_fd = fd
        try:
            yield
        finally:
            self.lock_fd = None
            os.close(fd)  # Persistent lock inode; kernel releases lock on crash.

    def read(self):
        fd = None
        try:
            fd = os.open('state.json', os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=self.fd)
            _safe_file(fd)
            with os.fdopen(fd, 'rb') as stream:
                fd = None
                data = stream.read(MAX_CACHE_BYTES + 1)
            if len(data) > MAX_CACHE_BYTES:
                raise CacheError('CORRUPT_CACHE')
            return validate_state(_decode(data))
        except FileNotFoundError:
            return None
        except (OSError, StateError, QuotaError, RecursionError):
            raise CacheError('CORRUPT_CACHE') from None
        finally:
            if fd is not None:
                os.close(fd)

    def write(self, state):
        if self.lock_fd is None:
            raise CacheError('WRITER_REQUIRED')
        validate_state(state)
        data = (json.dumps(state, sort_keys=True, allow_nan=False) + '\n').encode()
        if len(data) > MAX_CACHE_BYTES:
            raise CacheError('CACHE_SIZE_LIMIT')
        name = '.state-' + uuid.uuid4().hex + '.tmp'
        fd = None
        try:
            # Refuse existing symlink, hardlink, corrupt or unsafe target.
            self.read()
            fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=self.fd)
            with os.fdopen(fd, 'wb') as stream:
                fd = None
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, 'state.json', src_dir_fd=self.fd, dst_dir_fd=self.fd)
            os.fsync(self.fd)
        except OSError:
            raise CacheError('CACHE_WRITE_FAILED') from None
        finally:
            if fd is not None:
                os.close(fd)
            try:
                os.unlink(name, dir_fd=self.fd)
            except FileNotFoundError:
                pass
