import subprocess
import os
from PyQt5.QtCore import QObject, pyqtSignal

class LanTestWorker(QObject):
    result_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.lan_ports = []

    def find_lan_ports(self):
        # hardware_test.sh 경로 설정
        script_path = os.path.join(os.getcwd(), 'functions/scripts/hardware_test.sh')

        # LAN 포트 목록 검색 명령어 실행
        command = ["bash", script_path, "list_lan_ports"]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
            stdout, _ = process.communicate()

            # 결과에서 LAN 포트 목록 추출
            self.lan_ports = [line.strip() for line in stdout.splitlines() if line.strip()]
        except Exception as e:
            print(f"LAN 포트 검색 오류: {e}")

    def check_lan_port_status(self):
        # LAN 포트 검색
        self.find_lan_ports()

        # hardware_test.sh 경로 설정
        script_path = os.path.join(os.getcwd(), 'functions/scripts/hardware_test.sh')

        # 각 LAN 포트 상태 확인
        for port in self.lan_ports:
            command = ["bash", script_path, "lan_status", port]

            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()

                # 결과 출력
                print(f"STDOUT ({port}):", stdout)
                print(f"STDERR ({port}):", stderr)

                # 포트 상태 판별
                if "Link detected: yes" in stdout:
                    self.result_signal.emit(f"{port}: 활성화됨 (UP)")
                else:
                    self.result_signal.emit(f"{port}: 비활성화됨 (DOWN)")

            except Exception as e:
                print(f"오류 발생 ({port}): {e}")
                self.result_signal.emit(f"{port}: 오류 발생")

    def run_ping_test(self):
        # hardware_test.sh 경로 설정
        script_path = os.path.join(os.getcwd(), 'functions/scripts/hardware_test.sh')
        command = ["bash", script_path, "ping_test"]

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            # 핑 테스트 결과 출력
            print(f"핑 테스트 STDOUT: {stdout}")
            print(f"핑 테스트 STDERR: {stderr}")

            if "0% packet loss" in stdout:
                self.result_signal.emit("핑 테스트 성공")
            else:
                self.result_signal.emit("핑 테스트 실패")

        except Exception as e:
            print(f"핑 테스트 오류: {e}")
            self.result_signal.emit("핑 테스트 오류 발생")

