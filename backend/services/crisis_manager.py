from models.sector import Sector


class CrisisManager:

    @staticmethod
    def sort_by_priority(
        sectors: list[Sector]
    ) -> list[Sector]:

        return sorted(sectors, key=lambda s: s.priority)