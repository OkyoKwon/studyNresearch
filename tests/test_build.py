"""MkDocs 빌드 테스트 — 사이트가 에러 없이 빌드되는지 검증."""
import shutil
import subprocess


def test_mkdocs_build_succeeds():
    """mkdocs build가 exit code 0으로 완료되어야 한다."""
    mkdocs = shutil.which("mkdocs")
    if mkdocs is None:
        # CI에서는 pip install로 설치되므로 경로에 있어야 함
        # 로컬에서 못 찾으면 스킵
        import pytest
        pytest.skip("mkdocs not found in PATH")

    result = subprocess.run(
        [mkdocs, "build"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"mkdocs build failed:\nSTDERR:\n{result.stderr[-2000:]}"
    )
