"""Strict manifest/runtime-consistency checks without third-party libraries."""
from __future__ import annotations

import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from atda_pathb_fortress import Policy


class ManifestValidationError(ValueError):
    """Manifest contradicts reference configuration or its assurance limits."""


def _require(condition: bool, field: str) -> None:
    """Mandatory check, still active in optimized Python (`python -O`)."""
    if not condition:
        raise ManifestValidationError(f"Manifest validation failed: {field}")


def validate(path: pathlib.Path | None = None) -> dict:
    selected = path or ROOT / 'manifest' / 'ATDA_Privacy_Safety_Manifest_v1_2.json'
    with selected.open('r', encoding='utf-8') as handle:
        data = json.load(handle)
    policy = Policy()
    b = data['data_paths']['B']
    a = data['data_paths']['A']
    pq = data['post_quantum_migration']
    _require(data['status'] == 'PUBLIC_REFERENCE_NOT_PRODUCTION_CERTIFIED', 'status')
    _require(a['interference_cleaners_outcome'] == 'MAINTENANCE_ONLY', 'data_paths.A.interference_cleaners_outcome')
    _require(a['runtime_implemented_in_this_repository'] is False, 'data_paths.A.runtime_implemented_in_this_repository')
    _require(b['hardware_strip_pii_before_buffer'] is True, 'data_paths.B.hardware_strip_pii_before_buffer')
    _require(b['hardware_strip_pii_verified'] is False, 'data_paths.B.hardware_strip_pii_verified')
    _require(type(b['k_min']) is int and b['k_min'] == policy.k_min, 'data_paths.B.k_min')
    _require(b['dynamic_window_minutes'] == list(policy.window_steps_min), 'data_paths.B.dynamic_window_minutes')
    _require(b['fixed_categories'] == list(policy.categories), 'data_paths.B.fixed_categories')
    _require(type(b['max_interactions_per_epoch']) is int and b['max_interactions_per_epoch'] == policy.epoch_total_max, 'data_paths.B.max_interactions_per_epoch')
    _require(type(b['noise_q_numerator']) is int and b['noise_q_numerator'] == policy.q_num, 'data_paths.B.noise_q_numerator')
    _require(type(b['noise_q_denominator']) is int and b['noise_q_denominator'] == policy.q_den, 'data_paths.B.noise_q_denominator')
    _require(type(b['ideal_fixed_query_epsilon']) in (float, int) and math.isclose(b['ideal_fixed_query_epsilon'], policy.epsilon_query), 'data_paths.B.ideal_fixed_query_epsilon')
    _require(type(b['l1_vector_sensitivity']) is int and b['l1_vector_sensitivity'] == 1, 'data_paths.B.l1_vector_sensitivity')
    _require(b['end_to_end_pure_dp_claim'] is False, 'data_paths.B.end_to_end_pure_dp_claim')
    _require(b['person_level_dp_claim'] is False, 'data_paths.B.person_level_dp_claim')
    _require(b['gdpr_anonymisation_certified'] is False, 'data_paths.B.gdpr_anonymisation_certified')
    _require(b['no_release_when_true_count_under_k'] is True, 'data_paths.B.no_release_when_true_count_under_k')
    _require(pq['transition_design_only'] is True, 'post_quantum_migration.transition_design_only')
    _require(pq['fips_140_3_module_validation_confirmed'] is False, 'post_quantum_migration.fips_140_3_module_validation_confirmed')
    _require(data['assurance']['production_authorisation'] is False, 'assurance.production_authorisation')
    _require(data['provenance']['reconstruction_is_not_original_2025_code'] is True, 'provenance.reconstruction_is_not_original_2025_code')
    return data


if __name__ == '__main__':
    validated = validate()
    print('PASS manifest:', validated['manifest_version'])
