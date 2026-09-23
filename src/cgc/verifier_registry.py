"""Explicit concrete-leaf ledger; array * is an element, never a subtree wildcard.

Aggregation is the documented P1-P12 downstream verdict/decision/resolution cascade.
Schema additions must update this independent ledger and discrimination acceptance.
"""
GROUPS = {'G1': {'class': 'DERIVED_FIELD',
        'derivation_sources': ['/input/request',
                               '/input/reconciliation',
                               'trusted capture binding']},
 'G10': {'allowed_influence_scope': ['P2', 'P10', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'local_last',
         'dependent_claims': ['P2', 'P10', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G11': {'allowed_influence_scope': ['facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'observed_at',
         'dependent_claims': ['facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G12': {'allowed_influence_scope': ['P1', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'project',
         'dependent_claims': ['P1', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G13': {'allowed_influence_scope': ['P6', 'P7', 'P10', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'remote_error',
         'dependent_claims': ['P6', 'P7', 'P10', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G14': {'allowed_influence_scope': ['P2', 'P6', 'P7', 'P10', 'P11', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'remote_first',
         'dependent_claims': ['P2', 'P6', 'P7', 'P10', 'P11', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G15': {'allowed_influence_scope': ['P2', 'P6', 'P7', 'P10', 'P11', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'remote_last',
         'dependent_claims': ['P2', 'P6', 'P7', 'P10', 'P11', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G16': {'allowed_influence_scope': ['P2', 'P6', 'P7', 'P10', 'P11', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'remote_request',
         'dependent_claims': ['P2', 'P6', 'P7', 'P10', 'P11', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G17': {'allowed_influence_scope': ['facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'requested_operation',
         'dependent_claims': ['facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G18': {'allowed_influence_scope': ['P2', 'P10', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'review',
         'dependent_claims': ['P2', 'P10', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G19': {'allowed_influence_scope': ['P10', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'review_error',
         'dependent_claims': ['P10', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G2': {'class': 'NON_SEMANTIC_METADATA',
        'dependent_claims': [],
        'rationale': 'Quoted annotation only.'},
 'G20': {'allowed_influence_scope': ['P2', 'P10', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'review_first',
         'dependent_claims': ['P2', 'P10', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G21': {'allowed_influence_scope': ['P2', 'P10', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'review_last',
         'dependent_claims': ['P2', 'P10', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G22': {'allowed_influence_scope': ['P9', 'facts', 'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                           'OUTSIDE_REQUESTED_SCOPE',
                                           'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                           'DUPLICATE_EQUIVALENT_EVIDENCE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'tests',
         'dependent_claims': ['P9', 'facts'],
         'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                      'producer and out-of-scope claims cannot gain proof.'},
 'G23': {'allowed_influence_scope': ['P1',
                                     'P2',
                                     'P3',
                                     'P4',
                                     'P5',
                                     'P6',
                                     'P7',
                                     'P8',
                                     'P9',
                                     'P10',
                                     'P11',
                                     'P12',
                                     'facts',
                                     'aggregation'],
         'allowed_non_influence_reasons': ['SAME_PROOF_CLASS', 'OUTSIDE_REQUESTED_SCOPE'],
         'class': 'SEMANTIC_INPUT',
         'coherence_group': 'request',
         'dependent_claims': ['P1',
                              'P2',
                              'P3',
                              'P4',
                              'P5',
                              'P6',
                              'P7',
                              'P8',
                              'P9',
                              'P10',
                              'P11',
                              'P12',
                              'facts'],
         'predicate': 'Exact versioned profile, project/state binding. Version constants have no '
                      'alternate supported value.'},
 'G3': {'class': 'NON_SEMANTIC_METADATA',
        'dependent_claims': [],
        'rationale': 'Inert context; exact capture/reference bytes may change, factual proof does '
                     'not.'},
 'G4': {'allowed_influence_scope': ['P2', 'P10', 'facts', 'aggregation'],
        'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                          'OUTSIDE_REQUESTED_SCOPE',
                                          'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                          'DUPLICATE_EQUIVALENT_EVIDENCE'],
        'class': 'SEMANTIC_INPUT',
        'coherence_group': 'collection_error',
        'dependent_claims': ['P2', 'P10', 'facts'],
        'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                     'producer and out-of-scope claims cannot gain proof.'},
 'G5': {'allowed_influence_scope': ['P10', 'facts', 'aggregation'],
        'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                          'OUTSIDE_REQUESTED_SCOPE',
                                          'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                          'DUPLICATE_EQUIVALENT_EVIDENCE'],
        'class': 'SEMANTIC_INPUT',
        'coherence_group': 'expected_commit',
        'dependent_claims': ['P10', 'facts'],
        'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                     'producer and out-of-scope claims cannot gain proof.'},
 'G6': {'allowed_influence_scope': ['P1', 'P2', 'P4', 'P9', 'P10', 'P11', 'facts', 'aggregation'],
        'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                          'OUTSIDE_REQUESTED_SCOPE',
                                          'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                          'DUPLICATE_EQUIVALENT_EVIDENCE'],
        'class': 'SEMANTIC_INPUT',
        'coherence_group': 'handoff',
        'dependent_claims': ['P1', 'P2', 'P4', 'P9', 'P10', 'P11', 'facts'],
        'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                     'producer and out-of-scope claims cannot gain proof.'},
 'G7': {'allowed_influence_scope': ['P2', 'P10', 'P11', 'facts', 'aggregation'],
        'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                          'OUTSIDE_REQUESTED_SCOPE',
                                          'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                          'DUPLICATE_EQUIVALENT_EVIDENCE'],
        'class': 'SEMANTIC_INPUT',
        'coherence_group': 'handoff_last',
        'dependent_claims': ['P2', 'P10', 'P11', 'facts'],
        'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                     'producer and out-of-scope claims cannot gain proof.'},
 'G8': {'allowed_influence_scope': ['P2', 'P10', 'facts', 'aggregation'],
        'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                          'OUTSIDE_REQUESTED_SCOPE',
                                          'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                          'DUPLICATE_EQUIVALENT_EVIDENCE'],
        'class': 'SEMANTIC_INPUT',
        'coherence_group': 'local_error',
        'dependent_claims': ['P2', 'P10', 'facts'],
        'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                     'producer and out-of-scope claims cannot gain proof.'},
 'G9': {'allowed_influence_scope': ['P1', 'P2', 'P4', 'P7', 'P9', 'P10', 'facts', 'aggregation'],
        'allowed_non_influence_reasons': ['SAME_PROOF_CLASS',
                                          'OUTSIDE_REQUESTED_SCOPE',
                                          'SUPERSEDED_BY_CURRENT_OBSERVATION',
                                          'DUPLICATE_EQUIVALENT_EVIDENCE'],
        'class': 'SEMANTIC_INPUT',
        'coherence_group': 'local_first',
        'dependent_claims': ['P1', 'P2', 'P4', 'P7', 'P9', 'P10', 'facts'],
        'predicate': 'Compare required-domain presence/equality/relationships; unsupported '
                     'producer and out-of-scope claims cannot gain proof.'}}

LEAVES = {
'G1': """
/authority_required
/automatic_mutation_authorized
/blockers/*
/decision_state
/facts/cause
/facts/claim_freshness/checkpoint_receipt
/facts/claim_freshness/durable_intent
/facts/claim_freshness/local_git_observation
/facts/claim_freshness/remote_ref_observation
/facts/claim_freshness/reviewed_content
/facts/claim_freshness/test_applicability
/facts/collection_outcome
/facts/current_head
/facts/evidence_refs/*
/facts/head_relationship
/facts/historical_head
/facts/historical_test_result
/facts/kind
/facts/relationships/*/current
/facts/relationships/*/domain
/facts/relationships/*/freshness
/facts/relationships/*/historical
/facts/relationships/*/reason
/facts/relationships/*/subject
/facts/remote_observation
/facts/review_applicability
/facts/test_applicability
/input/provenance
/mutation_allowed
/next_exact_action/description
/next_exact_action/kind
/non_influence_reasons/*/claim
/non_influence_reasons/*/reason
/preconditions_for_future_action/*
/proof_obligations/*/evidence_refs/*
/proof_obligations/*/id
/proof_obligations/*/plane
/proof_obligations/*/reason
/proof_obligations/*/required
/proof_obligations/*/resolution_class
/proof_obligations/*/status
/resolution_plan/*/kind
/resolution_plan/*/obligation
/resolution_plan/*/resolution_class
/resolution_plan/*/scope_limit
/resolution_plan/*/source
/safe_to_resume
/unknowns/*
""".split(),
'G2': """
/input/annotation
""".split(),
'G3': """
/input/reconciliation/authority_description
/input/reconciliation/handoff/last_known_good/known_failures/*
/input/reconciliation/handoff/last_known_good/next_exact_action
/input/reconciliation/handoff/last_known_good/test_commands/*
/input/reconciliation/handoff/last_known_good/test_results/*
/input/reconciliation/handoff/previous_known_good/known_failures/*
/input/reconciliation/handoff/previous_known_good/next_exact_action
/input/reconciliation/handoff/previous_known_good/test_commands/*
/input/reconciliation/handoff/previous_known_good/test_results/*
/input/reconciliation/tests/commands/*
/input/reconciliation/tests/results/*
""".split(),
'G4': """
/input/reconciliation/collection_error
""".split(),
'G5': """
/input/reconciliation/expected_commit/parent
/input/reconciliation/expected_commit/tree
""".split(),
'G6': """
/input/reconciliation/handoff/digest
/input/reconciliation/handoff/error_code
/input/reconciliation/handoff/generation
/input/reconciliation/handoff/last_known_good/base_branch
/input/reconciliation/handoff/last_known_good/base_head
/input/reconciliation/handoff/last_known_good/base_identity/device
/input/reconciliation/handoff/last_known_good/base_identity/git_device
/input/reconciliation/handoff/last_known_good/base_identity/git_inode
/input/reconciliation/handoff/last_known_good/base_identity/inode
/input/reconciliation/handoff/last_known_good/digest
/input/reconciliation/handoff/last_known_good/evidence_basis
/input/reconciliation/handoff/last_known_good/generation
/input/reconciliation/handoff/last_known_good/paths/*
/input/reconciliation/handoff/last_known_good/phase
/input/reconciliation/handoff/last_known_good/publication_status
/input/reconciliation/handoff/last_known_good/receipts/local_commit
/input/reconciliation/handoff/last_known_good/receipts/remote_commit
/input/reconciliation/handoff/last_known_good/receipts/tracking_commit
/input/reconciliation/handoff/last_known_good/reported_safe_to_resume
/input/reconciliation/handoff/last_known_good/requested_level
/input/reconciliation/handoff/last_known_good/test_result
/input/reconciliation/handoff/latest_attempt/at
/input/reconciliation/handoff/latest_attempt/error_code
/input/reconciliation/handoff/latest_attempt/handoff_digest
/input/reconciliation/handoff/latest_attempt/status
/input/reconciliation/handoff/previous_known_good/base_branch
/input/reconciliation/handoff/previous_known_good/base_head
/input/reconciliation/handoff/previous_known_good/base_identity/device
/input/reconciliation/handoff/previous_known_good/base_identity/git_device
/input/reconciliation/handoff/previous_known_good/base_identity/git_inode
/input/reconciliation/handoff/previous_known_good/base_identity/inode
/input/reconciliation/handoff/previous_known_good/digest
/input/reconciliation/handoff/previous_known_good/evidence_basis
/input/reconciliation/handoff/previous_known_good/generation
/input/reconciliation/handoff/previous_known_good/paths/*
/input/reconciliation/handoff/previous_known_good/phase
/input/reconciliation/handoff/previous_known_good/publication_status
/input/reconciliation/handoff/previous_known_good/receipts/local_commit
/input/reconciliation/handoff/previous_known_good/receipts/remote_commit
/input/reconciliation/handoff/previous_known_good/receipts/tracking_commit
/input/reconciliation/handoff/previous_known_good/reported_safe_to_resume
/input/reconciliation/handoff/previous_known_good/requested_level
/input/reconciliation/handoff/previous_known_good/test_result
""".split(),
'G7': """
/input/reconciliation/handoff_last/digest
/input/reconciliation/handoff_last/error_code
/input/reconciliation/handoff_last/generation
""".split(),
'G8': """
/input/reconciliation/local_error
""".split(),
'G9': """
/input/reconciliation/local_first/branch
/input/reconciliation/local_first/changes/*/index
/input/reconciliation/local_first/changes/*/path
/input/reconciliation/local_first/changes/*/worktree
/input/reconciliation/local_first/commits/*/error_code
/input/reconciliation/local_first/commits/*/oid
/input/reconciliation/local_first/commits/*/parents/*
/input/reconciliation/local_first/commits/*/tree
/input/reconciliation/local_first/config_digest
/input/reconciliation/local_first/head
/input/reconciliation/local_first/identity/device
/input/reconciliation/local_first/identity/git_device
/input/reconciliation/local_first/identity/git_inode
/input/reconciliation/local_first/identity/inode
/input/reconciliation/local_first/index/*/flag
/input/reconciliation/local_first/index/*/mode
/input/reconciliation/local_first/index/*/oid
/input/reconciliation/local_first/index/*/path
/input/reconciliation/local_first/index/*/stage
/input/reconciliation/local_first/index_digest
/input/reconciliation/local_first/inspection_digest
/input/reconciliation/local_first/locks/*
/input/reconciliation/local_first/metadata_digest
/input/reconciliation/local_first/operations/*
/input/reconciliation/local_first/upstream
""".split(),
'G10': """
/input/reconciliation/local_last/branch
/input/reconciliation/local_last/changes/*/index
/input/reconciliation/local_last/changes/*/path
/input/reconciliation/local_last/changes/*/worktree
/input/reconciliation/local_last/commits/*/error_code
/input/reconciliation/local_last/commits/*/oid
/input/reconciliation/local_last/commits/*/parents/*
/input/reconciliation/local_last/commits/*/tree
/input/reconciliation/local_last/config_digest
/input/reconciliation/local_last/head
/input/reconciliation/local_last/identity/device
/input/reconciliation/local_last/identity/git_device
/input/reconciliation/local_last/identity/git_inode
/input/reconciliation/local_last/identity/inode
/input/reconciliation/local_last/index/*/flag
/input/reconciliation/local_last/index/*/mode
/input/reconciliation/local_last/index/*/oid
/input/reconciliation/local_last/index/*/path
/input/reconciliation/local_last/index/*/stage
/input/reconciliation/local_last/index_digest
/input/reconciliation/local_last/inspection_digest
/input/reconciliation/local_last/locks/*
/input/reconciliation/local_last/metadata_digest
/input/reconciliation/local_last/operations/*
/input/reconciliation/local_last/upstream
""".split(),
'G11': """
/input/reconciliation/observed_at
""".split(),
'G12': """
/input/reconciliation/project
""".split(),
'G13': """
/input/reconciliation/remote_error
""".split(),
'G14': """
/input/reconciliation/remote_first/config_digest
/input/reconciliation/remote_first/direct
/input/reconciliation/remote_first/identity/device
/input/reconciliation/remote_first/identity/inode
/input/reconciliation/remote_first/tip
/input/reconciliation/remote_first/tracking
/input/reconciliation/remote_first/tracking_error
""".split(),
'G15': """
/input/reconciliation/remote_last/config_digest
/input/reconciliation/remote_last/direct
/input/reconciliation/remote_last/identity/device
/input/reconciliation/remote_last/identity/inode
/input/reconciliation/remote_last/tip
/input/reconciliation/remote_last/tracking
/input/reconciliation/remote_last/tracking_error
""".split(),
'G16': """
/input/reconciliation/remote_request/expected_commit
/input/reconciliation/remote_request/identity/device
/input/reconciliation/remote_request/identity/inode
/input/reconciliation/remote_request/path
/input/reconciliation/remote_request/ref
/input/reconciliation/remote_request/tracking_ref
""".split(),
'G17': """
/input/reconciliation/requested_operation
""".split(),
'G18': """
/input/reconciliation/review/*/path
/input/reconciliation/review/*/sha256
""".split(),
'G19': """
/input/reconciliation/review_error
""".split(),
'G20': """
/input/reconciliation/review_first/*/mode
/input/reconciliation/review_first/*/oid
/input/reconciliation/review_first/*/path
""".split(),
'G21': """
/input/reconciliation/review_last/*/mode
/input/reconciliation/review_last/*/oid
/input/reconciliation/review_last/*/path
""".split(),
'G22': """
/input/reconciliation/tests/bound_head
/input/reconciliation/tests/result
""".split(),
'G23': """
/input/request/action
/input/request/evidence_digest
/input/request/identity/device
/input/request/identity/git_device
/input/request/identity/git_inode
/input/request/identity/inode
/input/request/level
/input/request/policy_profile
/input/request/project
/input/request/test_policy
/verifier_version
""".split(),
}

REGISTRY = {path: GROUPS[group] for group, paths in LEAVES.items() for path in paths}

# Exact derived dependencies supplement the input ledger; these are explicit output leaves.
DERIVATIONS = {
    '/input/reconciliation/local_first/index_digest': ('/input/reconciliation/local_first/index/*',),
    '/input/reconciliation/local_last/index_digest': ('/input/reconciliation/local_last/index/*',),
    '/input/provenance': ('trusted capture binding', '/input/reconciliation'),
    '/mutation_allowed': ('fixed observational capability policy',),
    '/automatic_mutation_authorized': ('fixed observational capability policy',),
    '/safe_to_resume': ('/proof_obligations/*', 'evidence-plane composition rule'),
    '/decision_state': ('/safe_to_resume', '/input/request/action'),
    '/authority_required': ('/input/request/action',),
    '/blockers/*': ('/proof_obligations/*', 'resolution priority'),
    '/unknowns/*': ('/proof_obligations/*',),
    '/next_exact_action/kind': ('/resolution_plan/*',),
    '/next_exact_action/description': ('/resolution_plan/*',),
    '/preconditions_for_future_action/*': ('fixed no-execution policy', '/input/request'),
    '/non_influence_reasons/*/claim': ('/proof_obligations/*/required',),
    '/non_influence_reasons/*/reason': ('/proof_obligations/*/required', 'profile omission rule'),
}
for leaf, sources in DERIVATIONS.items():
    REGISTRY[leaf] = {'class': 'DERIVED_FIELD', 'derivation_sources': list(sources)}
