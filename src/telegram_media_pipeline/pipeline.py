import asyncio
import time
from typing import Any, Callable, List, Optional

from .models import ChunkInfo, MediaItem, PipelineResult
from .stages import ChunkingStage, MetadataStage, PipelineStage, ValidationStage


class MediaPipeline:
    """Asynchronous media processing pipeline with configurable stages."""

    def __init__(self, stages: Optional[List[PipelineStage]] = None):
        self.stages: List[PipelineStage] = stages or [
            ValidationStage(),
            MetadataStage(),
            ChunkingStage(),
        ]

    def add_stage(self, stage: PipelineStage) -> "MediaPipeline":
        self.stages.append(stage)
        return self

    async def execute(
        self,
        item: MediaItem,
        progress_callback: Optional[Callable[[str, int], Any]] = None,
    ) -> PipelineResult:
        current_item = item
        total_stages = len(self.stages)

        try:
            for idx, stage in enumerate(self.stages):
                stage_name = stage.__class__.__name__
                if progress_callback:
                    pct = int((idx / total_stages) * 100)
                    progress_callback(stage_name, pct)

                current_item = await stage.process(current_item)

            if progress_callback:
                progress_callback("Completed", 100)

            chunk_dicts = current_item.metadata.get("chunks", [])
            chunks = [ChunkInfo(**c) for c in chunk_dicts]

            return PipelineResult(
                item=current_item,
                is_success=True,
                processed_at=time.time(),
                chunks=chunks,
            )
        except Exception as e:
            return PipelineResult(
                item=current_item,
                is_success=False,
                processed_at=time.time(),
                error_message=str(e),
            )
