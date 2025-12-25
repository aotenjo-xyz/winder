import math


def get_motor0_target_winding_position(
    motor2_total_mileage, current_motor2_mileage, m0_wind_range, winding_method, logger
):
    if winding_method == "linear":
        wind_range_distance = abs(m0_wind_range[1] - m0_wind_range[0])
        target_motor0_mileage = (
            wind_range_distance * 2 / motor2_total_mileage * current_motor2_mileage
        )
        if target_motor0_mileage < wind_range_distance:
            motor0_target = m0_wind_range[0] + target_motor0_mileage
        else:
            motor0_target = m0_wind_range[1] - (
                target_motor0_mileage - wind_range_distance
            )
        assert (
            m0_wind_range[0] <= motor0_target <= m0_wind_range[1]
        ), f"motor0_target: {motor0_target} is out of range {m0_wind_range}"
        return motor0_target

    elif winding_method == "ease-out-sine":
        wind_range_distance = abs(m0_wind_range[1] - m0_wind_range[0])
        progress = current_motor2_mileage / motor2_total_mileage
        if progress > 0.5:
            progress = 1 - progress
        progress *= 2  # normalize to [0,1]
        # ease-out-sine
        eased_progress = math.sin((progress * math.pi) / 2)
        motor0_target = wind_range_distance * eased_progress + m0_wind_range[0]
        return motor0_target
