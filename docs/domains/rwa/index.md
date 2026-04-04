---
tags:
  - 디지털자산
  - RWA
  - 토큰화
search:
  boost: 2
---
# 실물자산 토큰화 (RWA)

**RWA(Real World Assets) 토큰화**는 부동산, 국채, 사모신용, 원자재, 미술품 등 실물 자산의 소유권·수익권을 블록체인 토큰으로 변환하여 발행·유통하는 것이다. 전통 금융(TradFi)과 탈중앙 금융(DeFi)을 잇는 가교이자, 자본시장 인프라의 근본적 혁신이다.

## 왜 중요한가

전통 자산시장은 높은 최소 투자 단위, 제한된 거래 시간, 복잡한 중개 구조, 느린 정산으로 인해 수조 달러 규모의 자산이 비유동 상태에 머물러 있다. RWA 토큰화는 이러한 구조적 비효율을 블록체인으로 해결한다.

2025년 기준 RWA 토큰화 시장은 **$150B 이상**으로 성장했으며, 2030년 **$16T** 규모에 이를 것으로 전망된다(BCG, McKinsey). BlackRock, JPMorgan, Franklin Templeton 등 글로벌 금융기관이 본격적으로 참여하면서, RWA는 실험적 기술을 넘어 차세대 금융 인프라로 자리잡고 있다. 특히 미국 국채 토큰화가 스테이블코인의 수익형 대안으로 급부상하며 시장 성장을 견인하고 있다.

## 핵심 키워드

| 키워드 | 설명 |
|--------|------|
| **Tokenization** | 실물 자산의 권리를 블록체인 토큰으로 변환하는 과정 |
| **Fractional Ownership** | 고가 자산을 소액 단위로 분할하여 다수가 공동 소유 |
| **On-chain/Off-chain 연결** | 실물 자산과 토큰 간의 법적·기술적 연결 구조 |
| **오라클 (Oracle)** | 실물 자산의 가격·NAV 등 오프체인 데이터를 온체인에 전달 |
| **SPV (Special Purpose Vehicle)** | 자산 격리와 파산격리를 위한 법적 구조 |
| **수탁 (Custody)** | 기초 자산(물리적)과 토큰(디지털)의 이중 보관 관리 |

```mermaid
graph TD
    subgraph 실물 자산
        TBILL[국채·MMF]
        RE[부동산]
        CREDIT[사모신용]
        COMM[원자재]
        ART[미술품·IP]
    end
    subgraph 토큰화 인프라
        SPV[SPV 설계]
        CUSTODY[수탁]
        ORACLE[오라클]
        MINT[토큰 발행]
    end
    subgraph 유통·활용
        TRADE[거래 플랫폼]
        DEFI[DeFi 담보]
        INVESTOR[투자자]
    end

    TBILL --> SPV
    RE --> SPV
    CREDIT --> SPV
    COMM --> SPV
    ART --> SPV
    SPV --> CUSTODY --> MINT
    ORACLE --> MINT
    MINT --> TRADE --> INVESTOR
    MINT --> DEFI --> INVESTOR
```

!!! info "RWA vs STO"
    **RWA**는 토큰화 대상인 "실물 자산" 관점의 개념이고, **STO(Security Token Offering)**는 토큰증권의 "발행 메커니즘" 관점의 개념이다. RWA 토큰은 STO를 통해 발행될 수 있지만, 모든 RWA가 증권은 아니며(예: 원자재 토큰), 모든 STO가 RWA를 기반으로 하지도 않는다(예: 수익분배형 유틸리티 토큰). 이 위키에서는 **자산 중심**으로 RWA를 다루며, 발행·규제 메커니즘은 [STO 도메인](../sto/index.md)을 참고하라.

## RWA 대상 자산 분류

| 자산 클래스 | 시장 규모 (2025) | 특징 | 대표 사례 |
|------------|-----------------|------|----------|
| 국채·MMF | $60B+ | 가장 빠른 성장, 안정 수익 | BlackRock BUIDL, Ondo USDY |
| 사모신용 (Private Credit) | $15B+ | 기관 수요, 높은 수익률 | Maple Finance, Centrifuge |
| 부동산 | $10B+ | 분할소유 대표 자산 | RealT, 카사, 펀블 |
| 비상장 주식 | $5B+ | PE/VC 펀드 토큰화 | Securitize, KKR |
| 원자재 | $3B+ | 금, 탄소크레딧 등 | Paxos Gold, Toucan Protocol |
| 미술품·수집품 | $2B+ | 감정·보관 복잡성 | Masterworks, 소유 |
| IP·로열티 | 초기 단계 | 음악·특허 수익권 | Royal, Anotherblock |

!!! tip "학습 순서"
    ① [핵심 개념](concepts.md) → ② [주요 플랫폼 비교](products/index.md) → ③ [트렌드](trends.md)

## 이 섹션의 구성

| 문서 | 내용 |
|------|------|
| [핵심 개념](concepts.md) | 토큰화, SPV, 오라클, 수탁, 자산 클래스별 특성 등 |
| [주요 플랫폼 비교](products/index.md) | Centrifuge, Ondo, Maple, RealT, Securitize, BUIDL 등 |
| [시장 트렌드](trends.md) | 국채 토큰화 붐, 기관 참여, DeFi-TradFi 수렴, 규제 정비 |

## 관련 도메인

- [토큰증권 (STO)](../sto/index.md) — RWA 토큰의 발행 메커니즘, 규제 준수 토큰 표준
- [DeFi 프로토콜](../defi/index.md) — RWA 토큰의 DeFi 활용 (담보 렌딩, DEX 유통)
- [스테이블코인 규제](../stablecoin-regulation/index.md) — RWA 기반 수익형 스테이블코인과의 경계
- [가상자산 규제](../crypto-regulation/index.md) — RWA 토큰의 증권성 판단, 관할별 규제 차이

## 실무 적용

- **금융기관**: 국채·MMF 토큰화 상품 설계, 수탁 인프라 구축
- **자산 운용사**: RWA 펀드 토큰화, 분할소유 상품으로 리테일 고객 확대
- **DeFi 프로토콜**: RWA 담보 풀 구성, 수익형 프로토콜 설계
- **핀테크 기업**: 조각투자 플랫폼 개발, 오라클·수탁 솔루션 제공
- **개발자**: ERC-3643, Centrifuge SDK 등 RWA 토큰 표준 구현
- **규제 기관**: 투자자 보호와 혁신 촉진의 균형 설계, 크로스보더 규제 협력
