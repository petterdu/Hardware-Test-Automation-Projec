#!/bin/bash

# 비밀번호 파일 경로 설정
PASSWORD_FILE="functions/scripts/password.txt"

# 비밀번호 파일에서 비밀번호 읽기 함수
get_password() {
    if [ -f "$PASSWORD_FILE" ]; then
        cat "$PASSWORD_FILE"
    else
        echo "비밀번호 파일을 찾을 수 없습니다. $PASSWORD_FILE 파일을 생성하고 비밀번호를 저장해 주세요."
        exit 1
    fi
}

# CPU 테스트 함수
run_cpu_test() {
    PASSWORD=$(get_password)
    echo $PASSWORD | sudo -S stress-ng --cpu 4 --timeout 60s --metrics-brief
}

# GPU 테스트 함수
run_gpu_test() {
    PASSWORD=$(get_password)
    echo $PASSWORD | sudo -S glmark2
}

# Memtester 테스트 함수
run_memtester_test() {
    PASSWORD=$(get_password)
    echo $PASSWORD | sudo -S memtester 1024M 3
}

# Stress-ng 테스트 함수
run_stress_test() {
    PASSWORD=$(get_password)
    echo $PASSWORD | sudo -S stress-ng --vm 2 --vm-bytes 1G --timeout 60s
}

# 스크립트가 받는 인자에 따라 실행할 테스트 결정
case "$1" in
    "cpu")
        run_cpu_test
        ;;
    "gpu")
        run_gpu_test
        ;;
    "memtester")
        run_memtester_test
        ;;
    "stress")
        run_stress_test
        ;;
    *)
        echo "사용법: $0 {cpu|gpu|memtester|stress}"
        exit 1
        ;;
esac

