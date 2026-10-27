"""Strict manifest/runtime-consistency checks without third-party libraries."""
from __future__ import annotations

import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from atda_pathb_fortress import Policy


def validate(path: pathlib.Path | None = None) -> dict:
    selected = path or ROOT / 'manifest' / 'ATDA_Privacy_Safety_Manifest_v1_2.json'
    with selected.open('r', encoding='utf-8') as handle:
        data = json.load(handle)
    policy = Policy()
    b = data['data_paths']['B']
    a = data['data_paths']['A']
    pq = data['post_quantum_migration']
    assert data['status'] == 'PUBLIC_REFERENCE_NOT_PRODUCTION_CERTIFIED'
    assert a['interference_cleaners_outcome'] == 'MAINTENANCE_ONLY'
    assert not a['runtime_implemented_in_this_repository']
    assert b['hardware_strip_pii_before_buffer'] is True
    assert b['hardware_strip_pii_verified'] is False
    assert b['k_min'] == policy.k_min
    assert b['dynamic_window_minutes'] == list(policy.window_steps_min)
    assert b['fixed_categories'] == list(policy.categories)
    assert b['max_interactions_per_epoch'] == policy.epoch_total_max
    assert b['noise_q_numerator'] == policy.q_num
    assert b['noise_q_denominator'] == policy.q_den
    assert math.isclose(b['ideal_fixed_query_epsilon'], policy.epsilon_query)
    assert b['l1_vector_sensitivity'] == 1
    assert b['end_to_end_pure_dp_claim'] is False
    assert b['person_level_dp_claim'] is False
    assert b['gdpr_anonymisation_certified'] is False
    assert b['no_release_when_true_count_under_k'] is True
    assert pq['transition_design_only'] is True
    assert pq['fips_140_3_module_validation_confirmed'] is False
    assert data['assurance']['production_authorisation'] is False
    assert data['provenance']['reconstruction_is_not_original_2025_code'] is True
    return data


if __name__ == '__main__':
    validated = validate()
    print('PASS manifest:', validated['manifest_version'])
