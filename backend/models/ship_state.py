from dataclasses import dataclass
from models.battery import Battery


@dataclass
class ShipState:
    production: float
    storage_ratio: float
    consumption: float
    battery: Battery