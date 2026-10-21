import asyncio
import unittest
from telegram_media_pipeline import MediaItem, MediaType, MediaPipeline, ValidationStage


class TestTelegramMediaPipeline(unittest.TestCase):
    def test_pipeline_execution_and_chunking(self):
        async def run_test():
            pipeline = MediaPipeline()
            # 45 MB file -> should be chunked if chunk size is 20MB
            item = MediaItem(
                file_id="tg_file_001",
                file_name="video_tutorial.mp4",
                size_bytes=45 * 1024 * 1024,
                media_type=MediaType.VIDEO,
            )

            progress_log = []

            def progress_cb(stage, pct):
                progress_log.append((stage, pct))

            result = await pipeline.execute(item, progress_callback=progress_cb)

            self.assertTrue(result.is_success)
            self.assertEqual(len(result.chunks), 3)  # 20MB + 20MB + 5MB
            self.assertEqual(result.item.metadata["extension"], "mp4")
            self.assertEqual(result.item.metadata["size_mb"], 45.0)
            self.assertTrue(any(p[0] == "Completed" for p in progress_log))

        asyncio.run(run_test())

    def test_size_validation_failure(self):
        async def run_test():
            # Pipeline with max 10MB limit
            pipeline = MediaPipeline(stages=[ValidationStage(max_size_bytes=10 * 1024 * 1024)])
            item = MediaItem(
                file_id="tg_oversized",
                file_name="heavy_archive.zip",
                size_bytes=15 * 1024 * 1024,
                media_type=MediaType.DOCUMENT,
            )

            result = await pipeline.execute(item)
            self.assertFalse(result.is_success)
            self.assertIn("exceeds configured limit", result.error_message)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
