"""Mermaid 다이어그램 문법 검증 — 일반적인 파싱 오류 패턴을 사전 탐지."""
import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

MERMAID_BLOCK = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)

# 엣지 라벨 안에 따옴표 없이 괄호가 있으면 Mermaid 파싱 에러 발생
UNQUOTED_PARENS_IN_LABEL = re.compile(r"\|([^|\"]*\([^)]*\)[^|\"]*)\|")

# 노드 정의에서 닫히지 않은 괄호/대괄호
UNCLOSED_NODE_BRACKET = re.compile(r"(\w+)\[([^\]]*$)", re.MULTILINE)
UNCLOSED_NODE_PAREN = re.compile(r"(\w+)\(([^)]*$)", re.MULTILINE)

# subgraph 이름에 따옴표 없는 특수문자 (괄호, 유니코드 구두점 포함)
SUBGRAPH_SPECIAL = re.compile(r"subgraph\s+[^\[\"]*[(){}\u00B7\u2014\u2026\u2022\u2013]")

# quadrantChart 축 레이블에 따옴표 사용 금지 (Mermaid 11.x에서 파싱 오류 발생)
QUADRANT_AXIS_QUOTED = re.compile(
    r"(x-axis|y-axis)\s+\"",
)


def _extract_mermaid_blocks() -> list[tuple[str, int, str]]:
    """모든 Mermaid 블록을 (파일경로, 라인번호, 코드) 튜플로 반환."""
    results = []
    for path in DOCS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for m in MERMAID_BLOCK.finditer(text):
            line_num = text[:m.start()].count("\n") + 1
            results.append((
                str(path.relative_to(DOCS_DIR)),
                line_num,
                m.group(1),
            ))
    return results


def test_no_unquoted_parentheses_in_edge_labels():
    """엣지 라벨에 따옴표 없는 괄호가 있으면 안 된다.

    예: |담보 매입 (할인)| → |"담보 매입 (할인)"| 로 수정 필요
    """
    errors = []
    for filepath, line_num, code in _extract_mermaid_blocks():
        for i, line in enumerate(code.split("\n"), start=1):
            match = UNQUOTED_PARENS_IN_LABEL.search(line)
            if match:
                errors.append(
                    f"  {filepath}:{line_num + i} → {match.group(0).strip()}"
                )

    assert not errors, (
        f"엣지 라벨에 따옴표 없는 괄호 발견 ({len(errors)}건):\n"
        + "\n".join(errors[:20])
    )


def test_no_unclosed_brackets_in_nodes():
    """노드 정의에서 대괄호가 닫히지 않으면 안 된다."""
    errors = []
    for filepath, line_num, code in _extract_mermaid_blocks():
        for i, line in enumerate(code.split("\n"), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("%%") or stripped.startswith("style"):
                continue
            if UNCLOSED_NODE_BRACKET.search(stripped):
                errors.append(f"  {filepath}:{line_num + i} → {stripped}")

    assert not errors, (
        f"닫히지 않은 대괄호 발견 ({len(errors)}건):\n"
        + "\n".join(errors[:20])
    )


def test_no_unclosed_parentheses_in_nodes():
    """노드 정의에서 괄호가 닫히지 않으면 안 된다."""
    errors = []
    for filepath, line_num, code in _extract_mermaid_blocks():
        for i, line in enumerate(code.split("\n"), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("%%") or stripped.startswith("style"):
                continue
            # Skip edge labels (|...|) and arrows
            if "-->" in stripped or "-.->":
                continue
            if UNCLOSED_NODE_PAREN.search(stripped):
                errors.append(f"  {filepath}:{line_num + i} → {stripped}")

    assert not errors, (
        f"닫히지 않은 괄호 발견 ({len(errors)}건):\n"
        + "\n".join(errors[:20])
    )


def test_no_special_chars_in_subgraph_names():
    """subgraph 이름에 따옴표 없는 특수문자가 있으면 안 된다."""
    errors = []
    for filepath, line_num, code in _extract_mermaid_blocks():
        for i, line in enumerate(code.split("\n"), start=1):
            if SUBGRAPH_SPECIAL.search(line):
                errors.append(f"  {filepath}:{line_num + i} → {line.strip()}")

    assert not errors, (
        f"subgraph 이름에 특수문자 발견 ({len(errors)}건):\n"
        + "\n".join(errors[:20])
    )


def test_quadrant_axis_labels_not_quoted():
    """quadrantChart 축 레이블에 따옴표를 사용하면 안 된다.

    Mermaid 11.x의 quadrantChart는 축 레이블에 따옴표를 지원하지 않아 파싱 오류가 발생한다.

    예: x-axis "DeFi 네이티브" --> "TradFi 연계"
      → x-axis DeFi 네이티브 --> TradFi 연계
    """
    errors = []
    for filepath, line_num, code in _extract_mermaid_blocks():
        first_line = code.strip().split("\n")[0].strip()
        if first_line != "quadrantChart":
            continue
        for i, line in enumerate(code.split("\n"), start=1):
            if QUADRANT_AXIS_QUOTED.search(line.strip()):
                errors.append(f"  {filepath}:{line_num + i} → {line.strip()}")

    assert not errors, (
        f"quadrantChart 축 레이블에 따옴표 사용 금지 ({len(errors)}건):\n"
        + "\n".join(errors[:20])
    )


def test_mermaid_blocks_have_diagram_type():
    """모든 Mermaid 블록이 유효한 다이어그램 타입으로 시작해야 한다."""
    valid_types = {
        "graph", "flowchart", "sequenceDiagram", "classDiagram",
        "stateDiagram", "stateDiagram-v2", "erDiagram", "gantt",
        "pie", "gitgraph", "journey", "timeline", "mindmap",
        "quadrantChart", "xychart-beta", "sankey-beta",
    }
    errors = []
    for filepath, line_num, code in _extract_mermaid_blocks():
        first_line = code.strip().split("\n")[0].strip()
        diagram_type = first_line.split()[0] if first_line else ""
        if diagram_type not in valid_types:
            errors.append(
                f"  {filepath}:{line_num} → '{first_line}'"
            )

    assert not errors, (
        f"유효하지 않은 다이어그램 타입 ({len(errors)}건):\n"
        + "\n".join(errors[:20])
    )
