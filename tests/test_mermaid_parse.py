"""Mermaid 다이어그램 파서 기반 문법 검증.

mermaid 패키지의 parse() API를 사용하여 모든 다이어그램의 실제 파싱을 수행한다.
regex 정적 분석(test_mermaid.py)과 달리, 어떤 종류의 문법 오류든 감지할 수 있다.
"""
import subprocess
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "validate-mermaid.mjs"


def test_all_mermaid_diagrams_parse_successfully():
    """모든 Mermaid 다이어그램이 파서를 통과해야 한다."""
    node = shutil.which("node")
    if node is None:
        import pytest
        pytest.skip("Node.js가 설치되어 있지 않습니다")

    if not (PROJECT_ROOT / "node_modules" / "mermaid").exists():
        import pytest
        pytest.skip("mermaid 패키지 미설치 (npm ci 필요)")

    result = subprocess.run(
        [node, str(SCRIPT_PATH)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        timeout=60,
    )

    assert result.returncode == 0, (
        f"Mermaid 파싱 실패:\n{result.stderr or result.stdout}"
    )
