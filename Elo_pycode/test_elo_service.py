# tests/test_elo_service.py
# Tests para el sistema ELO de PyCode
# Verifican que las tablas de Coffee Break Python se aplican correctamente

import pytest
import sys
sys.path.insert(0, "../backend")

from app.services.elo_service import (
    process_attempt, get_rank, get_elo_delta,
    expected_score, EloRank, initial_elo,
    puzzle_difficulty_label, win_probability_label,
)


class TestGetRank:
    def test_basic_knowledge(self):
        assert get_rank(500) == EloRank.BASIC_KNOWLEDGE

    def test_beginner(self):
        assert get_rank(1000) == EloRank.BEGINNER
        assert get_rank(1050) == EloRank.BEGINNER

    def test_intermediate(self):
        assert get_rank(1500) == EloRank.INTERMEDIATE

    def test_expert(self):
        assert get_rank(1700) == EloRank.EXPERT

    def test_grandmaster(self):
        assert get_rank(2400) == EloRank.GRANDMASTER

    def test_world_class(self):
        assert get_rank(2500) == EloRank.WORLD_CLASS
        assert get_rank(9999) == EloRank.WORLD_CLASS

    def test_boundary_conditions(self):
        # 1499 → Experienced Learner, 1500 → Intermediate
        assert get_rank(1499) == EloRank.EXPERIENCED_LEARNER
        assert get_rank(1500) == EloRank.INTERMEDIATE


class TestEloDelta:
    """
    Verifica las tablas exactas de Coffee Break Python y NumPy
    """

    # Tabla Python (simple)
    def test_low_elo_correct(self):
        # 0-500: +43 si correcto
        assert get_elo_delta(300, correct=True, advanced=False) == 43

    def test_low_elo_incorrect(self):
        # 0-500: -12 si incorrecto
        assert get_elo_delta(300, correct=False, advanced=False) == -12

    def test_mid_elo_correct(self):
        # 500-1000: +21 si correcto
        assert get_elo_delta(750, correct=True, advanced=False) == 21

    def test_mid_elo_incorrect(self):
        # 500-1000: -34 si incorrecto
        assert get_elo_delta(750, correct=False, advanced=False) == -34

    def test_high_elo_correct(self):
        # 1000-1500: +9 si correcto
        assert get_elo_delta(1200, correct=True, advanced=False) == 9

    def test_high_elo_incorrect(self):
        # 1000-1500: -46 si incorrecto
        assert get_elo_delta(1200, correct=False, advanced=False) == -46

    # Tabla NumPy (advanced)
    def test_advanced_low_elo_correct(self):
        # 0-1500: +60 si correcto
        assert get_elo_delta(1000, correct=True, advanced=True) == 60

    def test_advanced_low_elo_incorrect(self):
        # 0-1500: -4 si incorrecto
        assert get_elo_delta(1000, correct=False, advanced=True) == -4

    def test_advanced_very_high_elo(self):
        # >2200: +10 correcto, -60 incorrecto
        assert get_elo_delta(2300, correct=True, advanced=True) == 10
        assert get_elo_delta(2300, correct=False, advanced=True) == -60


class TestExpectedScore:
    def test_equal_elos(self):
        # Mismos ELOs → 50% de probabilidad
        prob = expected_score(1500, 1500)
        assert abs(prob - 0.5) < 0.001

    def test_higher_user_elo(self):
        # Usuario más fuerte → mayor probabilidad
        prob = expected_score(1800, 1200)
        assert prob > 0.9

    def test_lower_user_elo(self):
        # Usuario más débil → menor probabilidad
        prob = expected_score(1200, 1800)
        assert prob < 0.1

    def test_400_point_difference(self):
        # Por definición ELO: +400 pts → ~91% de probabilidad
        prob = expected_score(1900, 1500)
        assert abs(prob - 0.909) < 0.01


class TestProcessAttempt:
    def test_correct_answer_increases_elo(self):
        result = process_attempt(1000, 1200, correct=True)
        assert result.user_elo_after > result.user_elo_before
        assert result.delta_user > 0

    def test_incorrect_answer_decreases_elo(self):
        result = process_attempt(1500, 1200, correct=False)
        assert result.user_elo_after < result.user_elo_before
        assert result.delta_user < 0

    def test_rank_detection(self):
        result = process_attempt(1499, 1200, correct=True)
        # Si el ELO sube de 1499 a ≥1500, el rango cambia
        if result.user_elo_after >= 1500:
            assert result.rank_changed is True
            assert result.rank_after == EloRank.INTERMEDIATE.value

    def test_elo_floor_at_zero(self):
        # El ELO nunca debe ser negativo
        result = process_attempt(10, 2000, correct=False)
        assert result.user_elo_after >= 0

    def test_puzzle_elo_increases_when_user_fails(self):
        # Si el usuario falla, el puzzle "ganó" → su ELO sube
        result = process_attempt(1500, 1200, correct=False)
        assert result.puzzle_elo_after >= result.puzzle_elo_before

    def test_puzzle_elo_decreases_when_user_wins(self):
        # Si el usuario acierta, el puzzle "perdió" → su ELO baja
        result = process_attempt(1200, 1500, correct=True)
        assert result.puzzle_elo_after <= result.puzzle_elo_before

    def test_advanced_puzzle_uses_different_table(self):
        # Con advanced=True, los deltas son distintos
        r_simple = process_attempt(1200, 1500, correct=True, advanced=False)
        r_advanced = process_attempt(1200, 1500, correct=True, advanced=True)
        # advanced da +60 vs +9 para ELO 1200
        assert r_advanced.delta_user > r_simple.delta_user

    def test_expected_probability_in_result(self):
        result = process_attempt(1500, 1500, correct=True)
        # Mismos ELOs → ~50%
        assert abs(result.expected_probability - 0.5) < 0.01


class TestInitialElo:
    def test_beginner_starts_at_1000(self):
        assert initial_elo("beginner") == 1000

    def test_intermediate_starts_at_1500(self):
        assert initial_elo("intermediate") == 1500

    def test_advanced_starts_at_2000(self):
        assert initial_elo("advanced") == 2000

    def test_unknown_defaults_to_beginner(self):
        assert initial_elo("unknown") == 1000


class TestDifficultyLabels:
    def test_introductory(self):
        assert puzzle_difficulty_label(700) == "Introductory"

    def test_easy(self):
        assert puzzle_difficulty_label(900) == "Easy"

    def test_medium(self):
        assert puzzle_difficulty_label(1200) == "Medium"

    def test_hard(self):
        assert puzzle_difficulty_label(1500) == "Hard"

    def test_expert(self):
        assert puzzle_difficulty_label(1800) == "Expert"

    def test_master(self):
        assert puzzle_difficulty_label(2100) == "Master"


class TestWinProbabilityLabel:
    def test_very_likely(self):
        assert win_probability_label(0.90) == "Very likely to solve"

    def test_likely(self):
        assert win_probability_label(0.70) == "Likely to solve"

    def test_even(self):
        assert win_probability_label(0.50) == "Even match"

    def test_challenging(self):
        assert win_probability_label(0.30) == "Challenging"

    def test_very_challenging(self):
        assert win_probability_label(0.10) == "Very challenging"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
