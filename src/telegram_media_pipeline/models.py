from dataclasses import dataclass, field
import enum
import time
from typing import Any, Dict, List, Optional


class MediaType(str, enum.Enum):
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    PHOTO = "PHOTO"
    DOCUMENT = "DOCUMENT"


@dataclass
class MediaItem:
    file_id: str
    file_name: str
    size_bytes: int
    media_type: MediaType
    file_path: Optional[str] = None
    mime_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChunkInfo:
    chunk_index: int
    total_chunks: int
    byte_start: int
    byte_end: int
    size_bytes: int


@dataclass
class PipelineResult:
    item: MediaItem
    is_success: bool
    processed_at: float
    chunks: List[ChunkInfo] = field(default_factory=list)
    error_message: Optional[str] = None
