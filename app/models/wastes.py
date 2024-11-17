from odmantic import Model, Reference

from app.models.categories import WasteCategory
from app.models.users import User


class Waste(Model):
    name: str
    description: str | None = None
    user: User = Reference()
    category: WasteCategory = Reference()
