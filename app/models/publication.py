from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    publication_url: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )

    rss_url: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )

    genre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        default="substack",
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
