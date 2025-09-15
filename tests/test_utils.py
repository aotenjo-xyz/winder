from src.utils import get_wind_orders_and_slot_indices, get_current_slot


def test_get_wind_orders_and_slot_indices():
    winding_config_letters = "AaAabBbBCcCcaAaABbBbcCcC"
    wind_orders, slot_indices = get_wind_orders_and_slot_indices(winding_config_letters)

    # wind order for 24n22p motor(motor 2 clockwise=True)
    wind_order_a = [0, 1, 0, 1, 1, 0, 1, 0]
    # t(+0) d(+180) t(+180) T(+0) - d(+180) t(+180) d(+180) t(+180)
    wind_order_b = [1, 0, 1, 0, 0, 1, 0, 1]
    # d(+180) t(+180) d(+180) t(+180) - D(+180) t(+180) d(+180) t(+180) T(+0)
    wind_order_c = [0, 1, 0, 1, 1, 0, 1, 0]

    assert wind_orders == [wind_order_a, wind_order_b, wind_order_c]

    slot_indices_a = [0, 1, 2, 3, 12, 13, 14, 15]
    slot_indices_b = [4, 5, 6, 7, 16, 17, 18, 19]
    slot_indices_c = [8, 9, 10, 11, 20, 21, 22, 23]

    assert slot_indices == [slot_indices_a, slot_indices_b, slot_indices_c]


def test_get_current_slot():
    m1_zero = -0.01
    slot_count = 24
    motor1_pos = -0.534
    current_slot = get_current_slot(motor1_pos, m1_zero, slot_count)
    assert current_slot == 2
