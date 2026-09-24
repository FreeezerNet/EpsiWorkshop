class Repository:

    def save_state(
        self,
        production_ratio,
        storage_ratio,
        battery_level,
        sectors,
    ):

        data = {

            "production":
                production_ratio,

            "storage_ratio":
                storage_ratio,

            "battery_level":
                battery_level,

            "survival":
                next(
                    s.allocated
                    for s in sectors
                    if s.name == "survival"
                ),

            "server":
                next(
                    s.allocated
                    for s in sectors
                    if s.name == "server"
                ),

            "greenhouse":
                next(
                    s.allocated
                    for s in sectors
                    if s.name == "greenhouse"
                ),

            "lighting":
                next(
                    s.allocated
                    for s in sectors
                    if s.name == "lighting"
                ),

            "propulsion":
                next(
                    s.allocated
                    for s in sectors
                    if s.name == "propulsion"
                ),

            "leisure":
                next(
                    s.allocated
                    for s in sectors
                    if s.name == "leisure"
                )
        }

        print(data)