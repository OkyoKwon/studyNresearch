# 도메인 추가 가이드

> 새로운 도메인(스터디 주제)을 사이트에 추가하는 단계별 가이드입니다.

## 사전 준비

- 프로젝트 저장소 클론
- Python 및 MkDocs 설치 (`pip install -r requirements.txt`)

## 추가 절차

### 1단계: 템플릿 복사

`templates/domain-template/` 디렉토리를 `docs/domains/` 아래에 새 이름으로 복사합니다.

```bash
cp -r templates/domain-template/ docs/domains/{새-도메인-이름}/
```

예시:

```bash
cp -r templates/domain-template/ docs/domains/open-banking/
```

### 2단계: 디렉토리 구조 확인

복사 후 다음과 같은 구조가 생성됩니다:

```
docs/domains/{새-도메인-이름}/
├── index.md          # 도메인 개요
├── concepts.md       # 핵심 개념
├── products/
│   └── index.md      # 제품 비교 개요
└── trends.md         # 트렌드
```

!!! tip "필요에 따라 파일 추가"
    도메인 특성에 맞게 추가 파일을 생성할 수 있습니다. 예를 들어 `products/` 아래에 개별 제품 파일을 추가하세요.

### 3단계: mkdocs.yml에 네비게이션 추가

`mkdocs.yml` 파일의 `nav` 섹션에 새 도메인을 추가합니다.

```yaml
nav:
  # ... 기존 항목들 ...
  - {새 도메인 이름}:
      - 개요: domains/{새-도메인-이름}/index.md
      - 핵심 개념: domains/{새-도메인-이름}/concepts.md
      - 대표 제품:
          - 비교 개요: domains/{새-도메인-이름}/products/index.md
      - 트렌드: domains/{새-도메인-이름}/trends.md
```

### 4단계: 콘텐츠 작성

각 템플릿 파일의 `{플레이스홀더}`를 실제 내용으로 교체합니다.

- `index.md`: 도메인 개요, 학습 목표, 참고 자료
- `concepts.md`: 용어 사전, 핵심 개념, 관계도
- `products/index.md`: 제품 비교표, 선택 가이드
- `trends.md`: 최신 동향, 전망, 타임라인

!!! note "AI 활용"
    [AI 프롬프트 템플릿](ai-templates.md)을 활용하면 콘텐츠 초안을 빠르게 작성할 수 있습니다.

### 5단계: 로컬 미리보기

```bash
mkdocs serve
```

브라우저에서 `http://127.0.0.1:8000`에 접속하여 결과를 확인합니다.

### 6단계: 커밋 및 배포

```bash
git add docs/domains/{새-도메인-이름}/ mkdocs.yml
git commit -m "feat: {새 도메인 이름} 도메인 추가"
git push origin main
```

`main` 브랜치에 push하면 GitHub Actions가 자동으로 사이트를 배포합니다.

## 체크리스트

- [ ] 템플릿 복사 완료
- [ ] mkdocs.yml nav에 추가 완료
- [ ] 플레이스홀더를 실제 콘텐츠로 교체
- [ ] 로컬 미리보기에서 링크 정상 확인
- [ ] 커밋 및 push 완료
