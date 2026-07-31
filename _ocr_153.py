import asyncio
import json
import os
from pathlib import Path
from collections import Counter

async def ocr_image_async(image_path):
    try:
        from winsdk.windows.media.ocr import OcrEngine
        from winsdk.windows.graphics.imaging import BitmapDecoder
        from winsdk.windows.storage import StorageFile
        
        file = await StorageFile.get_file_from_path_async(str(image_path))
        stream = await file.open_async(0)
        decoder = await BitmapDecoder.create_async(stream)
        bitmap = await decoder.get_software_bitmap_async()
        engine = OcrEngine.try_create_from_user_profile_languages()
        if engine is None:
            engine = OcrEngine.try_create_from_languages(['zh-CN', 'en-US'])
        result = await engine.recognize_async(bitmap)
        return result.text.strip()
    except Exception as e:
        return f"[OCR错误: {e}]"

async def main():
    screenshot_dir = Path("F:/人工截图")
    output_dir = Path("F:/个人作品/具身智能")
    output_dir.mkdir(exist_ok=True)
    
    images = sorted(screenshot_dir.glob("*.jpg"), key=lambda x: int(x.stem))
    print(f"共发现 {len(images)} 张截图")
    
    results = {}
    all_text = []
    batch_size = 5
    
    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]
        tasks = [ocr_image_async(img) for img in batch]
        texts = await asyncio.gather(*tasks)
        
        for img, text in zip(batch, texts):
            results[img.name] = text
            all_text.append(text)
            if text and not text.startswith("[OCR错误"):
                print(f"  [{img.name}] {text[:80]}...")
        
        print(f"进度: {min(i+batch_size, len(images))}/{len(images)}")
        await asyncio.sleep(0.5)
    
    output_file = output_dir / "ocr_results_153.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nOCR结果已保存到: {output_file}")
    
    keywords = Counter()
    for text in all_text:
        for word in text.replace('\n', ' ').replace('，', ' ').replace('。', ' ').split():
            if len(word) >= 2:
                keywords[word] += 1
    
    kw_file = output_dir / "ocr_keywords_153.json"
    with open(kw_file, "w", encoding="utf-8") as f:
        json.dump(keywords.most_common(200), f, ensure_ascii=False, indent=2)
    print(f"关键词统计已保存到: {kw_file}")
    print("\nTop 50 关键词:")
    for word, count in keywords.most_common(50):
        print(f"  {word}: {count}")

if __name__ == "__main__":
    asyncio.run(main())
