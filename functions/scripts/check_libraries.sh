#!/bin/bash

REQUIRED_LIBS=("stress-ng" "glmark2" "memtester")
MISSING_LIBS=()

# 라이브러리 설치 여부 확인
for LIB in "${REQUIRED_LIBS[@]}"
do
    if ! dpkg -s "$LIB" >/dev/null 2>&1; then
        MISSING_LIBS+=("$LIB")
    fi
done

# 필요한 라이브러리가 있다면 출력 및 파일로 저장
SCRIPTS_DIR=$(dirname "$0")
MISSING_LIBS_FILE="$SCRIPTS_DIR/missing_libraries.txt"

if [ ${#MISSING_LIBS[@]} -ne 0 ]; then
    echo "다음 라이브러리를 설치해야 합니다: ${MISSING_LIBS[@]}"
    echo "${MISSING_LIBS[@]}" > "$MISSING_LIBS_FILE"
    exit 1
else
    echo "모든 라이브러리가 이미 설치되어 있습니다." > "$MISSING_LIBS_FILE"  # 파일 비우기
    exit 0
fi

