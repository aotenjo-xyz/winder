from src.utils import (
    get_winding_teeth_indices,
    get_current_teeth,
    is_starting_from_bottom,
    is_skipping,
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


def test_is_skipping_24n22p():
    assert not is_skipping(winding_config_letters_24n22p, 0)
    assert not is_skipping(winding_config_letters_24n22p, 1)
    assert not is_skipping(winding_config_letters_24n22p, 2)
    assert not is_skipping(winding_config_letters_24n22p, 3)
    assert not is_skipping(winding_config_letters_24n22p, 4)
    assert not is_skipping(winding_config_letters_24n22p, 5)
    assert not is_skipping(winding_config_letters_24n22p, 6)
    assert not is_skipping(winding_config_letters_24n22p, 7)
    assert not is_skipping(winding_config_letters_24n22p, 8)
    assert not is_skipping(winding_config_letters_24n22p, 9)
    assert not is_skipping(winding_config_letters_24n22p, 10)
    assert not is_skipping(winding_config_letters_24n22p, 11)
    assert is_skipping(winding_config_letters_24n22p, 12)
    assert not is_skipping(winding_config_letters_24n22p, 13)
    assert not is_skipping(winding_config_letters_24n22p, 14)
    assert not is_skipping(winding_config_letters_24n22p, 15)
    assert is_skipping(winding_config_letters_24n22p, 16)
    assert not is_skipping(winding_config_letters_24n22p, 17)
    assert not is_skipping(winding_config_letters_24n22p, 18)
    assert not is_skipping(winding_config_letters_24n22p, 19)
    assert is_skipping(winding_config_letters_24n22p, 20)
    assert not is_skipping(winding_config_letters_24n22p, 21)
    assert not is_skipping(winding_config_letters_24n22p, 22)
    assert not is_skipping(winding_config_letters_24n22p, 23)


def test_is_skipping_12n14p():
    assert not is_skipping(winding_config_letters_12n14p, 0)
    assert not is_skipping(winding_config_letters_12n14p, 1)
    assert not is_skipping(winding_config_letters_12n14p, 2)
    assert not is_skipping(winding_config_letters_12n14p, 3)
    assert not is_skipping(winding_config_letters_12n14p, 4)
    assert not is_skipping(winding_config_letters_12n14p, 5)
    assert is_skipping(winding_config_letters_12n14p, 6)
    assert not is_skipping(winding_config_letters_12n14p, 7)
    assert is_skipping(winding_config_letters_12n14p, 8)
    assert not is_skipping(winding_config_letters_12n14p, 9)
    assert is_skipping(winding_config_letters_12n14p, 10)
    assert not is_skipping(winding_config_letters_12n14p, 11)


def test_is_skipping_36n40p():
    assert not is_skipping(winding_config_letters_36n40p, 0)
    assert not is_skipping(winding_config_letters_36n40p, 1)
    assert not is_skipping(winding_config_letters_36n40p, 2)
    assert not is_skipping(winding_config_letters_36n40p, 3)
    assert not is_skipping(winding_config_letters_36n40p, 4)
    assert not is_skipping(winding_config_letters_36n40p, 5)
    assert not is_skipping(winding_config_letters_36n40p, 6)
    assert not is_skipping(winding_config_letters_36n40p, 7)
    assert not is_skipping(winding_config_letters_36n40p, 8)
    assert is_skipping(winding_config_letters_36n40p, 9)
    assert not is_skipping(winding_config_letters_36n40p, 10)
    assert not is_skipping(winding_config_letters_36n40p, 11)
    assert is_skipping(winding_config_letters_36n40p, 12)
    assert not is_skipping(winding_config_letters_36n40p, 13)
    assert not is_skipping(winding_config_letters_36n40p, 14)
    assert is_skipping(winding_config_letters_36n40p, 15)
    assert not is_skipping(winding_config_letters_36n40p, 16)
    assert not is_skipping(winding_config_letters_36n40p, 17)
    assert is_skipping(winding_config_letters_36n40p, 18)
    assert not is_skipping(winding_config_letters_36n40p, 19)
    assert not is_skipping(winding_config_letters_36n40p, 20)
    assert is_skipping(winding_config_letters_36n40p, 21)
    assert not is_skipping(winding_config_letters_36n40p, 22)
    assert not is_skipping(winding_config_letters_36n40p, 23)
    assert is_skipping(winding_config_letters_36n40p, 24)
    assert not is_skipping(winding_config_letters_36n40p, 25)
    assert not is_skipping(winding_config_letters_36n40p, 26)
    assert is_skipping(winding_config_letters_36n40p, 27)
    assert not is_skipping(winding_config_letters_36n40p, 28)
    assert not is_skipping(winding_config_letters_36n40p, 29)
    assert is_skipping(winding_config_letters_36n40p, 30)
    assert not is_skipping(winding_config_letters_36n40p, 31)
    assert not is_skipping(winding_config_letters_36n40p, 32)
    assert is_skipping(winding_config_letters_36n40p, 33)
    assert not is_skipping(winding_config_letters_36n40p, 34)
    assert not is_skipping(winding_config_letters_36n40p, 35)


def test_get_winding_teeth_indices_24n22p():
    teeth_indices = get_winding_teeth_indices(winding_config_letters_24n22p)
    assert teeth_indices == teeth_indices_24n22p


def test_get_winding_teeth_indices_12n14p():
    teeth_indices = get_winding_teeth_indices(winding_config_letters_12n14p)
    assert teeth_indices == teeth_indices_12n14p


def test_get_winding_teeth_indices_36n40p():
    teeth_indices = get_winding_teeth_indices(winding_config_letters_36n40p)
    assert teeth_indices == teeth_indices_36n40p


def test_get_current_teeth():
    m1_zero = -0.01
    teeth_count = 24
    motor1_pos = -0.534
    current_teeth = get_current_teeth(motor1_pos, m1_zero, teeth_count)
    assert current_teeth == 2


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
