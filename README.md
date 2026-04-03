# Okyo's Domain Wiki

각 분야의 도메인 지식을 체계적으로 정리하는 개인 위키 사이트.

**Live Site**: https://okyokwon.github.io/studyNresearch/

## 도메인 목록

### 결제/금융 인프라

| 도메인 | 설명 | 대표 제품/서비스 |
|--------|------|-----------------|
| **PG (Payment Gateway)** | 결제 게이트웨이 구조, 결제 플로우 | Stripe, Toss Payments, NHN KCP |
| **MOR (Merchant of Record)** | 법적 판매자 대행, PG와의 차이 | Paddle, Lemon Squeezy, FastSpring |
| **오픈뱅킹 / BaaS** | 오픈 API 기반 금융 서비스 | Plaid, Unit, 한국 오픈뱅킹 |
| **BNPL (Buy Now Pay Later)** | 후불결제/할부 서비스 모델 | Klarna, Afterpay, 네이버페이 후결제 |
| **임베디드 금융** | 비금융 플랫폼 내 금융 서비스 | Stripe Treasury, Shopify Balance |
| **실시간 결제 인프라** | 즉시 이체 시스템 | FedNow, UPI, PIX |

### 디지털 자산/Web3

| 도메인 | 설명 | 대표 키워드 |
|--------|------|------------|
| **가상자산 규제** | 글로벌 규제 프레임워크 | FATF, SEC, MiCA |
| **스테이블코인 규제** | 스테이블코인 유형, 규제 동향 | USDT, USDC, DAI, GENIUS Act |
| **CBDC** | 중앙은행 디지털화폐 | 디지털 원화, e-CNY, Digital Euro |
| **토큰증권 (STO)** | 증권 토큰화 | Securitize, Polymath, 한국 STO |
| **DeFi 프로토콜** | 탈중앙화 금융 | Uniswap, Aave, MakerDAO |

### 규제/컴플라이언스

| 도메인 | 설명 | 대표 솔루션 |
|--------|------|------------|
| **AML/KYC** | 자금세탁 방지, 본인인증 | Chainalysis, Jumio, Sumsub |
| **데이터 규제** | 개인정보 보호 규제 | GDPR, 개인정보보호법, CCPA |
| **레그테크 (RegTech)** | 규제 준수 자동화 | ComplyAdvantage, Chainalysis KYT |

### 비즈니스 모델

| 도메인 | 설명 | 대표 사례 |
|--------|------|----------|
| **SaaS 비즈니스 모델** | 가격 전략, SaaS 지표, GTM | Notion, Figma, Slack |
| **플랫폼 이코노미** | 양면시장, 네트워크 효과 | 배달의민족, Uber, Airbnb |

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
│   ├── index.md                   # 홈 페이지
│   ├── domains/                   # 17개 도메인
│   │   ├── pg-service/            # PG (Payment Gateway)
│   │   ├── mor-service/           # MOR (Merchant of Record)
│   │   ├── open-banking/          # 오픈뱅킹 / BaaS
│   │   ├── bnpl/                  # BNPL
│   │   ├── embedded-finance/      # 임베디드 금융
│   │   ├── realtime-payment/      # 실시간 결제 인프라
│   │   ├── crypto-regulation/     # 가상자산 규제
│   │   ├── stablecoin-regulation/ # 스테이블코인 규제
│   │   ├── cbdc/                  # CBDC
│   │   ├── sto/                   # 토큰증권 (STO)
│   │   ├── defi/                  # DeFi 프로토콜
│   │   ├── aml-kyc/              # AML/KYC
│   │   ├── data-regulation/       # 데이터 규제
│   │   ├── regtech/              # 레그테크
│   │   ├── saas-business/        # SaaS 비즈니스 모델
│   │   └── platform-economy/     # 플랫폼 이코노미
│   └── guide/                     # 가이드
├── templates/domain-template/     # 새 도메인 추가용 템플릿
├── mkdocs.yml                     # MkDocs 설정
├── requirements.txt               # Python 의존성
└── .github/workflows/deploy.yml   # CI/CD 파이프라인
```
