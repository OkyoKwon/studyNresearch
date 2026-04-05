"""GNB 드롭다운 검증 — JS 내 경로·레이블이 실제 docs 구조 및 mkdocs.yml nav와 일치하는지 확인."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"
JS_PATH = DOCS_DIR / "javascripts" / "tabs-dropdown.js"
MKDOCS_YML = ROOT / "mkdocs.yml"


def _parse_dropdowns_from_js() -> dict[str, list[dict]]:
    """tabs-dropdown.js에서 DROPDOWNS 객체를 파싱하여 반환한다."""
    text = JS_PATH.read_text(encoding="utf-8")

    # var DROPDOWNS = { ... }; 블록 추출
    match = re.search(
        r"var\s+DROPDOWNS\s*=\s*\{(.+?)\};",
        text,
        re.DOTALL,
    )
    assert match, "DROPDOWNS 객체를 tabs-dropdown.js에서 찾을 수 없음"

    raw = match.group(0)
    # JS → JSON 변환: 키에 따옴표 추가, 후행 콤마 제거
    js_obj = raw.replace("var DROPDOWNS = ", "").rstrip(";")
    # JS 키를 JSON 키로: "결제/금융 인프라": → 유지 (이미 따옴표 있음)
    # label, path 같은 키에 따옴표 추가
    js_obj = re.sub(r'(\s)(label|path)(\s*:)', r'\1"\2"\3', js_obj)
    # 후행 콤마 제거
    js_obj = re.sub(r",(\s*[}\]])", r"\1", js_obj)

    return json.loads(js_obj)


def _load_mkdocs_nav() -> list:
    """mkdocs.yml에서 nav 섹션만 추출한다 (!!python 태그 우회)."""
    text = MKDOCS_YML.read_text(encoding="utf-8")
    # nav: 블록만 추출 (다음 최상위 키 전까지)
    match = re.search(r"^nav:\s*\n((?:[ \t]+.+\n)*)", text, re.MULTILINE)
    assert match, "mkdocs.yml에서 nav 섹션을 찾을 수 없음"
    import yaml
    return yaml.safe_load("nav:\n" + match.group(1))["nav"]


def _extract_nav_tabs(nav: list) -> dict[str, list[str]]:
    """mkdocs.yml nav에서 탭명 → 하위 도메인 디렉토리 목록을 추출한다."""
    tabs = {}
    for item in nav:
        if isinstance(item, dict):
            for tab_name, children in item.items():
                if tab_name in ("홈", "가이드", "태그 색인"):
                    continue
                if not isinstance(children, list):
                    continue
                # 하위 도메인 디렉토리 추출
                domains = []
                for child in children:
                    if isinstance(child, dict):
                        for _sub_name, sub_val in child.items():
                            if isinstance(sub_val, list):
                                for sub_item in sub_val:
                                    if isinstance(sub_item, dict):
                                        for _k, v in sub_item.items():
                                            if isinstance(v, str) and v.startswith("domains/"):
                                                domain_dir = "/".join(v.split("/")[:2])
                                                if domain_dir not in domains:
                                                    domains.append(domain_dir)
                                                break
                                        break
                                    elif isinstance(sub_item, str) and sub_item.startswith("domains/"):
                                        domain_dir = "/".join(sub_item.split("/")[:2])
                                        if domain_dir not in domains:
                                            domains.append(domain_dir)
                                        break
                tabs[tab_name] = domains
    return tabs


# ── 테스트 ──


def test_js_file_exists():
    """tabs-dropdown.js 파일이 존재해야 한다."""
    assert JS_PATH.exists(), f"{JS_PATH} 파일이 존재하지 않음"


def test_dropdowns_parseable():
    """DROPDOWNS 객체가 파싱 가능해야 한다."""
    dropdowns = _parse_dropdowns_from_js()
    assert isinstance(dropdowns, dict)
    assert len(dropdowns) > 0


def test_dropdown_paths_exist():
    """모든 드롭다운 경로가 실제 docs/ 디렉토리에 존재해야 한다."""
    dropdowns = _parse_dropdowns_from_js()
    missing = []
    for tab, items in dropdowns.items():
        for item in items:
            target = DOCS_DIR / item["path"]
            # 디렉토리이면 index.md 확인
            if target.is_dir():
                index = target / "index.md"
                if not index.exists():
                    missing.append(f"  [{tab}] {item['label']} → {item['path']}index.md")
            elif not target.exists():
                missing.append(f"  [{tab}] {item['label']} → {item['path']}")

    assert not missing, (
        f"존재하지 않는 드롭다운 경로 {len(missing)}건:\n" + "\n".join(missing)
    )


def test_dropdown_labels_not_empty():
    """드롭다운 레이블이 비어있지 않아야 한다."""
    dropdowns = _parse_dropdowns_from_js()
    empty = []
    for tab, items in dropdowns.items():
        for item in items:
            if not item.get("label", "").strip():
                empty.append(f"  [{tab}] path={item.get('path', '?')}")

    assert not empty, f"빈 레이블 {len(empty)}건:\n" + "\n".join(empty)


def test_dropdown_categories_match_nav():
    """드롭다운 카테고리가 mkdocs.yml nav의 탭과 일치해야 한다."""
    dropdowns = _parse_dropdowns_from_js()
    nav_tabs = _extract_nav_tabs(_load_mkdocs_nav())

    dropdown_keys = set(dropdowns.keys())
    nav_keys = set(nav_tabs.keys())

    missing_in_js = nav_keys - dropdown_keys
    extra_in_js = dropdown_keys - nav_keys

    errors = []
    if missing_in_js:
        errors.append(f"  nav에는 있지만 JS에 없는 탭: {missing_in_js}")
    if extra_in_js:
        errors.append(f"  JS에는 있지만 nav에 없는 탭: {extra_in_js}")

    assert not errors, "드롭다운 카테고리 불일치:\n" + "\n".join(errors)


def test_dropdown_domains_match_nav():
    """각 카테고리의 하위 도메인 경로가 mkdocs.yml nav 구조와 일치해야 한다."""
    dropdowns = _parse_dropdowns_from_js()
    nav_tabs = _extract_nav_tabs(_load_mkdocs_nav())

    mismatches = []
    for tab, nav_domains in nav_tabs.items():
        if tab not in dropdowns:
            continue
        js_domains = [item["path"].rstrip("/") for item in dropdowns[tab]]
        nav_set = set(nav_domains)
        js_set = set(js_domains)

        missing = nav_set - js_set
        extra = js_set - nav_set

        if missing:
            mismatches.append(f"  [{tab}] nav에는 있지만 JS에 없음: {missing}")
        if extra:
            mismatches.append(f"  [{tab}] JS에는 있지만 nav에 없음: {extra}")

    assert not mismatches, (
        f"도메인 경로 불일치 {len(mismatches)}건:\n" + "\n".join(mismatches)
    )


def test_js_has_portal_pattern():
    """JS가 body-append portal 패턴을 사용해야 한다 (탭 내부 append 아님)."""
    text = JS_PATH.read_text(encoding="utf-8")
    assert "document.body.appendChild" in text, "document.body.appendChild가 없음 — portal 패턴 미사용"
    assert "position: fixed" in text or "position" in text, "fixed positioning이 없음"


def test_js_has_instant_nav_support():
    """instant navigation 지원을 위한 MutationObserver와 cleanup 로직이 있어야 한다."""
    text = JS_PATH.read_text(encoding="utf-8")
    assert "MutationObserver" in text, "MutationObserver가 없음 — instant navigation 미지원"
    assert "cleanupPortals" in text, "cleanupPortals가 없음 — 포털 정리 로직 누락"
    assert "isDropdownsMapped" in text, "isDropdownsMapped가 없음 — 매핑 검증 로직 누락"


def test_js_has_mobile_hide():
    """모바일에서 드롭다운을 숨기는 CSS가 extra.css에 있어야 한다."""
    css_path = DOCS_DIR / "stylesheets" / "extra.css"
    text = css_path.read_text(encoding="utf-8")
    assert "max-width: 960px" in text, "모바일 숨김 미디어쿼리가 없음"
    assert ".tabs-dropdown" in text, ".tabs-dropdown 스타일이 없음"


def test_no_duplicate_paths():
    """같은 카테고리 내 중복 경로가 없어야 한다."""
    dropdowns = _parse_dropdowns_from_js()
    duplicates = []
    for tab, items in dropdowns.items():
        paths = [item["path"] for item in items]
        seen = set()
        for p in paths:
            if p in seen:
                duplicates.append(f"  [{tab}] {p}")
            seen.add(p)

    assert not duplicates, f"중복 경로 {len(duplicates)}건:\n" + "\n".join(duplicates)
