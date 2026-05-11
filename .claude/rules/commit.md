# 커밋 컨벤션

## 형식

```
<type>(<scope>): <description>
```

## 타입

| type | 용도 |
|------|------|
| `feat` | 새로운 기능 |
| `fix` | 버그 수정 |
| `refactor` | 기능 변경 없는 코드 개선 |
| `chore` | 설정, 의존성, 인프라 |
| `docs` | 문서 변경 |
| `test` | 테스트 추가/수정 |
| `style` | 포맷/공백 (로직 변경 없음) |

## 스코프 예시

`frontend`, `backend`, `db`, `infra`, `api`, `ui`

## 규칙

- 설명은 72자 이하, 명령형, 소문자, 마침표 없음
- `git add -A` / `git add .` 사용 금지 → 파일 명시
- secrets 포함 파일 커밋 금지 (`.env`, credentials)
- 논리적으로 독립된 변경은 분리 커밋

## 예시

```
feat(backend): add character cache endpoint with 10min TTL
fix(frontend): correct weight slider range to 0.5-2.0
chore(infra): add Cloud Run GitHub Actions workflow
feat(db): add SIMULATION_RESULTS table with is_latest flag
```
