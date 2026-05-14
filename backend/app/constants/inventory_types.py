from app.services.murlok import Slot

# Raidbots equippable-items.json inventoryType(int) → GearGap Slot
# 검증 기준: 현시즌(TWW S1) 드롭 아이템 453개 + spec_slot_item_popularity 대조
# type 15/26: 사냥꾼 활/총/석궁 → MAIN_HAND (Murlok main_hand 슬롯과 일치 확인)
# type 21/22: 현시즌 0개 — WoW 표준 기반 추정 매핑, 미검증
SLOT_BY_INVENTORY_TYPE: dict[int, Slot] = {
    1:  Slot.HEAD,
    2:  Slot.NECK,
    3:  Slot.SHOULDERS,
    5:  Slot.CHEST,
    6:  Slot.WAIST,
    7:  Slot.LEGS,
    8:  Slot.FEET,
    9:  Slot.WRIST,
    10: Slot.HANDS,
    11: Slot.RINGS,
    12: Slot.TRINKETS,
    13: Slot.MAIN_HAND,   # One-Hand
    14: Slot.OFF_HAND,    # Shield
    15: Slot.MAIN_HAND,   # Ranged (bow) — 사냥꾼 활
    16: Slot.BACK,
    17: Slot.MAIN_HAND,   # Two-Hand (staff 포함)
    20: Slot.CHEST,       # Chest (Robe) — type 5와 통합
    21: Slot.MAIN_HAND,   # Main Hand — 현시즌 미검증, WoW 표준 기반 추정 매핑
    22: Slot.OFF_HAND,    # Off Hand (item) — 현시즌 미검증, WoW 표준 기반 추정 매핑
    23: Slot.OFF_HAND,    # Held In Off-hand (grimoire, tome 등)
    26: Slot.MAIN_HAND,   # Ranged-Right (wand/gun/xbow) — 사냥꾼 총/석궁
}

# SKIP 케이스: inventoryType 키 자체가 없는 아이템 (crafting material 등)
# → map_inventory_type(None) 이 None 반환 → 워커가 스킵

# Raidbots quality(int) → GearGap quality(str)
QUALITY_BY_INT: dict[int, str] = {
    3: "rare",
    4: "epic",
    5: "legendary",
}


def map_inventory_type(inv_type: int | None) -> Slot | None:
    """inventoryType → Slot 변환. None 또는 미정의 type은 None 반환 (워커가 스킵)."""
    if inv_type is None:
        return None
    return SLOT_BY_INVENTORY_TYPE.get(inv_type)


def map_quality(quality_int: int | None) -> str | None:
    """quality int → str 변환. 미정의는 None 반환."""
    if quality_int is None:
        return None
    return QUALITY_BY_INT.get(quality_int)
