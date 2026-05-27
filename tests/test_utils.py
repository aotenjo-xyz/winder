from src.utils import (
    get_winding_teeth_indices,
    get_current_slot,
    is_starting_from_bottom,
)

teeth_indices_24n22p = [
    [0, 1, 2, 3, 12, 13, 14, 15],
    [4, 5, 6, 7, 16, 17, 18, 19],
    [8, 9, 10, 11, 20, 21, 22, 23],
]

teeth_indices_12n14p = [
    [0, 1, 6, 7],
    [2, 3, 8, 9],
    [4, 5, 10, 11],
]

teeth_indices_36n40p = [
    [0, 1, 2, 9, 10, 11, 18, 19, 20, 27, 28, 29],
    [3, 4, 5, 12, 13, 14, 21, 22, 23, 30, 31, 32],
    [6, 7, 8, 15, 16, 17, 24, 25, 26, 33, 34, 35],
]

winding_config_letters_24n22p = (
    "AaAabBbBCcCcaAaABbBbcCcC"  # for 24n22p motor (24 slots, 22 poles)
)

winding_config_letters_12n14p = "AabBCcaABbcC"  # for 12n14p motor (12 slots, 14 poles)

winding_config_letters_36n40p = (
    "AaABbBCcCAaABbBCcCAaABbBCcCAaABbBCcC"  # for 36n40p motor (36 slots, 40 poles)
)


def test_get_winding_teeth_indices_24n22p():
    teeth_indices = get_winding_teeth_indices(winding_config_letters_24n22p)
    assert teeth_indices == teeth_indices_24n22p


def test_get_winding_teeth_indices_12n14p():
    teeth_indices = get_winding_teeth_indices(winding_config_letters_12n14p)
    assert teeth_indices == teeth_indices_12n14p


def test_get_winding_teeth_indices_36n40p():
    teeth_indices = get_winding_teeth_indices(winding_config_letters_36n40p)
    assert teeth_indices == teeth_indices_36n40p


def test_get_current_slot():
    m1_zero = -0.01
    slot_count = 24
    motor1_pos = -0.534
    current_slot = get_current_slot(motor1_pos, m1_zero, slot_count)
    assert current_slot == 2


def test_is_starting_from_bottom_24n22p():
    teeth_indices_a = teeth_indices_24n22p[0]
    teeth_indices_b = teeth_indices_24n22p[1]
    teeth_indices_c = teeth_indices_24n22p[2]

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
            is_starting_from_bottom(i, winding_config_letters_24n22p, teeth_indices_a)
            is expected
        )

    for i, expected in enumerate(expected_results_a_c):
        assert (
            is_starting_from_bottom(i, winding_config_letters_24n22p, teeth_indices_c)
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
            is_starting_from_bottom(i, winding_config_letters_24n22p, teeth_indices_b)
            is expected
        )


def test_is_starting_from_bottom_12n14p():
    teeth_indices_a = teeth_indices_12n14p[0]
    teeth_indices_b = teeth_indices_12n14p[1]
    teeth_indices_c = teeth_indices_12n14p[2]

    expected_results_a_c = [
        False,  # starts_at = 0
        False,  # starts_at = 1
        False,  # starts_at = 2
        True,  # starts_at = 3
    ]

    for i, expected in enumerate(expected_results_a_c):
        assert (
            is_starting_from_bottom(i, winding_config_letters_12n14p, teeth_indices_a)
            is expected
        )

    for i, expected in enumerate(expected_results_a_c):
        assert (
            is_starting_from_bottom(i, winding_config_letters_12n14p, teeth_indices_c)
            is expected
        )

    expected_results_b = [
        False,  # starts_at = 0
        True,  # starts_at = 1
        False,  # starts_at = 2
        False,  # starts_at = 3
    ]

    for i, expected in enumerate(expected_results_b):
        assert (
            is_starting_from_bottom(i, winding_config_letters_12n14p, teeth_indices_b)
            is expected
        )


def test_is_starting_from_bottom_36n40p():
    teeth_indices_a = teeth_indices_36n40p[0]
    teeth_indices_b = teeth_indices_36n40p[1]
    teeth_indices_c = teeth_indices_36n40p[2]

    expected_results = [
        False,  # starts_at = 0
        False,  # starts_at = 1
        True,  # starts_at = 2
        False,  # starts_at = 3
        False,  # starts_at = 4
        True,  # starts_at = 5
        False,  # starts_at = 6
        False,  # starts_at = 7
        True,  # starts_at = 8
        False,  # starts_at = 9
        False,  # starts_at = 10
        True,  # starts_at = 11
    ]

    for i, expected in enumerate(expected_results):
        assert (
            is_starting_from_bottom(i, winding_config_letters_36n40p, teeth_indices_a)
            is expected
        )

    for i, expected in enumerate(expected_results):
        assert (
            is_starting_from_bottom(i, winding_config_letters_36n40p, teeth_indices_c)
            is expected
        )

    for i, expected in enumerate(expected_results):
        assert (
            is_starting_from_bottom(i, winding_config_letters_36n40p, teeth_indices_b)
            is expected
        )
