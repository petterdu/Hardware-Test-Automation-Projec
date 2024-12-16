import subprocess
from PyQt5.QtCore import QObject, pyqtSignal

class UsbTestWorker(QObject):
    progress_signal = pyqtSignal(int)  # 진행률 신호
    result_signal = pyqtSignal(str)  # 결과 신호
    usb_status_signal = pyqtSignal(str)  # USB 상태 신호

    def __init__(self, usb_path):
        super().__init__()
        self.usb_path = usb_path

    def run_usb_test(self):
        try:
            # USB 포트 정보 가져오기
            usb_status = self.get_usb_port_info()
            self.usb_status_signal.emit(usb_status)  # USB 상태 UI 업데이트

            # 1단계: 데이터 생성
            self.progress_signal.emit(33)
            print("1단계: 데이터 생성 중...")
            self.execute_command(["bash", "functions/scripts/hardware_test.sh", "usb_test_create", self.usb_path])
            print("1단계 완료: 데이터 생성 완료!")

            # 2단계: 데이터 복사
            self.progress_signal.emit(66)
            print("2단계: 데이터 복사 중...")
            self.execute_command(["bash", "functions/scripts/hardware_test.sh", "usb_test_copy", self.usb_path])
            print("2단계 완료: 데이터 복사 완료!")

            # 3단계: 데이터 비교
            self.progress_signal.emit(100)
            print("3단계: 데이터 비교 중...")
            compare_result = self.execute_command(["bash", "functions/scripts/hardware_test.sh", "usb_test_compare", self.usb_path])
            print(f"3단계 완료: {compare_result.strip()}")

            # 결과 처리
            if "The files are identical." in compare_result:
                self.result_signal.emit("USB 불량 테스트 성공! 다른 포트에 USB를 꽂아주세요.")
            else:
                self.result_signal.emit("USB 불량 테스트 실패! 파일이 일치하지 않습니다.")
        except Exception as e:
            self.result_signal.emit(f"오류 발생: {str(e)}")

    def execute_command(self, command):
        """명령어 실행 후 결과 반환"""
        try:
            print(f"명령어 실행: {' '.join(command)}")  # 디버깅 메시지 출력
            process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"STDOUT: {process.stdout.strip()}")
            print(f"STDERR: {process.stderr.strip()}")
            return process.stdout
        except Exception as e:
            print(f"명령어 실행 중 오류 발생: {e}")
            return f"오류 발생: {e}"

    def get_usb_port_info(self):
        """USB 연결 정보를 간단히 추출합니다."""
        try:
            lsusb_output = subprocess.run(["lsusb"], stdout=subprocess.PIPE, text=True).stdout.strip()
            if not lsusb_output:
                return "USB가 감지되지 않았습니다."

            # 첫 번째 USB 장치 정보만 사용 (예제)
            device_info = lsusb_output.split("\n")[0]  # 첫 번째 USB 장치 가져오기
            bus, device = device_info.split()[1], device_info.split()[3].strip(":")
            return f"USB 상태: {bus}번 버스, {device}번 디바이스에 연결됨"
        except Exception as e:
            return f"USB 상태를 확인할 수 없습니다: {str(e)}"

