# GearGap Phase 0 결정 + Phase 1 PoC 작업 지시서

> 이 문서는 채팅 로그에서 확정된 결정 사항을 한 곳에 정리한 자기 완결적
> 작업 지시서. 컨텍스트 압축 단계에서 결정이 흐려지지 않도록 모든 핵심
> 결정을 시간순 흐름과 함께 명시함.

---

## 🎯 GearGap 한 줄 정의

WoW 캐릭터의 시즌 BiS 갭을 시각화하고 드롭처를 안내하는 **로드맵 도구**.
"몇 % 강함" 같은 시뮬레이션은 스코프 외 (사용자가 Raidbots 가서 직접).

---

## 📊 데이터 소스 (최종 확정)

| 데이터 | MVP 소스 | Post-MVP 소스 | 상태 |
|---|---|---|---|
| 캐릭터 장비/스펙 | Blizzard API | (동일) | ✅ Phase 0 완료 |
| 시즌/넴드/보너스ID | Raidbots JSON | (동일) | ✅ |
| **슬롯별 BiS 픽률** | **Murlok 크롤링** | WarcraftLogs API 자체집계 | 🔜 Phase 1 |

### 명시적으로 제외된 것

- ❌ DPS 시뮬레이션 / 심크 연동 (스코프 외)
- ❌ Raider.IO runs 자체 집계 — 비메타 스펙(예: 흑마)에서
  500+ 페이지 페이지네이션 필요해서 비효율
- ❌ Archon.gg 크롤링 — RPGLogs ToS 명시적 금지
  ("you will not perform any data-mining, scraping, crawling")
- ❌ bloodmallet — JS 렌더링, API 없음
- ❌ Wowhead BiS 가이드 크롤링 — 라이선스 회색

---

## 🌀 결정 흐름 (참고용 — 또 흔들리지 말 것)

```
bloodmallet ❌
  ↓ JS 렌더링
Raider.IO 슬롯별 Top N 착용률
  ↓ 그런 집계 API 없음 발견
DPS Gain 자체 빼기 (로드맵만)
  ↓
Murlok 발견 → MVP 확정 ✅
  ↓ (Phase 0 막힘) Raider.IO runs 시도 → 비메타 비효율
Archon.gg 후보 → ToS 크롤링 금지 ❌
WarcraftLogs API 후보 → 빌드 집계 직접 없음
  ↓
원래 결정으로 회귀: Murlok MVP ✅✅ (현재)
```

**원칙: 다음에 더 좋아 보이는 사이트 발견해도, 이 결정 끝까지 검증한
후에 바꾼다. PoC 한 번도 안 해보고 데이터 소스 갈아엎지 말 것.**

---

## ⚖️ Murlok 크롤링 정당성 근거

- ❌ 별도 ToS 페이지 없음 (Privacy Policy만)
- ❌ Privacy Policy에 크롤링 금지 조항 없음
- ✅ Murlok 본인도 "Blizzard leaderboards를 daily crawl"이라고
  About 페이지에 공개
- ✅ 운영자(Maxence, @jonhymaxoo) Patreon/X 활성 — 막히면 연락 가능

→ 회색지대이나 도덕적 부담 적음. 운영자 요청 시 즉시 중단 약속.

---

## 🛠️ Murlok 크롤링 운영 원칙 (위반 금지)

1. **시작 전 robots.txt 확인** — `curl https://murlok.io/robots.txt`
2. **User-Agent 명시** — `GearGap/0.1 (+contact@email)` 같이
3. **갱신 주기 1일 1회** — Murlok 본인이 daily니까 그 이상 자주 X
4. **결과 우리 DB에 캐싱** — 사용자 요청은 우리 DB에서만 서빙
   (Murlok에 트래픽 부담 0이 핵심)
5. **운영자 요청 시 즉시 중단** + Phase 1.5(WCL 마이그레이션) 가속

---

## 🏗️ 아키텍처 — 추상화 핵심

Post-MVP에 Murlok → WCL로 갈아끼우려면 **인터페이스 추상화** 필수.

```python
# 추상 인터페이스 — Murlok과 WCL 둘 다 만족해야 함
class BiSDataSource(Protocol):
    async def get_slot_popularity(
        self,
        class_name: str,
        spec_name: str,
        content_type: Literal["mythic-plus", "raid"],
    ) -> dict[Slot, list[ItemPopularity]]:
        ...

# MVP 구현체
class MurlokScraper(BiSDataSource): ...

# Post-MVP 구현체 (당장은 만들지 X)
class WarcraftLogsAggregator(BiSDataSource): ...
```

