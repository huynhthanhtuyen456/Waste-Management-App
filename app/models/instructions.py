from odmantic import Model, Reference

from app.models.categories import WasteCategory


class WasteInstruction(Model):
    title: str
    content: str | None = None
    category: WasteCategory = Reference()


class WasteInstructionType(Model):
    type: str
    description: str | None = None
    instructions: list[WasteInstruction]
