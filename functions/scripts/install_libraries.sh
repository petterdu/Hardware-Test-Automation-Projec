#!/bin/bash

# 부족한 라이브러리 목록 불러오기
SCRIPTS_DIR=$(dirname "$0")
MISSING_LIBS_FILE="$SCRIPTS_DIR/missing_libraries.txt"
PASSWORD_FILE="$SCRIPTS_DIR/password.txt"

# 비밀번호 파일에서 비밀번호 읽기
if [ -f "$PASSWORD_FILE" ]; then
    PASSWORD=$(cat "$PASSWORD_FILE")
else
    echo "비밀번호 파일을 찾을 수 없습니다. $PASSWORD_FILE 파일을 생성하고 비밀번호를 저장해 주세요."
    exit 1
fi

# 부족한 라이브러리 목록 확인
if [ -f "$MISSING_LIBS_FILE" ]; then
    MISSING_LIBS=$(cat "$MISSING_LIBS_FILE")
else
    echo "설치할 라이브러리가 없습니다."
    exit 0
fi

# 부족한 라이브러리 설치 진행
for LIB in ${MISSING_LIBS}
do
    echo "비밀번호 입력 중... $LIB 설치 중입니다."
    echo $PASSWORD | sudo -S apt-get install -y "$LIB"
done

echo "설치 완료되었습니다."
