"""프론트매터 검증 — 도메인 페이지에 태그와 search.boost가 있는지 확인."""
import glob
import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"
DOMAIN_DIR = DOCS_DIR / "domains"


def _parse_frontmatter(path: Path) -> dict:
    """YAML 프론트매터에서 키를 추출한다 (간단 파서)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.index("---\n", 4)
    fm_text = text[4:end]
    result = {}
    if "tags:" in fm_text:
        tags = re.findall(r"^\s+-\s+(.+)$", fm_text.split("tags:")[1], re.MULTILINE)
        result["tags"] = [t.strip() for t in tags]
    if "boost:" in fm_text:
        m = re.search(r"boost:\s*([\d.]+)", fm_text)
        if m:
            result["boost"] = float(m.group(1))
    return result


def _get_domain_files() -> list[Path]:
    """docs/domains/ 하위의 모든 .md 파일을 반환한다."""
    return sorted(DOMAIN_DIR.rglob("*.md"))


def test_all_domain_pages_have_tags():
    """모든 도메인 페이지에 tags 프론트매터가 있어야 한다."""
    missing = []
    for path in _get_domain_files():
        fm = _parse_frontmatter(path)
        if not fm.get("tags"):
            missing.append(str(path.relative_to(DOCS_DIR)))

    assert not missing, (
        f"{len(missing)}개 파일에 tags가 없음:\n" + "\n".join(missing[:20])
    )


def test_domain_index_pages_have_search_boost():
    """도메인 최상위 index.md에 search.boost가 설정되어 있어야 한다."""
    missing = []
    for domain_dir in sorted(DOMAIN_DIR.iterdir()):
        if not domain_dir.is_dir():
            continue
        index_file = domain_dir / "index.md"
        if not index_file.exists():
            continue
        fm = _parse_frontmatter(index_file)
        if not fm.get("boost"):
            missing.append(str(index_file.relative_to(DOCS_DIR)))

    assert not missing, (
        f"{len(missing)}개 index 파일에 search.boost가 없음:\n"
        + "\n".join(missing[:20])
    )
