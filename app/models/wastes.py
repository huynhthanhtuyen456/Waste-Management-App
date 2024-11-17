from odmantic import Model


class Waste(Model):
    name: str
    description: str | None = None
