from src.winding import Wind


turns = 5  # Use a smaller number for testing
config_file = "dev-settings.yml"


def test_winding_wire0():
    wind = Wind(config_file, True, turns=turns)
    wind.wind(0)


def test_winding_wire1():
    wind = Wind(config_file, True, turns=turns)
    wind.wind(1)


def test_winding_wire2():
    wind = Wind(config_file, True, turns=turns)
    wind.wind(2)


def test_continuous_winding():
    wind = Wind(config_file, True, turns=turns)
    wind.continuous_winding()
