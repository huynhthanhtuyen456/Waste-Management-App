from odmantic import Model

from app.models.challenges import Challenge
from app.models.wastes import Waste


class WasteCategory(Model):
    name: str
    description: str
    challenges: list[Challenge] | None = None
    wastes: list[Waste] | None = None
