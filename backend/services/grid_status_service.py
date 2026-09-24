def evaluate_grid_status(
    sectors,
    battery,
    production
):
    demand = sum(
        sector.max_consumption
        for sector in sectors
    )

    battery_percent = battery.percentage

    # =====================================
    # BLACKOUT
    # No production, no battery
    # =====================================

    if (
        production <= 0
        and battery.level <= 0
    ):
        return "OFF"

    # =====================================
    # BLUE
    # =====================================

    if (
        production > demand
        and battery_percent >= 90
    ):
        return "BLUE"

    # =====================================
    # GREEN
    # =====================================

    if production >= demand:
        return "GREEN"

    # =====================================
    # RED
    # =====================================

    if (
        production < demand
        and battery_percent <= 10
    ):
        return "RED"

    # =====================================
    # PURPLE
    # =====================================

    return "PURPLE"


def rgb_from_status(status):

    colors = {
        "OFF": (0, 0, 0),
        "BLUE": (0, 0, 255),
        "GREEN": (0, 255, 0),
        "PURPLE": (255, 0, 255),
        "RED": (255, 0, 0),
    }

    return colors[status]


def buzzer_state(status):

    return status == "RED"