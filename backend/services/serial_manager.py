import serial


class SerialManager:
    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
    ):
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=1,
        )

    def read_inputs(self) -> dict | None:

        if not self.serial.in_waiting:
            return None

        try:
            line = (
                self.serial.readline()
                .decode("utf-8")
                .strip()
            )

            if not line.startswith("P:"):
                return None

            values = {}

            for part in line.split(";"):
                key, value = part.split(":")
                values[key] = int(value)

            return {
                "production_ratio": values["P"],
                "storage_ratio": values["S"],
            }

        except Exception as e:
            print(f"Serial read error: {e}")
            return None

    def send_outputs(
        self,
        sector_intensities: dict,
        battery_state: int
    ):
        command = (
            f"SUR:{sector_intensities['survival']};"
            f"GRN:{sector_intensities['greenhouse']};"
            f"PRO:{sector_intensities['propulsion']};"
            f"SRV:{sector_intensities['server']};"
            f"LIG:{sector_intensities['lighting']};"
            f"LEI:{sector_intensities['leisure']};"
            f"BAT:{battery_state}\n"
        )

        self.serial.write(
            command.encode("utf-8")
        )