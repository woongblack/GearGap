"""Murlok.io — script 태그 + h3 주변 구조 상세 파악"""
import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"}
URL = "https://murlok.io/warlock/destruction/m+"

soup = BeautifulSoup(httpx.get(URL, timeout=15, headers=HEADERS, follow_redirects=True).text, "html.parser")

# 1. script 태그 전체 내용 확인
print("=== Script 태그 내용 ===")
for i, s in enumerate(soup.find_all("script")):
    src = s.get("src", "")
    text = (s.string or "").strip()
    print(f"\n[script {i}] src={src or '(inline)'} | 길이={len(text)}")
    if text:
        print(f"  앞 500자: {text[:500]}")

# 2. h3 Head 주변 siblings 확인
print("\n\n=== h3 슬롯 헤더 주변 구조 (Head) ===")
h3_head = soup.find("h3", string="Head")
if h3_head:
    parent = h3_head.parent
    print(f"부모: <{parent.name}> class={parent.get('class')}")
    print(f"조부모: <{parent.parent.name}> class={parent.parent.get('class')}")
    # 형제 요소들
    siblings = list(parent.children)
    print(f"형제 수: {len(siblings)}")
    for j, sib in enumerate(siblings[:10]):
        if hasattr(sib, 'name') and sib.name:
            print(f"  [{j}] <{sib.name}> class={sib.get('class')} text='{sib.text[:80].strip()}'")

# 3. __NEXT_DATA__ 또는 window.__INITIAL_STATE__ 탐색
print("\n\n=== Next.js / 초기 데이터 탐색 ===")
next_data = soup.find("script", id="__NEXT_DATA__")
if next_data:
    print("__NEXT_DATA__ 발견!")
    data = json.loads(next_data.string)
    # props.pageProps 탐색
    page_props = data.get("props", {}).get("pageProps", {})
    print(f"pageProps keys: {list(page_props.keys())[:10]}")
    print(json.dumps(page_props, ensure_ascii=False, indent=2)[:2000])
else:
    print("__NEXT_DATA__ 없음")
    # 다른 패턴 탐색
    for s in soup.find_all("script"):
        text = s.string or ""
        for pattern in ["window.__", "initialData", "pageData", "gearData", "__APP_"]:
            if pattern in text:
                print(f"'{pattern}' 발견! 앞 400자: {text[:400]}")
                break
