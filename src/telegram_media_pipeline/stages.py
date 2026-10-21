import math
from typing import List, Optional
from .models import ChunkInfo, MediaItem, MediaType


class PipelineStage:
    async def process(self, item: MediaItem) -> MediaItem:
        raise NotImplementedError


class ValidationStage(PipelineStage):
    """Validates file sizes and allowed media extensions."""

    def __init__(self, max_size_bytes: int = 50 * 1024 * 1024, allowed_types: Optional[List[MediaType]] = None):
        self.max_size_bytes = max_size_bytes
        self.allowed_types = allowed_types

    async def process(self, item: MediaItem) -> MediaItem:
        if self.allowed_types and item.media_type not in self.allowed_types:
            raise ValueError(f"Media type '{item.media_type.value}' is not supported in this pipeline.")

        if item.size_bytes > self.max_size_bytes:
            raise ValueError(
                f"File size {item.size_bytes} exceeds configured limit {self.max_size_bytes} bytes."
            )

        return item


class MetadataStage(PipelineStage):
    """Enriches media item with format, extension, and tag information."""

    async def process(self, item: MediaItem) -> MediaItem:
        ext = item.file_name.rsplit(".", 1)[-1].lower() if "." in item.file_name else ""
        item.metadata["extension"] = ext
        item.metadata["size_mb"] = round(item.size_bytes / (1024 * 1024), 2)
        return item


class ChunkingStage(PipelineStage):
    """Splits large media files into contiguous chunk windows for bot upload limits."""

    def __init__(self, max_chunk_size: int = 20 * 1024 * 1024):
        self.max_chunk_size = max_chunk_size

    def calculate_chunks(self, total_size: int) -> List[ChunkInfo]:
        if total_size < 0:
            raise ValueError("File size cannot be negative")
        if total_size <= self.max_chunk_size:
            return [ChunkInfo(chunk_index=0, total_chunks=1, byte_start=0, byte_end=total_size, size_bytes=total_size)]

        total_chunks = math.ceil(total_size / self.max_chunk_size)
        chunks = []
        for i in range(total_chunks):
            start = i * self.max_chunk_size
            end = min(total_size, (i + 1) * self.max_chunk_size)
            chunks.append(
                ChunkInfo(
                    chunk_index=i,
                    total_chunks=total_chunks,
                    byte_start=start,
                    byte_end=end,
                    size_bytes=end - start,
                )
            )
        return chunks

    async def process(self, item: MediaItem) -> MediaItem:
        chunks = self.calculate_chunks(item.size_bytes)
        item.metadata["chunks"] = [c.__dict__ for c in chunks]
        return item
