"""Reusable full-projection dependency audit, no production provenance claims."""
import copy
from cgc import safe_resume as v
from cgc.verifier_registry import REGISTRY


def claims(result):
    result=copy.deepcopy(result)
    out={row['id']:row for row in result.pop('proof_obligations')}
    out['facts']=result.pop('facts')
    result.pop('input'); result.pop('verifier_version')
    out['aggregation']=result
    return out


def audit(before,after,changed_leaves):
    """Assert influence limits and return explicit field/claim no-op explanations.

    Predicate-specific degradation witnesses accompany this general audit: identical proof
    classes alone cannot establish that the classifier actually uses a required dependency.
    """
    entries=[REGISTRY[p] for p in changed_leaves]
    allowed=set().union(*(set(e.get('allowed_influence_scope',())) for e in entries))
    a,b=claims(before),claims(after)
    delta={k for k in a if a[k]!=b[k]}
    assert delta<=allowed, ('OVER_COUPLING',delta-allowed,changed_leaves)
    explanations=[]
    for leaf,entry in zip(changed_leaves,entries):
        if entry['class']=='DERIVED_FIELD': continue # validated from their registered semantic sources
        if entry['class']=='NON_SEMANTIC_METADATA':
            assert not delta, ('METADATA_INFLUENCE',leaf)
            explanations.append((leaf,'all','NON_SEMANTIC_METADATA',entry['rationale']))
        else:
            for claim in entry['dependent_claims']:
                if claim in delta: continue
                outside=claim.startswith('P') and a[claim]['status']=='NOT_APPLICABLE'
                reason='OUTSIDE_REQUESTED_SCOPE' if outside else 'SAME_PROOF_CLASS'
                assert reason in entry['allowed_non_influence_reasons']
                explanations.append((leaf,claim,reason,entry['predicate']))
    assert delta or explanations, 'UNEXPLAINED_SEMANTIC_NO_OP'
    return delta,explanations


def concrete_leaves(value,spec,path=(),pattern=''):
    if isinstance(spec,tuple) and spec[0]=='nullable':
        if value is None: return
        spec=spec[1]
    if isinstance(spec,dict):
        for key,sub in spec.items(): yield from concrete_leaves(value[key],sub,path+(key,),pattern+'/'+key)
    elif isinstance(spec,tuple) and spec[0]=='array':
        for i,sub in enumerate(value): yield from concrete_leaves(sub,spec[1],path+(i,),pattern+'/*')
    else: yield path,pattern,spec,value


def alternate(spec,value):
    if isinstance(spec,tuple) and spec[0]=='enum':
        choices=[x for x in spec[1] if x!=value]
        return choices[0] if choices else value
    if isinstance(value,int): return value+1
    name=getattr(spec,'__name__','')
    if name=='_stamp': return '2026-09-23T00:00:00Z'
    if name in ('sha','oid'): return ('b' if value[0]!='b' else 'c')*len(value)
    if name=='artifact': return '.git/HEAD.lock'
    if name=='code': return 'TIMEOUT' if value!='TIMEOUT' else 'TARGET_CHANGED'
    if isinstance(value,str): return value+'x'
    return value


def assign(root,path,value):
    for key in path[:-1]: root=root[key]
    root[path[-1]]=value
