from config import settings


class AllocationEngine:

    def allocate(
        self,
        sectors,
        battery,
        production_ratio,
        storage_ratio,
        max_production,
    ):

        # ----------------------------------------------
        # reset allocations
        # ----------------------------------------------

        for sector in sectors:
            sector.allocated = 0

        # ----------------------------------------------
        # production
        # ----------------------------------------------

        production = (
            max_production *
            production_ratio
            / 100
        )

        effective_storage = (
            production *
            storage_ratio
            / 100 *
            settings.MAX_STORAGE_RATIO
        )

        available_energy = (
            production -
            effective_storage
        )

        battery.charge(
            effective_storage
        )

        # ----------------------------------------------
        # sort sectors
        # ----------------------------------------------

        sectors.sort(
            key=lambda s: (
                s.criticality,
                s.priority
            )
        )

        # ----------------------------------------------
        # calculate minimums
        # ----------------------------------------------

        total_minimum = sum(
            sector.min_consumption
            for sector in sectors
        )

        # ==============================================
        # CRISIS MODE
        # Not enough energy for all minimums
        # ==============================================

        if available_energy < total_minimum:

            remaining = available_energy

            for sector in sectors:

                allocation = min(
                    remaining,
                    sector.min_consumption
                )

                sector.allocated = (
                    allocation
                )

                remaining -= allocation

                if remaining <= 0:
                    break

            # ------------------------------------------
            # battery support for criticality 1
            # sectors
            # ------------------------------------------

            for sector in sectors:

                if sector.criticality != 1:
                    continue

                deficit = (
                    sector.min_consumption
                    - sector.allocated
                )

                if deficit <= 0:
                    continue

                restored = (
                    battery.discharge(
                        deficit
                    )
                )

                sector.allocated += (
                    restored
                )

            return sectors

        # ==============================================
        # NORMAL MODE
        # Every sector gets its minimum
        # ==============================================

        remaining = available_energy

        for sector in sectors:

            sector.allocated = (
                sector.min_consumption
            )

            remaining -= (
                sector.min_consumption
            )

        # ==============================================
        # distribute surplus according
        # to criticality + priority
        # ==============================================

        for sector in sectors:

            extra_capacity = (

                sector.max_consumption
                - sector.min_consumption

            )

            if extra_capacity <= 0:
                continue

            extra = min(
                remaining,
                extra_capacity
            )

            sector.allocated += extra

            remaining -= extra

            if remaining <= 0:
                break

        # ==============================================
        # charge battery with unused energy
        # ==============================================

        if remaining > 0:

            battery.charge(
                remaining
            )

        return sectors


def sectors_to_leds(
    sectors
):
    return {

        sector.name:
        sector.intensity

        for sector in sectors
    }