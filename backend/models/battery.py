from dataclasses import dataclass


@dataclass
class Battery:
    capacity: float
    level: float = 50

    def charge(self, amount: float):
        self.level = min(
            self.capacity,
            self.level + amount
        )

    def discharge(self, amount: float):
        provided = min(
            amount,
            self.level
        )

        self.level -= provided

        return provided

    @property
    def percentage(self):
        return (self.level / self.capacity) * 100

    @property
    def state_code(self):
        """
        Battery state sent to Arduino.
        """

        if self.percentage < 20:
            return 0

        if self.percentage < 50:
            return 1

        if self.percentage < 90:
            return 2

        return 3