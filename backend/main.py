from services.serial_manager import SerialManager
from services.allocation_engine import (
    AllocationEngine,
    sectors_to_leds
)
from services.grid_status_service import (
    evaluate_grid_status,
    rgb_from_status,
    buzzer_state
)

from models.battery import Battery
from models.sector import Sector

from database.repositories import Repository
from config import settings

import time

serial_manager = SerialManager("COM5")

allocation_engine = AllocationEngine()

repository = Repository()

battery = Battery(
    capacity=settings.BATTERY_CAPACITY,
    level=0,
)

sectors = [
    Sector(
        name=name,
        criticality=config["criticality"],
        priority=config["priority"],
        min_consumption=config["minimum"],
        max_consumption=config["maximum"],
    )
    for name, config
    in settings.SECTOR_CONFIG.items()
]

while True:

    inputs = serial_manager.read_inputs()

    if inputs is None:
        time.sleep(0.1)
        continue

    # -----------------------------
    # Energy allocation
    # -----------------------------

    sectors = allocation_engine.allocate(
        sectors=sectors,
        battery=battery,
        production_ratio=inputs["production_ratio"],
        storage_ratio=inputs["storage_ratio"],
        max_production=settings.MAX_PRODUCTION,
    )

    # -----------------------------
    # Current production
    # -----------------------------

    production = (
        settings.MAX_PRODUCTION
        * inputs["production_ratio"]
        / 100
    )

    # -----------------------------
    # Grid state
    # -----------------------------

    status = evaluate_grid_status(
        sectors,
        battery,
        production
    )

    r, g, b = rgb_from_status(
        status
    )

    buzzer = buzzer_state(
        status
    )

    # -----------------------------
    # Sector LEDs
    # -----------------------------

    leds = sectors_to_leds(
        sectors
    )

    # -----------------------------
    # Send to Arduino
    # -----------------------------

    serial_manager.send_outputs(
        sector_intensities=leds,
        rgb_r=r,
        rgb_g=g,
        rgb_b=b,
        buzzer=buzzer
    )

    # -----------------------------
    # Database
    # -----------------------------

    repository.save_state(
        production_ratio=inputs["production_ratio"],
        storage_ratio=inputs["storage_ratio"],
        battery_level=battery.level,
        sectors=sectors,
    )

    time.sleep(0.5)