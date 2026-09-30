from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Preference(Base):
    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(primary_key=True)

    genre: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
