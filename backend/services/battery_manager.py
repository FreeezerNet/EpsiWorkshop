from config import settings

class BatteryManager:

    def __init__(
        self,
        capacity=settings.BATTERY_CAPACITY, #kWh
        initial_level=2500,
    ):
        self.capacity = capacity
        self.level = initial_level

    @property
    def percentage(self) -> float:
        return (
            self.level /
            self.capacity
        ) * 100

    def charge(self, amount: float):

        self.level = min(
            self.capacity,
            self.level + amount
        )

    def discharge(self, amount: float):

        available = min(
            amount,
            self.level
        )

        self.level -= available

        return available

    def get_state_code(self): # To Update with actual codes

        percentage = self.percentage

        if percentage < 20:
            return 0      # red

        if percentage < 50:
            return 1      # yellow

        if percentage < 90:
            return 2      # green

        return 3          # blue