# Okyo's Domain Wiki

결제, 규제, 핀테크 분야의 도메인 지식을 체계적으로 정리하는 개인 위키 사이트.

**Live Site**: https://okyokwon.github.io/studyNresearch/

## 도메인 목록

| 도메인 | 설명 | 대표 제품/기관 |
|--------|------|---------------|
| **PG (Payment Gateway)** | Payment Gateway 구조, 결제 플로우, PG사 비교 | Stripe, Toss Payments, NHN KCP |
| **MOR (Merchant of Record)** | Merchant of Record 모델, PG와의 차이 | Paddle, Lemon Squeezy, FastSpring |
| **가상자산 규제** | 글로벌 규제 프레임워크, 국가별 현황 | FATF, SEC, 금융위원회, MiCA |
| **스테이블코인 규제** | 스테이블코인 유형, 규제 프레임워크, 주요 코인 분석 | USDT, USDC, DAI, MiCA, GENIUS Act |

## 기술 스택

- **사이트 빌더**: [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- **다이어그램**: Mermaid.js
- **호스팅**: GitHub Pages
- **CI/CD**: GitHub Actions (main push 시 자동 배포)

## 로컬 실행

```bash
pip install -r requirements.txt
mkdocs serve
```

http://localhost:8000 에서 확인.

## 새 도메인 추가

```bash
cp -r templates/domain-template/ docs/domains/{new-domain}/
```

`mkdocs.yml`의 `nav` 섹션에 새 도메인 경로를 추가한 뒤 콘텐츠를 작성하고 push하면 자동 배포된다.

상세 절차: [도메인 추가 가이드](https://okyokwon.github.io/studyNresearch/guide/add-domain/)

## 프로젝트 구조

```
├── docs/
│   ├── index.md                 # 홈 페이지
│   ├── domains/
│   │   ├── pg-service/          # PG 서비스 (8개 문서)
│   │   ├── mor-service/         # MOR 서비스 (8개 문서)
│   │   ├── crypto-regulation/    # 가상자산 규제 (8개 문서)
│   │   └── stablecoin-regulation/ # 스테이블코인 규제 (12개 문서)
│   └── guide/                   # 도메인 추가 가이드, AI 템플릿
├── templates/domain-template/   # 새 도메인 추가용 템플릿
├── mkdocs.yml                   # MkDocs 설정
├── requirements.txt             # Python 의존성
└── .github/workflows/deploy.yml # CI/CD 파이프라인
```
