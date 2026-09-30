from app.sources.base import ContentSource
from app.sources.substack import SubstackSource


def get_content_source(
    source_type: str,
) -> ContentSource:

    if source_type == "substack":
        return SubstackSource()

    raise ValueError(f"Unsupported content source: {source_type}")
