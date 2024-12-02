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

# 메모리 테스트 함수
run_memory_test() {
    PASSWORD=$(get_password)
    SIZE=$2
    REPEAT=$3
    echo $PASSWORD | sudo -S nice -n -10 memtester $SIZE $REPEAT
}

# 파티션 목록 검색 함수
list_partitions() {
    lsblk -ln -o NAME,TYPE | awk '$2 == "part" && $1 ~ /^mmcblk0p/ {print $1}'
}

# 디스크 불량 테스트 함수
run_disk_test() {
    PASSWORD=$(get_password)
    PARTITION=$2
    echo $PASSWORD | sudo -S fsck -n /dev/$PARTITION
}

# LAN 포트 목록 검색 함수
list_lan_ports() {
    ip link show | awk -F: '$0 ~ "^[2-9]:" {print $2}' | tr -d ' '
}

# LAN 포트 상태 확인 함수
# LAN 포트 상태 확인 함수
check_lan_port_status() {
    PORT=$2
    PASSWORD=$(get_password)
    echo $PASSWORD | sudo -S ethtool $PORT 2>&1
}


# 핑 테스트 함수
run_ping_test() {
    ping -c 4 8.8.8.8
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
        run_memory_test "$@"
        ;;
    "stress")
        PASSWORD=$(get_password)
        echo $PASSWORD | sudo -S stress-ng --vm 2 --vm-bytes 1G --timeout 60s
        ;;
    "list_partitions")
        list_partitions
        ;;
    "disk_test")
        run_disk_test "$@"
        ;;
    "list_lan_ports")
        list_lan_ports
        ;;
    "lan_status")
        check_lan_port_status "$@"
        ;;
    "ping_test")
        run_ping_test
        ;;
    *)
        echo "사용법: $0 {cpu|gpu|memtester|stress|list_partitions|disk_test|list_lan_ports|lan_status|ping_test} [size] [repeat|partition|port]"
        exit 1
        ;;
esac

