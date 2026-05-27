from src.utils import (
    get_winding_teeth_indices,
    get_current_slot,
    is_starting_from_bottom,
)


def test_get_winding_teeth_indices_24n22p():
    winding_config_letters = (
        "AaAabBbBCcCcaAaABbBbcCcC"  # for 24n22p motor (24 slots, 22 poles)
    )
    teeth_indices = get_winding_teeth_indices(winding_config_letters)

    teeth_indices_a = [0, 1, 2, 3, 12, 13, 14, 15]
    teeth_indices_b = [4, 5, 6, 7, 16, 17, 18, 19]
    teeth_indices_c = [8, 9, 10, 11, 20, 21, 22, 23]

    assert teeth_indices == [teeth_indices_a, teeth_indices_b, teeth_indices_c]


def test_get_current_slot():
    m1_zero = -0.01
    slot_count = 24
    motor1_pos = -0.534
    current_slot = get_current_slot(motor1_pos, m1_zero, slot_count)
    assert current_slot == 2


def test_is_starting_from_bottom_24n22p():
    winding_config_letters = (
        "AaAabBbBCcCcaAaABbBbcCcC"  # for 24n22p motor (24 slots, 22 poles)
    )
    teeth_indices_a = [0, 1, 2, 3, 12, 13, 14, 15]
    teeth_indices_b = [4, 5, 6, 7, 16, 17, 18, 19]
    teeth_indices_c = [8, 9, 10, 11, 20, 21, 22, 23]

    expected_results_a_c = [
        False,  # starts_at = 0
        False,  # starts_at = 1
        True,  # starts_at = 2
        False,  # starts_at = 3
        False,  # starts_at = 4
        True,  # starts_at = 5
        False,  # starts_at = 6
        True,  # starts_at = 7
    ]

    for i, expected in enumerate(expected_results_a_c):
        assert (
            is_starting_from_bottom(i, winding_config_letters, teeth_indices_a)
            is expected
        )

    for i, expected in enumerate(expected_results_a_c):
        assert (
            is_starting_from_bottom(i, winding_config_letters, teeth_indices_c)
            is expected
        )

    expected_results_b = [
        False,  # starts_at = 0
        True,  # starts_at = 1
        False,  # starts_at = 2
        True,  # starts_at = 3
        False,  # starts_at = 4
        False,  # starts_at = 5
        True,  # starts_at = 6
        False,  # starts_at = 7
    ]

    for i, expected in enumerate(expected_results_b):
        assert (
            is_starting_from_bottom(i, winding_config_letters, teeth_indices_b)
            is expected
        )
