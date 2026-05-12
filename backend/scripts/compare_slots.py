"""두 스펙 슬롯별 아이템 수 비교"""
import io, sys, asyncio
from pathlib import Path
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.murlok import MurlokScraper, Slot

SPECS = [("warlock", "destruction"), ("death-knight", "unholy")]

async def main() -> None:
    scraper = MurlokScraper()
    data: dict[str, dict[Slot, int]] = {}
    for cls, spec in SPECS:
        items = await scraper.get_slot_popularity(cls, spec)
        by_slot: dict[Slot, int] = defaultdict(int)
        for it in items:
            by_slot[it.slot] += 1
        data[f"{cls}/{spec}"] = by_slot

    labels = list(data.keys())
    print(f"{'슬롯':<14}  {labels[0]:<22}  {labels[1]:<22}  차이")
    print("-" * 65)
    for slot in Slot:
        a = data[labels[0]].get(slot, 0)
        b = data[labels[1]].get(slot, 0)
        diff = a - b
        flag = "  ← 차이" if diff != 0 else ""
        a_str = str(a) if a else "(없음)"
        b_str = str(b) if b else "(없음)"
        print(f"{slot.value:<14}  {a_str:<22}  {b_str:<22}  {diff:+d}{flag}")

    print()
    for label, by_slot in data.items():
        print(f"{label}: 총 {sum(by_slot.values())}개")

asyncio.run(main())
