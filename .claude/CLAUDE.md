# Product Manager Harness

PM 업무의 로드맵→PRD→유저스토리→스프린트→회고를 에이전트 팀이 협업하여 생성하는 하네스.

## 구조

```
.claude/
├── agents/
│   ├── strategist.md          — 전략가 (비전, 로드맵, 우선순위 프레임워크)
│   ├── prd-writer.md          — PRD 작성자 (제품 요구사항 정의서)
│   ├── story-writer.md        — 유저스토리 작성자 (AC, 스토리맵, 포인트)
│   ├── sprint-planner.md      — 스프린트 플래너 (계획, 용량, 리스크)
│   └── pm-reviewer.md         — PM 검증자 (정합성, 실행 가능성 검토)
├── skills/
│   ├── product-manager/
│       └── skill.md           — 오케스트레이터 (팀 조율, 워크플로우, 에러핸들링)
│   ├── rice-prioritizer/
│   │   └── skill.md           — RICE 우선순위 (스코어 공식, ICE/MoSCoW 보완)
│   └── story-point-estimator/
│       └── skill.md           — 스토리 포인트 (피보나치, 벨로시티, 분해 기준)
└── CLAUDE.md                  — 이 파일
```

## 사용법

`/product-manager` 스킬을 트리거하거나, "PRD 작성해줘" 같은 자연어로 요청한다.

## 산출물

모든 산출물은 `_workspace/` 디렉토리에 저장된다:
- `00_input.md` — 사용자 입력 정리
- `01_product_roadmap.md` — 제품 로드맵
- `02_prd.md` — 제품 요구사항 정의서
- `03_user_stories.md` — 유저스토리 목록
- `04_sprint_plan.md` — 스프린트 계획
- `05_review_report.md` — PM 검증 보고서


---

# Fullstack Web App Harness

풀스택 웹앱의 요구사항→설계→프론트엔드→백엔드→테스트→배포를 에이전트 팀이 협업하여 개발하는 하네스.

## 구조

```
.claude/
├── agents/
│   ├── architect.md             — 시스템 설계 (요구사항 분석, 아키텍처, DB 모델링, API 설계)
│   ├── frontend-dev.md          — 프론트엔드 개발 (React/Next.js, UI 컴포넌트, 상태관리)
│   ├── backend-dev.md           — 백엔드 개발 (API 구현, DB, 인증, 비즈니스 로직)
│   ├── qa-engineer.md           — QA 엔지니어 (테스트 전략, 단위/통합/E2E 테스트)
│   └── devops-engineer.md       — DevOps 엔지니어 (CI/CD, 인프라, 배포, 모니터링)
├── skills/
│   ├── fullstack-webapp/
│   │   └── skill.md             — 오케스트레이터 (팀 조율, 워크플로우, 에러핸들링)
│   ├── component-patterns/
│   │   └── skill.md             — 프론트엔드 확장 (React 패턴, 상태관리, 폴더 구조)
│   └── api-security-checklist/
│       └── skill.md             — 백엔드 확장 (OWASP Top 10, 인증/인가, 보안 헤더)
└── CLAUDE.md                    — 이 파일
```

## 사용법

`/fullstack-webapp` 스킬을 트리거하거나, "웹앱 만들어줘" 같은 자연어로 요청한다.

## 산출물

모든 산출물은 프로젝트 루트에 직접 생성된다:
- `_workspace/00_input.md` — 사용자 입력 정리
- `_workspace/01_architecture.md` — 아키텍처 설계 문서
- `_workspace/02_api_spec.md` — API 명세
- `_workspace/03_db_schema.md` — DB 스키마
- `_workspace/04_test_plan.md` — 테스트 계획
- `_workspace/05_deploy_guide.md` — 배포 가이드
- `_workspace/06_review_report.md` — 리뷰 보고서
- `src/` — 소스 코드 (프론트엔드 + 백엔드)


---

# Test Automation Harness

테스트 자동화 전략 수립부터 테스트 작성, CI 통합, 커버리지 분석까지 에이전트 팀이 협업하는 하네스.

## 구조

```
.claude/
├── agents/
│   ├── test-strategist.md      — 테스트 전략 (피라미드, 범위, 도구 선정)
│   ├── unit-tester.md          — 단위 테스트 (모킹, 어서션, 경계값)
│   ├── integration-tester.md   — 통합 테스트 (API, DB, 외부 서비스)
│   ├── coverage-analyst.md     — 커버리지 분석 (갭 식별, 리스크 기반 우선순위)
│   └── qa-reviewer.md          — 교차 검증 (전략↔테스트↔커버리지 정합성)
├── skills/
│   ├── test-automation/
│   │   └── skill.md              — 오케스트레이터 (팀 조율, 워크플로우, 에러핸들링)
│   ├── test-design-patterns/
│   │   └── skill.md              — 체계적 테스트 설계 패턴 가이드
│   └── mocking-strategy/
│       └── skill.md              — 테스트 더블 선택 및 모킹 전략 가이드
└── CLAUDE.md                   — 이 파일
```

## 사용법

`/test-automation` 스킬을 트리거하거나, "테스트 자동화해줘" 같은 자연어로 요청한다.

## 산출물

모든 산출물은 `_workspace/` 디렉토리에 저장된다:
- `00_input.md` — 사용자 입력 정리
- `01_test_strategy.md` — 테스트 전략서
- `02_unit_tests.md` — 단위 테스트 코드 및 가이드
- `03_integration_tests.md` — 통합 테스트 코드 및 가이드
- `04_coverage_report.md` — 커버리지 분석 보고서
- `05_review_report.md` — 최종 리뷰 보고서


---

# Mermaid 다이어그램 작성 규칙

`docs/` 내 마크다운에 Mermaid 다이어그램을 작성할 때 **반드시** 아래 규칙을 지켜야 한다.
위반 시 브라우저에서 Lexical/Parse error가 발생하여 다이어그램이 렌더링되지 않는다.

## quadrantChart 규칙

| 규칙 | 올바른 예 | 잘못된 예 |
|------|----------|----------|
| 축 레이블에 **영문 필수** (순수 한글 금지) | `x-axis Low --> High` | `x-axis 저접근성 --> 고접근성` |
| 축 레이블 **2단어 이하** | `x-axis Early Stage --> Mature` | `x-axis 서울 접근성 낮음 --> 서울 접근성 높음` |
| 축 레이블에 **따옴표 금지** | `x-axis Low --> High` | `x-axis "Low" --> "High"` |
| 포인트 이름에 **한글 가능하지만 영문 권장** | `Centrifuge: [0.3, 0.5]` | — |

## 노드·라벨 규칙

| 규칙 | 올바른 예 | 잘못된 예 |
|------|----------|----------|
| 노드 텍스트에 괄호 → **따옴표로 감싸기** | `A["MOR (Record)"]` | `A[MOR (Record)]` |
| 엣지 라벨에 괄호 → **따옴표로 감싸기** | `-->|"할인 (50%)"|` | `-->|할인 (50%)|` |
| 노드 텍스트에 `@` 등 특수문자 → **따옴표** | `VPA["user@bank"]` | `VPA[user@bank]` |
| subgraph 이름에 특수문자 → **따옴표** | `subgraph "PIX (결제)"` | `subgraph PIX (결제)` |

## 일반 규칙

- 모든 다이어그램은 유효한 타입으로 시작: `graph`, `flowchart`, `sequenceDiagram`, `quadrantChart` 등
- 노드 정의에서 대괄호`[]`와 괄호`()`는 반드시 닫기
- `docs/` 수정 후 `pytest tests/test_mermaid.py -v`로 검증 권장
