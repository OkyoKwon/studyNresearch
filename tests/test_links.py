"""내부 링크 검증 — 마크다운 파일 간 링크가 유효한지 확인."""
import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

# [text](relative/path.md) 또는 [text](relative/path.md#anchor)
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def _is_internal_link(href: str) -> bool:
    """외부 URL, 앵커 전용, mailto 등을 제외한 내부 링크인지 확인."""
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return False
    if href.startswith("..") or href.endswith(".md") or "/" in href:
        return True
    return False


def test_internal_links_resolve():
    """내부 마크다운 링크가 실제 파일을 가리켜야 한다."""
    broken = []
    for path in DOCS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")

        # Mermaid 블록 안의 링크는 제외
        text_no_mermaid = re.sub(r"```mermaid.*?```", "", text, flags=re.DOTALL)

        for match in MD_LINK.finditer(text_no_mermaid):
            href = match.group(2)
            if not _is_internal_link(href):
                continue

            # 앵커 제거
            href_no_anchor = href.split("#")[0]
            if not href_no_anchor:
                continue

            # 상대 경로 해석
            target = (path.parent / href_no_anchor).resolve()

            # 디렉토리면 index.md 확인
            if target.is_dir():
                target = target / "index.md"

            if not target.exists():
                rel = str(path.relative_to(DOCS_DIR))
                broken.append(f"  {rel} → {href}")

    assert not broken, (
        f"깨진 내부 링크 {len(broken)}건:\n" + "\n".join(broken[:30])
    )
