# Configuration for the winding machine

# end gear: motor gear ratio
m2_gear_ratio = 50 / 51

# If True, motor rotates clockwise
rotating_directions = [True, True, False, False, True]

# wind order for 24n22p motor(motor 2 clockwise=True)
wind_order_a = [0, 1, 0, 1, 1, 0, 1, 0]
# t(+0) d(+180) t(+180) T(+0) - d(+180) t(+180) d(+180) t(+180)
wind_order_b = [1, 0, 1, 0, 0, 1, 0, 1]
# d(+180) t(+180) d(+180) t(+180) - D(+180) t(+180) d(+180) t(+180) T(+0)
wind_order_c = [0, 1, 0, 1, 1, 0, 1, 0]

wind_orders = [wind_order_a, wind_order_b, wind_order_c]

slot_indices_a = [0, 1, 2, 3, 12, 13, 14, 15]
slot_indices_b = [4, 5, 6, 7, 16, 17, 18, 19]
slot_indices_c = [8, 9, 10, 11, 20, 21, 22, 23]

slot_indices = [slot_indices_a, slot_indices_b, slot_indices_c]
