from src.winding import Wind


turns = 5  # Use a smaller number for testing
config_file_24n22p = "tests/dev-24n22p-settings.yml"
config_file_12n14p = "tests/dev-12n14p-settings.yml"
config_file_36n40p = "tests/dev-36n40p-settings.yml"


def test_winding_wire0_24n22p():
    wind = Wind(config_file_24n22p, True, turns=turns)
    wind.wind(0)


def test_winding_wire1_24n22p():
    wind = Wind(config_file_24n22p, True, turns=turns)
    wind.wind(1)


def test_winding_wire2_24n22p():
    wind = Wind(config_file_24n22p, True, turns=turns)
    wind.wind(2)


def test_continuous_winding_24n22p():
    wind = Wind(config_file_24n22p, True, turns=turns)
    wind.continuous_winding()


def test_winding_wire0_12n14p():
    wind = Wind(config_file_12n14p, True, turns=turns)
    wind.wind(0)


def test_winding_wire1_12n14p():
    wind = Wind(config_file_12n14p, True, turns=turns)
    wind.wind(1)


def test_winding_wire2_12n14p():
    wind = Wind(config_file_12n14p, True, turns=turns)
    wind.wind(2)


def test_continuous_winding_12n14p():
    wind = Wind(config_file_12n14p, True, turns=turns)
    wind.continuous_winding()


def test_winding_wire0_36n40p():
    wind = Wind(config_file_36n40p, True, turns=turns)
    wind.wind(0)


def test_winding_wire1_36n40p():
    wind = Wind(config_file_36n40p, True, turns=turns)
    wind.wind(1)


def test_winding_wire2_36n40p():
    wind = Wind(config_file_36n40p, True, turns=turns)
    wind.wind(2)


def test_continuous_winding_36n40p():
    wind = Wind(config_file_36n40p, True, turns=turns)
    wind.continuous_winding()
