import itertools

import pytest

from generator import NameGenerator
from morphology import CMUDictMorphologyService


@pytest.fixture(scope='session')
def cmudict_service():
    svc = CMUDictMorphologyService()
    svc.bootstrap()
    return svc


@pytest.fixture(scope='session')
def low_diversity_generator(cmudict_service):
    return NameGenerator(cmudict_service, diversity_level=NameGenerator.DIVERSITY_LOW)


@pytest.fixture(scope='session')
def high_diversity_generator(cmudict_service):
    return NameGenerator(cmudict_service, diversity_level=NameGenerator.DIVERSITY_HIGH)


def test_cmu_sample_words(cmudict_service):
    random_10 = list(itertools.islice(cmudict_service.sample_words(), 10))
    assert len(random_10) == 10
    assert all(len(word) > 0 for word in random_10)


def test_cmu_syllabify(cmudict_service):
    assert cmudict_service.syllabify('batch') == [
        ['B', 'AE1', 'CH'],
    ]
    assert cmudict_service.syllabify('precaution') == [
        ['P', 'R', 'IY0'],
        ['K', 'AO1'],
        ['SH', 'AH0', 'N'],
    ]
    assert cmudict_service.syllabify('volunteer') == [
        ['V', 'AA2'],
        ['L', 'AH0'],
        ['N', 'T', 'IH1', 'R'],
    ]


def test_cmu_detects_last_vowel_sound(cmudict_service):
    assert cmudict_service.last_vowel_sound('batch') == 'AE'
    assert cmudict_service.last_vowel_sound('precaution') == 'AH'
    assert cmudict_service.last_vowel_sound('volunteer') == 'IH'


def test_cmu_detects_stressed_syllable(cmudict_service):
    assert cmudict_service.stressed_syllable_index('batch') == 0
    assert cmudict_service.stressed_syllable_index('precaution') == 1
    assert cmudict_service.stressed_syllable_index('volunteer') == 2


def test_low_diversity_generator(low_diversity_generator):
    name = low_diversity_generator.random_name()
    first_name, last_name = name.split(' ')
    assert first_name.startswith('B')
    assert last_name.startswith('C')


def test_high_diversity_generator(high_diversity_generator):
    name = high_diversity_generator.random_name()
    first_name, last_name = name.split(' ')
    assert len(first_name) > 1
    assert len(last_name) > 1
    assert first_name[0].isupper()
    assert last_name[0].isupper()
