#!/usr/bin/env bash
# Mermaid 다이어그램 빠른 regex 검증 (PostToolUse 훅용)
# 사용법: check-mermaid-quick.sh <file_path>
# 종료 코드: 0 = 정상, 1 = 위반 발견

set -euo pipefail

FILE="$1"

# docs/ 디렉토리의 .md 파일만 검사
if [[ ! "$FILE" =~ docs/.*\.md$ ]]; then
  exit 0
fi

if [[ ! -f "$FILE" ]]; then
  exit 0
fi

ERRORS=()

# --- 헬퍼: 문자열이 순수 한글+공백+슬래시만인지 판별 ---
is_pure_korean() {
  local text="$1"
  # 영문(a-zA-Z)이나 숫자가 하나라도 있으면 false
  if echo "$text" | grep -q '[a-zA-Z0-9]'; then
    return 1
  fi
  # 한글이 하나라도 있으면 true
  if echo "$text" | grep -q '[가-힣]'; then
    return 0
  fi
  return 1
}

# --- mermaid 블록 파싱 ---
IN_BLOCK=false
BLOCK=""
BLOCK_START=0
LINE_NUM=0

while IFS= read -r line || [[ -n "$line" ]]; do
  ((LINE_NUM++))

  if [[ "$line" =~ ^\`\`\`mermaid ]]; then
    IN_BLOCK=true
    BLOCK=""
    BLOCK_START=$LINE_NUM
    continue
  fi

  if $IN_BLOCK && [[ "$line" =~ ^\`\`\` ]]; then
    IN_BLOCK=false
    DIAGRAM_TYPE=$(echo "$BLOCK" | head -1 | awk '{print $1}')

    # === quadrantChart 검사 ===
    if [[ "$DIAGRAM_TYPE" == "quadrantChart" ]]; then

      while IFS= read -r axis_line; do
        # 축 레이블 추출
        label_left=$(echo "$axis_line" | sed -E 's/.*(x-axis|y-axis)[[:space:]]*//' | sed 's/[[:space:]]*-->.*//')
        label_right=$(echo "$axis_line" | sed 's/.*-->[[:space:]]*//')

        # 순수 한글 검사
        if is_pure_korean "$label_left"; then
          ERRORS+=("L$BLOCK_START: quadrantChart 축 레이블 순수한글 금지 — $axis_line")
        fi
        if is_pure_korean "$label_right"; then
          ERRORS+=("L$BLOCK_START: quadrantChart 축 레이블 순수한글 금지 — $axis_line")
        fi

        # 따옴표 검사
        if echo "$axis_line" | grep -qE '(x-axis|y-axis)[[:space:]]+"'; then
          ERRORS+=("L$BLOCK_START: quadrantChart 축 레이블 따옴표 금지 — $axis_line")
        fi

        # 3단어 초과 검사
        label_left_w=$(echo "$axis_line" | sed -E 's/.*(x-axis|y-axis)[[:space:]]*//' | sed 's/[[:space:]]*-->.*//')
        left_words=$(echo "$label_left_w" | wc -w | tr -d ' ')
        right_words=$(echo "$label_right" | wc -w | tr -d ' ')
        if [[ "$left_words" -gt 2 ]] || [[ "$right_words" -gt 2 ]]; then
          ERRORS+=("L$BLOCK_START: quadrantChart 축 레이블 3단어 이상 — $axis_line")
        fi
      done < <(echo "$BLOCK" | grep -E '(x-axis|y-axis).*-->')

    fi

    # === 노드 텍스트 내 따옴표 없는 괄호 검사 ===
    while IFS= read -r node_line; do
      # [텍스트(괄호)] 패턴 감지 — ["텍스트(괄호)"]는 허용
      clean=$(echo "$node_line" | sed 's/\["[^"]*"\]//g')
      if echo "$clean" | grep -q '\[[^]]*([^)]*)[^]]*\]'; then
        ERRORS+=("L$BLOCK_START: 노드 텍스트 내 괄호는 따옴표 필수 — $(echo "$node_line" | sed 's/^[[:space:]]*//')")
      fi
    done < <(echo "$BLOCK" | grep -v '^\s*%%' | grep '\[.*(.*).*\]')

    continue
  fi

  if $IN_BLOCK; then
    BLOCK+="$line"$'\n'
  fi

done < "$FILE"

if [[ ${#ERRORS[@]} -gt 0 ]]; then
  echo ""
  echo "⚠ Mermaid 문법 위반 (${#ERRORS[@]}건) in $FILE:"
  for err in "${ERRORS[@]}"; do
    echo "  $err"
  done
  echo ""
  echo "→ .claude/CLAUDE.md 'Mermaid 다이어그램 작성 규칙' 참고"
  exit 1
fi

exit 0
