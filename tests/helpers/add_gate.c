/* Test-only rendezvous around Git's real index rename. Never linked into CGC. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void gate(void)
{
    const char *ready = getenv("CGC_FIXTURE_READY");
    const char *release = getenv("CGC_FIXTURE_GATE");
    char message[128], token;
    int fd = open(ready, O_WRONLY);
    if (fd < 0) _exit(120);
    int size = snprintf(message, sizeof(message), "{\"git\":%ld,\"group\":%ld}\n",
                        (long)getpid(), (long)getpgrp());
    if (write(fd, message, size) != size || close(fd)) _exit(121);
    fd = open(release, O_RDONLY);
    if (fd < 0 || read(fd, &token, 1) != 1 || token != 'G') _exit(122);
    close(fd);
}

int rename(const char *old, const char *new)
{
    int (*real_rename)(const char *, const char *) = dlsym(RTLD_NEXT, "rename");
    if (!real_rename) _exit(123);
    const char *index = getenv("CGC_FIXTURE_INDEX");
    const char *stage = getenv("CGC_FIXTURE_STAGE");
    int match = index && stage && !strcmp(new, index)
        && strlen(old) == strlen(index) + 5
        && !strncmp(old, index, strlen(index)) && !strcmp(old + strlen(index), ".lock");
    if (match && !strcmp(stage, "before")) gate();
    int result = real_rename(old, new);
    int saved_errno = errno;
    if (match && !strcmp(stage, "after") && result == 0) gate();
    errno = saved_errno;
    return result;
}
