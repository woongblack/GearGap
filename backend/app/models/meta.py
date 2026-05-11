from sqlmodel import Field, SQLModel


class WowClass(SQLModel, table=True):
    __tablename__ = "classes"

    id: int = Field(primary_key=True)
    name: str           # e.g. "Warlock"
    name_kr: str        # e.g. "흑마법사"


class Spec(SQLModel, table=True):
    __tablename__ = "specs"

    id: int = Field(primary_key=True)
    class_id: int = Field(foreign_key="classes.id")
    name: str           # e.g. "Destruction"
    name_kr: str        # e.g. "파멸"
    role: str           # "DPS" | "HEALER" | "TANK"
