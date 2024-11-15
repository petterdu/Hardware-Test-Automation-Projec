import subprocess
import time
from PyQt5.QtCore import QObject, pyqtSignal

class CpuTestWorker(QObject):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)

    def run_cpu_test(self):
        # 스크립트 경로 설정
        script_path = "./functions/scripts/hardware_test.sh"

        # 스크립트 실행 - 'cpu' 인자를 전달하여 CPU 테스트 실행
        process = subprocess.Popen(['bash', script_path, 'cpu'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 진행률 업데이트 (시간 기반)
        total_time = 60  # 테스트 시간 60초
        start_time = time.time()

        while process.poll() is None:
            elapsed_time = time.time() - start_time
            progress = int((elapsed_time / total_time) * 100)
            self.progress_signal.emit(progress)  # 진행률을 시그널로 보냄

            time.sleep(1)

        stdout, stderr = process.communicate()

        # 테스트 결과 확인 및 시그널로 전달
        if "successful run completed" in stdout or "successful run completed" in stderr:
            self.result_signal.emit("success")
        else:
            self.result_signal.emit("failure")
        
        stdout, stderr = process.communicate()
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
