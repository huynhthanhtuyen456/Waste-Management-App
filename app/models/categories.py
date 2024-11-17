from odmantic import Model

from app.models.challenges import Challenge


class WasteCategory(Model):
    name: str
    description: str
    challenges: list[Challenge] | None = None
