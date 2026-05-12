"""MurlokScraper 동작 검증"""
import io, sys, asyncio
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.murlok import MurlokScraper, Slot, BLIZZARD_TO_SLOT

async def main() -> None:
    scraper = MurlokScraper()

    print("=== MurlokScraper 검증 ===\n")

    # 1. 기본 동작
    items = await scraper.get_slot_popularity("warlock", "destruction", "mythic-plus")
    print(f"[warlock/destruction] 총 {len(items)}개 아이템")

    # 슬롯별 집계
    from collections import defaultdict
    by_slot: dict[Slot, list] = defaultdict(list)
    for it in items:
        by_slot[it.slot].append(it)

    for slot, slot_items in sorted(by_slot.items()):
        top = slot_items[0]
        print(f"  {slot:<12} {len(slot_items)}개 | 1위: {top.item_name} ({top.count}/{top.total_sample})")

    # 2. 데이터 모델 필드 확인
    print(f"\n[샘플 ItemPopularity]")
    sample = items[0]
    print(f"  class_name   = {sample.class_name}")
    print(f"  spec_name    = {sample.spec_name}")
    print(f"  content_type = {sample.content_type}")
    print(f"  slot         = {sample.slot!r}  (type: {type(sample.slot).__name__})")
    print(f"  item_name    = {sample.item_name}")
    print(f"  item_id      = {sample.item_id}")
    print(f"  count        = {sample.count}")
    print(f"  total_sample = {sample.total_sample}")
    print(f"  scraped_at   = {sample.scraped_at}")

    # 3. __post_init__ 검증 (canary)
    print(f"\n[__post_init__ canary 테스트]")
    try:
        from app.services.murlok import ItemPopularity
        from datetime import datetime, timezone
        bad = ItemPopularity(
            class_name="warlock", spec_name="destruction", content_type="mythic-plus",
            slot=Slot.HEAD, item_name="test", item_id=1,
            count=99, total_sample=50,
            scraped_at=datetime.now(timezone.utc),
        )
        print("  ❌ 검증 실패 — ValueError 발생 안 함")
    except ValueError as e:
        print(f"  ✅ 검증 정상 — {e}")

    # 4. Slot enum + BLIZZARD_TO_SLOT 타입 확인
    print(f"\n[Slot enum 타입 확인]")
    print(f"  Slot.RINGS == 'rings': {Slot.RINGS == 'rings'}")
    print(f"  BLIZZARD_TO_SLOT['FINGER_1']: {BLIZZARD_TO_SLOT['FINGER_1']!r}")
    print(f"  BLIZZARD_TO_SLOT['TRINKET_2']: {BLIZZARD_TO_SLOT['TRINKET_2']!r}")

    # 5. 메타 스펙 비교 (DK unholy)
    print(f"\n[death-knight/unholy 비교]")
    dk_items = await scraper.get_slot_popularity("death-knight", "unholy", "mythic-plus")
    print(f"  총 {len(dk_items)}개 | total_sample={dk_items[0].total_sample if dk_items else '?'}")

    print("\n✅ MurlokScraper 검증 완료")


if __name__ == "__main__":
    asyncio.run(main())