이게 되면 데이터 소스 갈아끼우는 게 **DI 설정 한 줄**이 됨.

---

## 🚧 Phase 1 PoC 작업 (Murlok HTML 파싱)

### 1단계: robots.txt 확인 (5분)

```bash
curl -A "GearGap-PoC/0.1 (+contact@email)" https://murlok.io/robots.txt
```

- `Disallow:` 항목 확인
- 우리가 노릴 경로(`/{class}/{spec}/m+`)가 막혀있는지 검사

### 2단계: URL 패턴 확정 (5분)

후보 URL들 실제로 fetch해서 어느 게 맞는지:
- `https://murlok.io/destruction/warlock/m+`
- `https://murlok.io/warlock/destruction/m+`
- `https://murlok.io/warlock/destruction`

이전 채팅에서 확인된 작동 URL:
`https://murlok.io/death-knight/unholy/m+` ← class-spec 순서일 가능성

### 3단계: 1개 스펙 HTML 받기 (10분)

```python
import httpx
url = "https://murlok.io/{class}/{spec}/m+"  # 패턴 확정 후
async with httpx.AsyncClient() as c:
    r = await c.get(url, headers={
        "User-Agent": "GearGap-PoC/0.1 (+contact@email)"
    })
    print(r.text[:5000])  # 슬롯 데이터 박혀있는지 육안 확인
```

**예상:** WASM 로더가 있지만 SSR 결과 HTML에 데이터 박혀있음
(이전 fetch에서 "Light Company Guidon — 49명" 같은 텍스트 확인됨).

### 4단계: 파서 PoC (30분~1시간)

BeautifulSoup으로 슬롯별 데이터 추출.

**산출물 스키마:**
```python
@dataclass
class ItemPopularity:
    slot: str           # "head" | "neck" | "shoulder" | ...
    item_name: str      # "Light Company Guidon"
    item_id: int        # Wowhead item ID
    count: int          # 49
    total_sample: int   # 50

# 1 스펙 → list[ItemPopularity]
```

**검증:** 흑마 어둠 1개 스펙에 대해
- 모든 17 슬롯 데이터 추출되는가?
- 트링켓 (2 슬롯) 분리 처리 되는가?
- item_id 추출 가능한가? (Wowhead 링크 href에서)

### 5단계: 26 스펙 확장 (PoC 검증 후)

```python
SPECS = [
    ("death-knight", "unholy"),
    ("death-knight", "frost"),
    ...
]
for cls, spec in SPECS:
    await asyncio.sleep(10)  # rate limit
    data = await scrape(cls, spec)
    await db.upsert(data)
```

26 스펙 × 10초 = 4분. 1일 1회면 충분.

---

## 📋 Phase 1 완료 정의

- [ ] robots.txt 확인 + 경로 허용 검증
- [ ] URL 패턴 확정 (1개 작동하는 URL)
- [ ] 1개 스펙 HTML 파싱 → 17 슬롯 데이터 추출 성공
- [ ] `BiSDataSource` Protocol + `MurlokScraper` 구현
- [ ] 26 스펙 전체 스크립트 작동 (수동 실행)
- [ ] DB 스키마: `spec_slot_popularity` 테이블 정의 + upsert

---

## 🚨 막힐 만한 지점 (사전 경고)

1. **WASM 로더가 데이터 못 받게 막을 수도** — HTML에 데이터가
   진짜 박혀있는지 1단계에서 즉시 확인
2. **트링켓 슬롯 처리** — 1번/2번 트링켓 구분 필요할 수도
3. **무기 슬롯** — 양손/한손/방패 등 카테고리 처리
4. **Cloudflare 차단** — Murlok이 Cloudflare CDN 씀.
   User-Agent 정상이면 보통 OK지만, 403 받으면 알려줄 것

---

## 🎯 Phase 1 끝나면 다음

- Phase 2: Raidbots JSON 파서 + ingestion (아키텍처 이미 그림)
- Phase 3: 데이터 조인 (내 장비 ↔ BiS ↔ 드롭처)
- Phase 4: UI 시안

---

## 🔑 환경 정보 (이미 확보)

- ✅ Blizzard API: Client ID/Secret 발급됨 (KR 리전 캐릭터 조회 OK)
- ✅ Raidbots JSON: 해시값 확보 (이전 발견)
- ⏳ Murlok: PoC 통해서 검증 (이 문서가 그 시작점)