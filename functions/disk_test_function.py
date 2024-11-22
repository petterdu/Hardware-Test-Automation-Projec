import subprocess
import os
from PyQt5.QtCore import QObject, pyqtSignal

class DiskTestWorker(QObject):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.partitions = []

    def find_partitions(self):
        # hardware_test.sh 경로 설정
        script_path = os.path.join(os.getcwd(), 'functions/scripts/hardware_test.sh')

        # 파티션 목록 검색 명령어 실행
        command = ["bash", script_path, "list_partitions"]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
            stdout, _ = process.communicate()

            # 결과에서 파티션 목록 추출
            self.partitions = [line.strip() for line in stdout.splitlines() if line.strip()]
        except Exception as e:
            print(f"파티션 검색 오류: {e}")

    def run_disk_test(self):
        # 파티션 검색
        self.find_partitions()

        # 비밀번호 파일 경로 설정
        password_file_path = os.path.join(os.getcwd(), 'functions/scripts/password.txt')
        if not os.path.isfile(password_file_path):
            self.result_signal.emit("failure: password file not found")
            return

        with open(password_file_path, 'r') as f:
            password = f.read().strip()

        # hardware_test.sh 경로 설정
        script_path = os.path.join(os.getcwd(), 'functions/scripts/hardware_test.sh')

        # 각 파티션 테스트
        for partition in self.partitions:
            command = f"echo {password} | sudo -S bash {script_path} disk_test {partition}"

            try:
                # 명령 실행
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()

                # 결과 출력
                print(f"STDOUT ({partition}):", stdout)
                print(f"STDERR ({partition}):", stderr)

                # 테스트 성공 여부 판별
                if "leaving filesystem unchanged." in stdout.lower() or "clean" in stdout.lower():
                    self.result_signal.emit(f"{partition}: success")
                else:
                    self.result_signal.emit(f"{partition}: failure")

            except Exception as e:
                print(f"오류 발생 ({partition}): {e}")
                self.result_signal.emit(f"{partition}: failure")

