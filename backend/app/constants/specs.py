# DPS 스펙 명단 — GearGap MVP 범위
#
# 검증: 2026-05-13, Murlok.io 26 DPS 스펙 전체 smoke test 통과
# 범위: DPS only (힐러/탱커 Post-MVP)
#
# 새 스펙 추가 절차:
#   1. Murlok URL 슬러그 확인: https://murlok.io/{class}/{spec}/m+
#   2. scripts/smoke_test_murlok.py 에 추가 후 단독 실행 검증
#   3. 이 파일에 알파벳 순으로 추가

# (class_name, spec_name) — Murlok URL 슬러그 기준
DPS_SPECS: list[tuple[str, str]] = [
    ("death-knight", "frost"),
    ("death-knight", "unholy"),
    ("demon-hunter", "havoc"),
    ("druid", "balance"),
    ("druid", "feral"),
    ("evoker", "augmentation"),
    ("evoker", "devastation"),
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
