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

# USB 데이터 생성
run_usb_test_create() {
    PASSWORD=$(get_password)
    echo "USB에 데이터 생성 중..."
    echo $PASSWORD | sudo -S dd if=/dev/zero of=$1/testfile bs=1M count=100
    if [ $? -eq 0 ]; then
        echo "데이터 생성 완료"
    else
        echo "데이터 생성 실패"
    fi
}

# USB 데이터 복사
run_usb_test_copy() {
    PASSWORD=$(get_password)
    echo "USB 데이터 복사 중..."
    echo $PASSWORD | sudo -S cp $1/testfile /tmp/testfile_copy
    if [ $? -eq 0 ]; then
        echo "데이터 복사 완료"
    else
        echo "데이터 복사 실패"
    fi
}

# USB 데이터 비교
run_usb_test_compare() {
    echo "USB 데이터 비교 중..."
    USB_MD5=$(md5sum $1/testfile | awk '{ print $1 }')
    PC_MD5=$(md5sum /tmp/testfile_copy | awk '{ print $1 }')

    if [ "$USB_MD5" = "$PC_MD5" ]; then
        echo "The files are identical."
    else
        echo "The files are different."
    fi
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
    "usb_test_create")
        run_usb_test_create "$2"
        ;;
    "usb_test_copy")
        run_usb_test_copy "$2"
        ;;
    "usb_test_compare")
        run_usb_test_compare "$2"
        ;;
    *)
        echo "사용법: $0 {cpu|gpu|memtester|stress|list_partitions|disk_test|list_lan_ports|lan_status|ping_test|usb_test_create|usb_test_copy|usb_test_compare} [size] [repeat|partition|port|usb_path]"
        exit 1
        ;;
esac

