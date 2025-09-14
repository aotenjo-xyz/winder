# Configuration for the winding machine

# end gear: motor gear ratio
m2_gear_ratio = 50 / 50

# If True, motor rotates clockwise
rotating_directions = [True, True, True, False]


def get_wind_orders_and_slot_indices(winding_config: str):
    only_small_letters = winding_config.lower()
    slot_indices_a = []
    slot_indices_b = []
    slot_indices_c = []
    for i, letter in enumerate(only_small_letters):
        if letter == "a":
            slot_indices_a.append(i)
        elif letter == "b":
            slot_indices_b.append(i)
        elif letter == "c":
            slot_indices_c.append(i)
    slot_index_matrix = [slot_indices_a, slot_indices_b, slot_indices_c]

    wind_orders = []
    for slot_indices in slot_index_matrix:
        wind_order = []
        for slot_idx in slot_indices:
            letter = winding_config[slot_idx]
            if letter.isupper():
                wind_order.append(0)
            else:
                wind_order.append(1)
        wind_orders.append(wind_order)
    return wind_orders, slot_index_matrix
