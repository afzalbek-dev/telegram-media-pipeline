# 🎬 Telegram Media Pipeline

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)]()

Telegram botlar (aiogram, telethon, pyrogram) uchun media fayllarni (video, audio, rasm, hujjat) qabul qilish, hajmini tekshirish, metama'lumotlarni boyitish, yuklash chegaralariga moslab bo'laklarga ajratish (**Chunking Pipeline**) va bosqichma-bosqich qayta ishlash uchun modulli asinxron konveyer (Pipeline).

---

## 🌟 Imkoniyatlari

- **Bosqichli Konveyer Arxitekturasi (Modular Pipeline):** Yangi qayta ishlash bosqichlarini (watermarking, FFmpeg konvertatsiya, o'lchamni kichraytirish) oson qo'shish.
- **Chegaralarni Tekshirish (ValidationStage):** Telegram bot API cheklovlaridan oshib ketgan fayllarni (masalan, 50MB yoki 2000MB) zudlik bilan ushlab qoladi.
- **Katta Fayllarni Bo'laklash (ChunkingStage):** Katta videolarni Telegram bot chekloviga mos qilib avtomatik segmentlar va bayt intervallariga hisoblaydi.
- **Jonli Progress Callback:** Foydalanuvchiga Telegramda `[25% Tekshirilmoqda...]` ko'rinishida jarayonni ko'rsatib borish.
- **Nol tashqi bog'liqlik:** Sof Python standart kutubxonasida ishlaydi.

---

## 🚀 O'rnatish

```bash
git clone https://github.com/afzalbek-dev/telegram-media-pipeline.git
cd telegram-media-pipeline
pip install .
```

---

## 🛠️ Foydalanish

```python
import asyncio
from telegram_media_pipeline import MediaItem, MediaType, MediaPipeline

async def main():
    pipeline = MediaPipeline()

    item = MediaItem(
        file_id="BAACAgIAAxkBAAE...",
        file_name="kurs_darsi_yuqori_sifat.mp4",
        size_bytes=65 * 1024 * 1024,  # 65 MB fayl
        media_type=MediaType.VIDEO
    )

    def on_progress(stage: str, percent: int):
        print(f"Jarayon: {stage} ({percent}%)")

    result = await pipeline.execute(item, progress_callback=on_progress)

    if result.is_success:
        print("✅ Muvaffaqiyatli yakunlandi!")
        print(f"Kengaytma: {result.item.metadata['extension']}")
        print(f"Hajmi: {result.item.metadata['size_mb']} MB")
        print(f"Kerakli bo'laklar soni: {len(result.chunks)}")
        for ch in result.chunks:
            print(f"  Bo'lak {ch.chunk_index + 1}: {ch.byte_start} - {ch.byte_end} baytlar")
    else:
        print("❌ Xatolik:", result.error_message)

asyncio.run(main())
```

---

## 🧪 Testlash

```bash
python3 -m unittest discover tests -v
```

---

## 📄 Litsenziya

MIT License. Muallif: [Afzalbek](https://github.com/afzalbek-dev).
