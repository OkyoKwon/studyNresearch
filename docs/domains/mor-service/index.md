# MOR(Merchant of Record) 서비스 개요

## MOR이란 무엇인가

**Merchant of Record(MOR)** 는 고객과의 거래에서 **법적 판매자(Legal Seller of Record)** 역할을 대행하는 서비스다. 소프트웨어 개발사가 직접 판매자가 되는 대신, MOR 서비스 제공자가 법적 판매 주체가 되어 결제 처리, 세금 징수 및 납부, 환불, 차지백 대응까지 전부 책임진다.

쉽게 말하면 **"내 제품을 대신 팔아주는 공인 대리점"** 이다. 고객의 신용카드 명세서에는 MOR 서비스 회사 이름이 찍히고, 세금 신고 의무도 MOR이 진다.

## 왜 알아야 하는가

SaaS를 글로벌로 판매할 때, 각국의 세금 규정을 직접 준수하는 것은 매우 복잡하고 비용이 크다.

- **EU 27개국** 각각 다른 VAT 세율과 규정
- **미국 50개 주** 의 Sales Tax Nexus 규칙
- **인도, 호주, 캐나다** 등의 GST 규정
- **디지털세(Digital Services Tax)** 확산 추세

MOR 서비스를 사용하면 이 모든 세금 처리, 규제 준수, 결제 인프라를 단일 계약으로 해결할 수 있다. 특히 **인디 개발자, 소규모 SaaS 팀** 에게는 글로벌 진출의 현실적인 유일한 경로인 경우가 많다.

## 핵심 키워드

| 키워드 | 설명 |
|---|---|
| **Merchant of Record** | 법적 판매 주체를 대행하는 서비스 모델 |
| **Reseller 모델** | MOR이 제품을 구매 후 재판매하는 구조 |
| **VAT / GST / Sales Tax** | 각국의 부가가치세 및 판매세 |
| **Tax Compliance** | 세금 규정 준수 (징수, 신고, 납부) |
| **Chargeback** | 고객의 결제 이의 제기 처리 |
| **Payment Localization** | 현지 통화, 결제 수단 지원 |

## 하위 문서 목차

| 문서 | 내용 |
|---|---|
| [핵심 개념](./concepts.md) | MOR 관련 용어와 개념 상세 정리 |
| [PG vs MOR 비교](./pg-vs-mor.md) | 결제 대행(PG)과 MOR의 차이점 및 선택 기준 |
| [제품 비교 개요](./products/index.md) | Paddle, Lemon Squeezy, FastSpring 등 주요 제품 비교 |
| [Paddle 상세](./products/paddle.md) | Paddle 서비스 심층 분석 |
| [Lemon Squeezy 상세](./products/lemon-squeezy.md) | Lemon Squeezy 서비스 심층 분석 |
| [FastSpring 상세](./products/fastspring.md) | FastSpring 서비스 심층 분석 |
| [트렌드 및 전망](./trends.md) | MOR 시장 동향과 미래 전망 |

## 관련 도메인

- [PG(Payment Gateway) 서비스](../pg-service/index.md) - MOR과 자주 비교되는 결제 대행 서비스. PG는 결제 처리만 담당하고 세금/법적 판매자 역할은 하지 않는다.
- [암호화폐 규제](../crypto-regulation/index.md) - 디지털 자산 관련 글로벌 규제 동향
