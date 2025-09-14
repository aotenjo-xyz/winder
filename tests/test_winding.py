from src.winding import Wind


turns_per_slot = 5  # Use a smaller number for testing
config_file = "settings.yml"


def test_winding_wire0():
    wind = Wind(config_file, True, turns_per_slot=turns_per_slot)
    wind.wind(0)


def test_winding_wire1():
    wind = Wind(config_file, True, turns_per_slot=turns_per_slot)
    wind.wind(1)


def test_winding_wire2():
    wind = Wind(config_file, True, turns_per_slot=turns_per_slot)
    wind.wind(2)


def test_continuous_winding():
    wind = Wind(config_file, True, turns_per_slot=turns_per_slot)
    wind.continuous_winding()
