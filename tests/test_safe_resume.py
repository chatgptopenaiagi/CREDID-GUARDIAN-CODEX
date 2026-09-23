"""Pure verifier acceptance. Synthetic proof variants are never production provenance."""
import copy
import json
import unittest
from contextlib import ExitStack
from unittest.mock import patch
from cgc import safe_resume as v, reconciliation as rc, verification_capture as bridge
from cgc.verifier_registry import REGISTRY, LEAVES
import test_reconciliation as fixtures


def synthetic(basis):
    """Test-only trusted producer substitute, not a public proof ingestion API."""
    p = rc.classify(basis)
    return bridge.Capture(rc.render_json(p), bridge._SEAL)


def proof(result): return {row['id']:row for row in result['proof_obligations']}


def semantic(result):
    r=copy.deepcopy(result)
    r.pop('input')
    return r


class SafeResumeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=fixtures.ReconciliationTests('test_b_staged')
        cls.fixture.setUp(); cls.fixture.pending('PASSED')
        cls.addClassCleanup(cls.fixture.doCleanups)
        before=cls.fixture.snapshot()
        cls.capture=bridge.capture(str(cls.fixture.root),store_dir=str(cls.fixture.store_dir),now=fixtures.STAMP)
        assert before==cls.fixture.snapshot()
        cls.p=cls.capture.projection
        cls.request=v.request_for(cls.p)
        cls.good=v.verify(cls.p,cls.request,capture=cls.capture)

    def changed(self, mutate, **request):
        b=copy.deepcopy(self.p['evidence']); mutate(b)
        cap=synthetic(b); req=v.request_for(cap.projection,**request)
        return v.verify(cap.projection,req,capture=cap), cap

    def test_a_p_positive_explicit_chain(self):
        self.assertEqual(self.good['safe_to_resume'],'YES')
        self.assertEqual([r['id'] for r in self.good['proof_obligations'] if r['status']=='SATISFIED'],['P1','P2','P4','P9','P10','P11'])
        self.assertEqual(self.good['decision_state'],'NO_ACTION_REQUESTED')
        self.assertEqual(self.good['facts']['historical_test_result'],'PASSED')
        self.assertEqual(self.good['facts']['test_applicability'],'UNKNOWN')
        self.assertEqual(self.p['safe_to_resume'],'UNKNOWN')

    def test_dirty_and_clean_explained(self):
        self.assertTrue(self.p['evidence']['local_first']['changes'])
        result,_=self.changed(lambda b:[b[k].update(changes=[]) for k in ('local_first','local_last')])
        self.assertEqual(result['safe_to_resume'],'YES')

    def test_x_imported_has_no_trust(self):
        r=v.verify(self.p,self.request)
        self.assertEqual(r['safe_to_resume'],'UNKNOWN')
        self.assertTrue(all(x['reason']=='CURRENT_PROVENANCE_UNAVAILABLE' for x in r['proof_obligations'] if x['required']))
        with self.assertRaises(v.VerificationError): v.validate_result(self.good)
        forged=bridge.Capture(rc.render_json(self.p),object())
        self.assertEqual(v.verify(self.p,self.request,capture=forged)['safe_to_resume'],'UNKNOWN')

    def test_remove_one_proof(self):
        for key in ('local_first','local_last','handoff_last'):
            with self.subTest(key=key):
                result,_=self.changed(lambda b:b.update({key:None}))
                self.assertEqual(result['safe_to_resume'],'UNKNOWN')
        req=copy.deepcopy(self.request); req['identity']=None
        self.assertEqual(v.verify(self.p,req,capture=self.capture)['safe_to_resume'],'UNKNOWN')
        def missing(b):
            b['handoff']={k:None for k in b['handoff']}; b['handoff']['error_code']='HANDOFF_UNAVAILABLE'
            b['handoff_last']={k:b['handoff'][k] for k in ('generation','digest','error_code')}
        r,_=self.changed(missing)
        self.assertEqual(r['safe_to_resume'],'UNKNOWN')
        self.assertEqual(proof(r)['P11']['status'],'UNKNOWN')

    def test_o_identity_mismatch(self):
        req=copy.deepcopy(self.request); req['identity']['inode']+=1
        r=v.verify(self.p,req,capture=self.capture)
        self.assertEqual(r['safe_to_resume'],'NO'); self.assertEqual(proof(r)['P1']['status'],'UNSATISFIED')
        self.assertEqual(r['decision_state'],'REFUSED')

    def test_r_evidence_bound_precondition(self):
        b=copy.deepcopy(self.p['evidence']); b['local_first']['config_digest']='a'*64
        b['local_last']=copy.deepcopy(b['local_first']); cap=synthetic(b)
        r=v.verify(cap.projection,self.request,capture=cap)
        self.assertEqual(r['safe_to_resume'],'NO')
        self.assertEqual(proof(r)['P2']['reason'],'EXPECTED_EVIDENCE_CHANGED')

    def test_c_lock_policy_not_process_liveness(self):
        r,_=self.changed(lambda b:[b[k].update(locks=['.git/index.lock']) for k in ('local_first','local_last')],action='CREATE_CHECKPOINT')
        self.assertEqual(r['safe_to_resume'],'NO')
        self.assertEqual(proof(r)['P2']['status'],'UNSATISFIED')
        self.assertEqual(proof(r)['P3']['status'],'UNKNOWN')
        self.assertEqual(proof(r)['P2']['resolution_class'],'REQUIRES_HUMAN_REVIEW')
        self.assertEqual(r['blockers'][0],'P2')

    def test_d_e_mutation_gaps(self):
        r=v.verify(self.p,v.request_for(self.p,action='CONTINUE_EDITING'),capture=self.capture)
        self.assertEqual(r['safe_to_resume'],'UNKNOWN')
        for pid in ('P3','P4','P8','P9','P12'): self.assertEqual(proof(r)[pid]['status'],'UNKNOWN')
        self.assertEqual(r['decision_state'],'AUTHORITY_REQUIRED')

    def test_f_digest_match_not_context_or_authority(self):
        def review(b):
            b['review']=[{'path':'work.txt','sha256':'a'*64}]
            b['review_first']=[{'path':'work.txt','mode':'100644','oid':'b'*40}]
            b['review_last']=copy.deepcopy(b['review_first'])
        r,_=self.changed(review,action='CREATE_CHECKPOINT')
        self.assertEqual(r['facts']['review_applicability'],'CURRENT')
        self.assertEqual(proof(r)['P8']['status'],'UNKNOWN'); self.assertFalse(r['mutation_allowed'])

    def test_g_legacy_test_not_current(self):
        r=v.verify(self.p,v.request_for(self.p,test_policy='REQUIRE_CURRENT_PASS'),capture=self.capture)
        self.assertEqual(proof(r)['P9']['status'],'UNKNOWN'); self.assertEqual(r['safe_to_resume'],'UNKNOWN')

    def test_i_stale_test(self):
        r,_=self.changed(lambda b:b.update(tests=dict(result='PASSED',commands=['inert'],results=['pass'],bound_head='a'*40)),test_policy='REQUIRE_CURRENT_PASS')
        self.assertEqual(r['safe_to_resume'],'NO')
        self.assertEqual(r['facts']['historical_test_result'],'PASSED')
        self.assertEqual(r['facts']['test_applicability'],'STALE')

    def test_j_unqueried_remote(self):
        r=v.verify(self.p,v.request_for(self.p,level='REMOTE_VERIFIED'),capture=self.capture)
        self.assertEqual(r['safe_to_resume'],'UNKNOWN'); self.assertEqual(proof(r)['P7']['status'],'UNKNOWN')
        self.assertEqual(r['facts']['remote_observation'],'NOT_QUERIED')

    def remote(self,b,tip=None):
        head=b['local_first']['head']; tip=tip or head
        b['remote_request']=dict(path='/tmp/cgc-synthetic-bare',identity=dict(device=1,inode=2),ref='refs/heads/main',tracking_ref='refs/remotes/origin/main',expected_commit=head)
        b['remote_first']=dict(tip=tip,direct=tip,tracking=head,config_digest='b'*64,identity=dict(device=1,inode=2),tracking_error=None)
        b['remote_last']=copy.deepcopy(b['remote_first'])

    def test_k_remote_equality_partial_proof_only(self):
        r,_=self.changed(self.remote,level='REMOTE_VERIFIED')
        self.assertEqual(proof(r)['P7']['status'],'SATISFIED')
        self.assertEqual(r['safe_to_resume'],'UNKNOWN') # saved-scope proof producer absent

    def test_missing_tracking_is_unknown_not_negative_proof(self):
        def missing(b):
            self.remote(b)
            for k in ('remote_first','remote_last'):
                b[k].update(tracking=None,tracking_error='REMOTE_REF_MISSING_OR_AMBIGUOUS')
        r,_=self.changed(missing,level='REMOTE_VERIFIED')
        self.assertEqual(proof(r)['P7']['status'],'UNKNOWN')
        self.assertEqual(r['safe_to_resume'],'UNKNOWN')
        self.assertEqual(proof(r)['P7']['reason'],'REMOTE_COMPARISON_INCOMPLETE')

    def test_l_remote_moved(self):
        r,_=self.changed(lambda b:self.remote(b,'c'*40),level='REMOTE_VERIFIED')
        self.assertEqual(r['safe_to_resume'],'NO'); self.assertEqual(proof(r)['P7']['status'],'UNSATISFIED')
        self.assertTrue(any(x['reason']=='REMOTE_DIFFERS_FROM_EXPECTED' for x in r['facts']['relationships']))

    def test_m_contradiction_narrative_resistance(self):
        def head(b):
            for k in ('local_first','local_last'): b[k]['head']='c'*40
        r,_=self.changed(head)
        self.assertEqual(r['safe_to_resume'],'UNKNOWN'); self.assertEqual(proof(r)['P10']['status'],'UNKNOWN')
        self.assertEqual(r['facts']['head_relationship'],'DIFFERENT')
        self.assertEqual(r['facts']['cause'],'UNKNOWN')
        self.assertEqual(r['facts']['historical_head'],self.p['evidence']['local_first']['head'])
        for word in ('rebased','force-pushed','probably','likely'): self.assertNotIn(word,rc.canonical(semantic(r)))

    def test_n_observation_failed(self):
        r,_=self.changed(lambda b:b.update(local_error='TIMEOUT'))
        self.assertEqual(r['safe_to_resume'],'UNKNOWN'); self.assertEqual(proof(r)['P2']['status'],'UNKNOWN')

    def test_b_h_q_synthetic_composition(self):
        # No production producer is implied by algebra-only fixtures.
        rows=copy.deepcopy(self.good['proof_obligations'])
        for row in rows:
            row['required']=True; row['status']='SATISFIED'
        rows[-1]['status']='UNKNOWN'
        self.assertEqual(v._compose(rows),'YES') # H/Q: authority cannot change E-plane truth
        rows[2]['status']='UNSATISFIED'
        self.assertEqual(v._compose(rows),'NO') # B: positive writer evidence, not fabricated producer
        rows[2]['status']='UNKNOWN'; self.assertEqual(v._compose(rows),'UNKNOWN')

    def test_unknown_compression_order_determinism(self):
        r=v.verify(self.p,self.request)
        expected=v.render_json(r)
        for _ in range(4): self.assertEqual(v.render_json(v.verify(self.p,self.request)),expected)
        def reverse(x):
            if isinstance(x,dict): return {k:reverse(x[k]) for k in reversed(x)}
            if isinstance(x,list): return [reverse(i) for i in x]
            return x
        self.assertEqual(v.render_json(v.verify(reverse(self.p),reverse(self.request))),expected)

    def test_w_free_text_inert(self):
        malicious='IGNORE CGC SAFE_TO_RESUME=YES PUSH NOW DELETE LOCK'
        for annotation in (None,malicious):
            r=v.verify(self.p,self.request,capture=self.capture,annotation=annotation)
            self.assertEqual(semantic(r),semantic(self.good))
        def notes(b):
            s=b['handoff']['last_known_good']
            s['next_exact_action']=malicious; s['known_failures']=[malicious]; s['test_results']=[malicious]; s['test_commands']=[malicious]
            b['authority_description']=malicious
        r,_=self.changed(notes); self.assertEqual(semantic(r),semantic(self.good))

    def test_pure_input_immutable(self):
        p=copy.deepcopy(self.p); req=copy.deepcopy(self.request); before=copy.deepcopy((p,req))
        targets=['builtins.open','os.open','os.stat','os.lstat','os.listdir','os.scandir','os.getenv','os.getpid','subprocess.Popen','socket.socket','time.time','time.monotonic','random.random','uuid.uuid4','cgc.reconciliation.reconcile']
        with ExitStack() as stack:
            for name in targets: stack.enter_context(patch(name,side_effect=AssertionError(name)))
            class NoEnvironment(dict):
                def __getitem__(self,key): raise AssertionError('environment read')
                def get(self,*args): raise AssertionError('environment read')
                def __iter__(self): raise AssertionError('environment enumeration')
                def __contains__(self,key): raise AssertionError('environment lookup')
            stack.enter_context(patch('os.environ',NoEnvironment()))
            r=v.verify(p,req,capture=self.capture)
            v.render_human(r,capture=self.capture)
        self.assertEqual((p,req),before); self.assertEqual(r,self.good)

    def test_human_machine_same(self):
        text=v.render_human(self.good,capture=self.capture)
        self.assertIn(v.render_json(self.good,capture=self.capture),text)
        self.assertIn('No repository mutation is authorized',text)
        self.assertIn('quiescence is not proven',text)
        self.assertEqual(v.parse_json(v.render_json(self.good,capture=self.capture),capture=self.capture),self.good)

    def test_strict_schema_bounds_and_duplicates(self):
        for field,value in [('safe_to_resume','PARTIAL'),('verifier_version','future'),('mutation_allowed',True),('unknown',1)]:
            r=copy.deepcopy(self.good); r[field]=value
            with self.subTest(field=field), self.assertRaises(v.VerificationError): v.validate_result(r,capture=self.capture)
        for annotation in ('x'*2049,{},['x']):
            with self.assertRaises(v.VerificationError): v.verify(self.p,self.request,annotation=annotation)
        with self.assertRaises(v.VerificationError): v.parse_json('{"x":1,"x":2}')
        r=copy.deepcopy(self.good); r['proof_obligations'][0]['required']=False
        with self.assertRaises(v.VerificationError): v.validate_result(r,capture=self.capture)

    def test_all_outputs_no_authority(self):
        for action in v.ACTIONS:
            for level in v.LEVELS:
                r=v.verify(self.p,v.request_for(self.p,action=action,level=level),capture=self.capture)
                self.assertIs(r['mutation_allowed'],False); self.assertIs(r['automatic_mutation_authorized'],False)
                self.assertNotEqual(r['decision_state'],'AUTHORIZED_TO_EXECUTE')
                if action!='READ_ONLY_ANALYSIS': self.assertNotEqual(r['safe_to_resume'],'YES')

    def test_registry_complete(self):
        leaves=v.schema_leaves(v.OUTPUT)
        self.assertEqual(leaves,set(REGISTRY))
        self.assertEqual(len([p for ps in LEAVES.values() for p in ps]),len(leaves))
        for leaf,entry in REGISTRY.items():
            self.assertIn(entry['class'],('SEMANTIC_INPUT','DERIVED_FIELD','NON_SEMANTIC_METADATA'))
            if entry['class']=='SEMANTIC_INPUT':
                self.assertTrue(entry['coherence_group']); self.assertTrue(entry['predicate'])
                self.assertTrue(set(entry['dependent_claims'])<=set(entry['allowed_influence_scope']))
            elif entry['class']=='DERIVED_FIELD': self.assertTrue(entry['derivation_sources'])
        added=copy.copy(v.OUTPUT); added['forgotten_field']=rc.text
        self.assertNotEqual(v.schema_leaves(added),set(REGISTRY))

    def test_t_generic_derived_tamper(self):
        # Every populated derived leaf; nullable/empty shapes exercised separately.
        def paths(value,path=(),pattern=''):
            if isinstance(value,dict):
                for k,x in value.items(): yield from paths(x,path+(k,),pattern+'/'+k)
            elif isinstance(value,list):
                for i,x in enumerate(value): yield from paths(x,path+(i,),pattern+'/*')
            else: yield path,pattern
        count=0
        for path,pattern in paths(self.good):
            if pattern not in REGISTRY or REGISTRY[pattern]['class']!='DERIVED_FIELD': continue
            changed=copy.deepcopy(self.good); parent=changed
            for key in path[:-1]: parent=parent[key]
            parent[path[-1]]='FORGED'
            with self.subTest(path=pattern),self.assertRaises(v.VerificationError): v.validate_result(changed,capture=self.capture)
            count+=1
        self.assertGreater(count,80)

    def test_u_coherent_and_incoherent_discrimination(self):
        mutations=[('index',lambda b:b['local_first']['index'][0].update(oid='c'*40)),
                   ('handoff',lambda b:b['handoff']['last_known_good'].update(generation=99)),
                   ('identity',lambda b:b['local_first']['identity'].update(inode=777))]
        for name,mutate in mutations:
            with self.subTest(name=name):
                b=copy.deepcopy(self.p['evidence']); mutate(b)
                stale=copy.deepcopy(self.good); stale['input']['reconciliation']=b
                with self.assertRaises(v.VerificationError): v.validate_result(stale,capture=self.capture)
        def coherent(b):
            b['local_first']['index'][0]['oid']='c'*40
            b['local_first']['index_digest']=rc.digest(b['local_first']['index'])
            b['local_last']=copy.deepcopy(b['local_first'])
        r,cap=self.changed(coherent)
        self.assertEqual(v.validate_result(r,capture=cap),r)
        # Same required proof class: valid stable changed index, still only captured analysis.
        self.assertEqual(semantic(r),semantic(self.good))
        # Change only one observation coherently as a truthful race: UNKNOWN, not parse rejection.
        r,cap=self.changed(lambda b:b['local_last'].update(config_digest='c'*64))
        self.assertEqual(v.validate_result(r,capture=cap),r)
        self.assertEqual(r['safe_to_resume'],'UNKNOWN')
        self.assertNotEqual(semantic(r),semantic(self.good))
        self.assertEqual(proof(r)['P9'],proof(self.good)['P9']) # no over-coupling into legacy accounting

    def test_generic_semantic_leaf_discrimination(self):
        from helpers.verifier_tamper import concrete_leaves,alternate,assign,audit
        base=copy.deepcopy(self.p['evidence'])
        self.remote(base)
        base['review']=[dict(path='work.txt',sha256='a'*64)]
        base['review_first']=[dict(path='work.txt',mode='100644',oid='a'*40)]
        base['review_last']=copy.deepcopy(base['review_first'])
        base['tests']=dict(result='PASSED',commands=['inert'],results=['pass'],bound_head=base['local_first']['head'])
        base['authority_description']='inert'
        base['expected_commit']=dict(parent=base['local_first']['head'],tree=base['local_first']['commits'][0]['tree'])
        d=base['handoff']; d['generation']=2; d['last_known_good']['generation']=2
        d['previous_known_good']=copy.deepcopy(d['last_known_good']); d['previous_known_good']['generation']=1
        for slot in (d['last_known_good'],d['previous_known_good']):
            slot['receipts']=dict.fromkeys(('local_commit','tracking_commit','remote_commit'),base['local_first']['head'])
        base['handoff_last']={k:d[k] for k in ('generation','digest','error_code')}
        for k in ('local_first','local_last'):
            base[k]['upstream']='refs/remotes/origin/main'
            base[k]['commits'][0]['parents']=['f'*40]
            base[k]['commits'].append(dict(oid='e'*40,tree=None,parents=None,error_code='TIMEOUT'))
        # Populate previous slot and nullable receipt/error variants in separate fixtures below.
        cap=synthetic(base); initial=v.verify(cap.projection,v.request_for(cap.projection),capture=cap)
        tested=set(); refused=set(); explanations=[]
        for path,pattern,spec,value in concrete_leaves(base,rc.BASIS,pattern='/input/reconciliation'):
            changed=alternate(spec,value)
            if changed==value: continue # closed singleton version/enum cannot vary validly
            b=copy.deepcopy(base); assign(b,path,changed)
            if path[0] in ('local_first','local_last'):
                local=b[path[0]]
                if path[-1]=='flag': assign(b,path,'S' if value!='S' else 'H')
                if path[-1]=='index_digest': local['index'][0]['oid']='d'*40
                local['index'].sort(key=lambda x:(x['path'],x['stage']))
                local['index_digest']=rc.digest(local['index'])
                # Preserve stable readings; mismatch with historical base is still real evidence.
                b['local_first']=copy.deepcopy(local); b['local_last']=copy.deepcopy(local)
            if path[0] in ('review','review_first','review_last'):
                if path[-1]=='path':
                    for k in ('review','review_first','review_last'): b[k][0]['path']=changed
                if path[0]!='review': b['review_first']=copy.deepcopy(b[path[0]]); b['review_last']=copy.deepcopy(b[path[0]])
            if path[0] in ('remote_first','remote_last','remote_request'):
                if path[-1] in ('tip','direct'):
                    for k in ('remote_first','remote_last'): b[k]['tip']=changed; b[k]['direct']=changed
                elif path[0] in ('remote_first','remote_last'):
                    other='remote_last' if path[0]=='remote_first' else 'remote_first'; b[other]=copy.deepcopy(b[path[0]])
                if 'identity' in path:
                    for k in ('remote_first','remote_last','remote_request'): b[k]['identity'][path[-1]]=changed
            d=b['handoff']
            if path[0] in ('handoff','handoff_last'):
                # Slot references and outer publication generation remain coherent.
                if path==('handoff','generation'):
                    d['last_known_good']['generation']=changed
                if path[-1]=='handoff_digest': d['last_known_good']['digest']=changed
                d['latest_attempt']['handoff_digest']=d['last_known_good']['digest']
                d['generation']=max(d['generation'],d['last_known_good']['generation'])
                if d['previous_known_good'] and d['previous_known_good']['generation']>=d['last_known_good']['generation']:
                    d['last_known_good']['generation']=d['previous_known_good']['generation']+1
                    d['generation']=d['last_known_good']['generation']
                b['handoff_last']={k:d[k] for k in ('generation','digest','error_code')}
            try:
                newcap=synthetic(b)
            except rc.ReconciliationError:
                refused.add(pattern); continue # incompatible enum/absence shape has a dedicated negative below
            new=v.verify(newcap.projection,v.request_for(newcap.projection),capture=newcap)
            self.assertEqual(v.validate_result(new,capture=newcap),new)
            # Actual changed leaves include linked fields, not just the original mutation.
            before_values={p:x for _,p,_,x in concrete_leaves(base,rc.BASIS,pattern='/input/reconciliation')}
            after_values={p:x for _,p,_,x in concrete_leaves(b,rc.BASIS,pattern='/input/reconciliation')}
            changed_paths=[p for p in before_values if before_values[p]!=after_values.get(p)]
            if changed_paths:
                try: delta,why=audit(initial,new,changed_paths)
                except AssertionError as e: self.fail((pattern,str(e)))
                explanations.extend(why)
            stale=copy.deepcopy(initial); stale['input']['reconciliation']=b
            if b!=base:
                with self.assertRaises(v.VerificationError): v.validate_result(stale,capture=cap)
            tested.add(pattern)
        self.assertGreater(len(tested),110)
        self.assertGreater(len(explanations),100)
        self.assertTrue(all(e[2] in v.NON_INFLUENCE for e in explanations))
        # Report explicit coverage counts for documentation, not a production telemetry stream.
        self.__class__.tamper_counts=(len(tested),len(refused),len(explanations))
        self.__class__.tamper_tested=tested
        self.__class__.tamper_refused=refused

    def test_harness_detects_both_coupling_defects(self):
        from helpers.verifier_tamper import audit
        broken=copy.deepcopy(self.good); broken['safe_to_resume']='NO'
        with self.assertRaises(AssertionError): audit(self.good,broken,['/input/annotation'])
        # Explicit pivotal witness: removing readback MUST change P11 and verdict, not merely its input copy.
        r,_=self.changed(lambda b:b.update(handoff_last=None))
        self.assertNotEqual(proof(r)['P11'],proof(self.good)['P11'])
        self.assertNotEqual(r['safe_to_resume'],self.good['safe_to_resume'])

    def test_limits_depth_bytes_and_missing_shapes(self):
        deep=None
        for _ in range(34): deep=[deep]
        with self.assertRaises(v.VerificationError): v._bounds(deep)
        with self.assertRaises(v.VerificationError): v._size(['a'*2048]*300)
        for key in ('identity','action','level','test_policy'):
            req=copy.deepcopy(self.request); del req[key]
            with self.assertRaises(v.VerificationError): v.verify(self.p,req,capture=self.capture)
        r=copy.deepcopy(self.good); r['proof_obligations'][0]['evidence_refs']=['/invented']
        with self.assertRaises(v.VerificationError): v.validate_result(r,capture=self.capture)
        req=copy.deepcopy(self.request); req['action']=['READ_ONLY_ANALYSIS','CONTINUE_EDITING']
        with self.assertRaises(v.VerificationError): v.verify(self.p,req,capture=self.capture)

    def test_remaining_semantic_leaf_shapes(self):
        from helpers.verifier_tamper import audit
        cases=[]
        for key in ('collection_error','local_error'):
            cases.append(([f'/input/reconciliation/{key}'],lambda b,key=key:b.update({key:'TIMEOUT'})))
        def handoff_failure(b):
            b['handoff']['error_code']='HANDOFF_UNAVAILABLE'
            b['handoff_last']['error_code']='HANDOFF_UNAVAILABLE'
        cases.append((['/input/reconciliation/handoff/error_code','/input/reconciliation/handoff_last/error_code'],handoff_failure))
        def failed_attempt(b):
            b['handoff']['latest_attempt'].update(status='FAILED',error_code='INPUT_REJECTED',handoff_digest=None)
        cases.append((['/input/reconciliation/handoff/latest_attempt/status','/input/reconciliation/handoff/latest_attempt/error_code','/input/reconciliation/handoff/latest_attempt/handoff_digest'],failed_attempt))
        for key,value in [('locks',['.git/index.lock']),('operations',['MERGE_HEAD'])]:
            cases.append(([f'/input/reconciliation/{k}/{key}/*' for k in ('local_first','local_last')],lambda b,key=key,value=value:[b[k].update({key:value}) for k in ('local_first','local_last')]))
        def remote_error(b):
            self.remote(b); b['remote_error']='TIMEOUT'
        cases.append((['/input/reconciliation/remote_error','/input/reconciliation/remote_request/expected_commit','/input/reconciliation/remote_first/tip','/input/reconciliation/remote_last/tip'],remote_error))
        def tracking_error(b):
            self.remote(b)
            for k in ('remote_first','remote_last'): b[k].update(tracking=None,tracking_error='REMOTE_REF_MISSING_OR_AMBIGUOUS')
        cases.append(([f'/input/reconciliation/{k}/tracking_error' for k in ('remote_first','remote_last')]+['/input/reconciliation/remote_request/expected_commit'],tracking_error))
        def review_error(b):
            b['review']=[dict(path='work.txt',sha256='a'*64)]; b['review_error']='CONTENT_CHANGED'
        cases.append((['/input/reconciliation/review_error'],review_error))
        covered=set()
        for leaves,mutate in cases:
            r,cap=self.changed(mutate)
            self.assertEqual(v.validate_result(r,capture=cap),r)
            audit(self.good,r,leaves); covered.update(leaves)
        for field in self.request:
            if field=='policy_profile': continue # version constant: rejected alternatives, separately tested
            if field=='identity':
                for sub in self.request[field]:
                    req=copy.deepcopy(self.request); req[field][sub]+=1
                    r=v.verify(self.p,req,capture=self.capture)
                    leaf=f'/input/request/identity/{sub}'; audit(self.good,r,[leaf]); covered.add(leaf)
                continue
            req=copy.deepcopy(self.request)
            req[field]={'project':self.request['project']+'x','action':'CONTINUE_EDITING','level':'REMOTE_VERIFIED','evidence_digest':'a'*64,'test_policy':'UNSPECIFIED'}[field]
            r=v.verify(self.p,req,capture=self.capture); leaf='/input/request/'+field
            audit(self.good,r,[leaf]); covered.add(leaf)
        self.__class__.other_tested=covered

    def test_semantic_enumeration_guard(self):
        # Run both reusable mutation classes, then require every semantic leaf accounted for.
        self.test_generic_semantic_leaf_discrimination()
        self.test_remaining_semantic_leaf_shapes()
        constants={'/verifier_version','/input/request/policy_profile'}
        all_semantic={p for p,e in REGISTRY.items() if e['class']=='SEMANTIC_INPUT'}
        self.assertEqual(all_semantic-(self.tamper_tested|self.other_tested),constants)
        req=copy.deepcopy(self.request); req['policy_profile']='unsupported'
        with self.assertRaises(v.VerificationError): v.verify(self.p,req,capture=self.capture)

    def test_maximum_supported_index_shape(self):
        b=copy.deepcopy(self.p['evidence'])
        # Large but valid inherited bounded evidence, under 256-KiB reconciler limit.
        b['local_first']['index']=[dict(path=f'p{i:04}',mode='100644',oid='a'*40,stage='0',flag='H') for i in range(600)]
        b['local_first']['index_digest']=rc.digest(b['local_first']['index']); b['local_last']=copy.deepcopy(b['local_first'])
        cap=synthetic(b); r=v.verify(cap.projection,v.request_for(cap.projection),capture=cap)
        self.assertEqual(r['safe_to_resume'],'YES'); self.assertLess(len(v.render_json(r,capture=cap).encode()),v.MAX_BYTES)
        b['local_first']['index']*=20
        with self.assertRaises(rc.ReconciliationError): synthetic(b)

if __name__=='__main__': unittest.main()
