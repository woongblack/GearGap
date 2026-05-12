"""
Murlok 26 DPS 스펙 전체 스모크 테스트
결과: backend/data/murlok_smoke_test_results.json

검증 항목:
- 슬롯 수, 총 아이템 수, 분모(total_sample)
- 이상 케이스: 슬롯 누락, count=None, 파싱 실패
- 슬롯당 아이템 수 통계 (평균/최소/최대)
"""
import io, sys, asyncio, json, time
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
from dataclasses import asdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.murlok import MurlokScraper, Slot, ItemPopularity

DPS_SPECS = [
    ("death-knight", "frost"),
    ("death-knight", "unholy"),
    ("demon-hunter", "havoc"),
    ("druid", "balance"),
    ("druid", "feral"),
    ("evoker", "devastation"),
    ("evoker", "augmentation"),
    ("hunter", "beast-mastery"),
    ("hunter", "marksmanship"),
    ("hunter", "survival"),
    ("mage", "arcane"),
    ("mage", "fire"),
    ("mage", "frost"),
    ("monk", "windwalker"),
    ("paladin", "retribution"),
    ("priest", "shadow"),
    ("rogue", "assassination"),
    ("rogue", "outlaw"),
    ("rogue", "subtlety"),
    ("shaman", "elemental"),
    ("shaman", "enhancement"),
    ("warlock", "affliction"),
    ("warlock", "demonology"),
    ("warlock", "destruction"),
    ("warrior", "arms"),
    ("warrior", "fury"),
]

EXPECTED_SLOTS = set(Slot) - {Slot.OFF_HAND}  # off_hand은 있을 때만


async def run_smoke_test() -> dict:
    scraper = MurlokScraper()
    results = []
    anomalies = []
    all_slot_item_counts: dict[str, list[int]] = defaultdict(list)

    print(f"{'스펙':<32} {'sample':>7} {'슬롯':>5} {'아이템':>7} {'none':>5} {'상태':>4}")
    print("-" * 65)

    for i, (cls, spec) in enumerate(DPS_SPECS):
        label = f"{cls}/{spec}"
        spec_result = {
            "class_name": cls,
            "spec_name": spec,
            "status": "ok",
            "total_sample": None,
            "slot_count": 0,
            "item_count": 0,
            "none_count": 0,
            "slots": {},
            "anomalies": [],
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }

        try:
            items: list[ItemPopularity] = await scraper.get_slot_popularity(cls, spec)

            by_slot: dict[str, list[dict]] = defaultdict(list)
            none_count = 0
            sample = items[0].total_sample if items else None

            for it in items:
                by_slot[it.slot.value].append({
                    "item_id": it.item_id,
                    "item_name": it.item_name,
                    "count": it.count,
                })
                if it.count is None:
                    none_count += 1

            # 슬롯별 아이템 수 통계 수집
            for slot_name, slot_items in by_slot.items():
                all_slot_item_counts[slot_name].append(len(slot_items))

            # 이상 탐지
            spec_anomalies = []
            if sample != 50:
                spec_anomalies.append(f"total_sample={sample} (50 아님)")
            if len(by_slot) < 10:
                spec_anomalies.append(f"슬롯 수 {len(by_slot)} < 10")
            if none_count > 0:
                spec_anomalies.append(f"count=None {none_count}개")

            status = "⚠️" if spec_anomalies else "✅"
            spec_result.update({
                "total_sample": sample,
                "slot_count": len(by_slot),
                "item_count": len(items),
                "none_count": none_count,
                "slots": {k: v for k, v in sorted(by_slot.items())},
                "anomalies": spec_anomalies,
                "status": "anomaly" if spec_anomalies else "ok",
            })

            if spec_anomalies:
                anomalies.append((label, spec_anomalies))

            print(f"{label:<32} {str(sample):>7} {len(by_slot):>5} {len(items):>7} {none_count:>5} {status:>4}")

        except Exception as e:
            spec_result["status"] = "error"
            spec_result["anomalies"] = [str(e)]
            anomalies.append((label, [str(e)]))
            print(f"{label:<32} {'ERROR':>7} {'':>5} {'':>7} {'':>5} ❌")

        results.append(spec_result)

        if i < len(DPS_SPECS) - 1:
            time.sleep(10)

    # 슬롯별 통계
    slot_stats = {}
    for slot_name, counts in sorted(all_slot_item_counts.items()):
        slot_stats[slot_name] = {
            "avg": round(sum(counts) / len(counts), 1),
            "min": min(counts),
            "max": max(counts),
            "spec_count": len(counts),
        }

    summary = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "total_specs": len(DPS_SPECS),
        "ok_count": sum(1 for r in results if r["status"] == "ok"),
        "anomaly_count": len(anomalies),
        "slot_stats": slot_stats,
        "specs": results,
    }

    # 통계 출력
    print(f"\n{'='*65}")
    print(f"총 {len(DPS_SPECS)}개 스펙 | OK: {summary['ok_count']} | 이상: {summary['anomaly_count']}")

    print("\n[슬롯별 아이템 수 통계 (전 스펙 평균)]")
    for slot_name, stat in slot_stats.items():
        bar = "█" * int(stat["avg"])
        print(f"  {slot_name:<14} avg={stat['avg']:>4}  min={stat['min']}  max={stat['max']}  {bar}")

    if anomalies:
        print("\n[⚠️ 이상 케이스]")
        for label, issues in anomalies:
            print(f"  {label}: {', '.join(issues)}")
    else:
        print("\n✅ 이상 없음")

    return summary


async def main() -> None:
    print("=== Murlok 26 DPS 스펙 스모크 테스트 ===")
    print(f"스펙 간 10초 딜레이 적용 (총 약 {len(DPS_SPECS) * 10 // 60}분 소요 예상)\n")

    summary = await run_smoke_test()

    out_path = Path(__file__).parent.parent / "data" / "murlok_smoke_test_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n결과 저장: {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
