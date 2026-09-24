from dataclasses import dataclass


@dataclass
class Sector:

    name: str
    priority: int

    criticality: int

    max_consumption: float
    min_consumption: float

    allocated: float = 0

    @property
    def ratio(self):

        if self.max_consumption == 0:
            return 0

        return (
            self.allocated /
            self.max_consumption
        )

    @property
    def intensity(self):

        ratio = max(
            0,
            min(self.ratio, 1)
        )

        return int(
            ratio * 255
        )

    def reset(self):
        self.allocated = 0