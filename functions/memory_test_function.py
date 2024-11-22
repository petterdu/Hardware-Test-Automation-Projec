import subprocess
import os
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import time

class MemoryTestWorker(QObject):
    progress_signal = pyqtSignal(int)  # 진행률 시그널 추가
    result_signal = pyqtSignal(str)

    def __init__(self, test_type):
        super().__init__()
        self.test_type = test_type
        self._running = False

    def run_memory_test(self):
        # hardware_test.sh 스크립트 경로 설정
        script_path = os.path.join(os.getcwd(), 'functions/scripts/hardware_test.sh')

        # 테스트 유형에 따른 인자 설정
        if self.test_type == "memtester":
            self.run_memtester_test(script_path)
        elif self.test_type == "stress":
            self.run_stress_test(script_path)
        else:
            self.result_signal.emit("failure")

    def run_memtester_test(self, script_path):
        repeat_count = "1"  # 반복 횟수를 줄여서 설정
        chunk_size = "256M"  # 테스트할 메모리 크기
        num_chunks = 4  # 병렬 실행할 프로세스 수

        processes = []

        for _ in range(num_chunks):
            command = ["nice", "-n", "-10", "bash", script_path, "memtester", chunk_size, repeat_count]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            processes.append(process)

        # 모든 프로세스의 종료 대기 및 결과 확인
        all_successful = True
        for process in processes:
            stdout, stderr = process.communicate()
            print("STDOUT (final):", stdout)  # 결과 확인을 위해 stdout 출력
            print("STDERR (final):", stderr)  # 결과 확인을 위해 stderr 출력
            process.wait()

            # 성공 여부 판단
            if "done" not in stdout.lower() and "done" not in stderr.lower():
                all_successful = False

        if all_successful:
            self.result_signal.emit("success")
        else:
            self.result_signal.emit("failure")

    def run_stress_test(self, script_path):
        command = ["bash", script_path, "stress"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        total_duration = 60  # 예를 들어 60초 동안 실행된다고 가정
        start_time = time.time()
        self._running = True

        # 진행률 업데이트를 시간 기반으로 계산하여 단순 출력
        while self._running:
            elapsed_time = time.time() - start_time
            progress = min(int((elapsed_time / total_duration) * 100), 100)
            self.progress_signal.emit(progress)

            if progress >= 100 or process.poll() is not None:
                self._running = False
                break

            time.sleep(1)

        # 프로세스 종료 대기 및 결과 확인
        stdout, stderr = process.communicate()
        print("STDOUT (final):", stdout)  # 결과 확인을 위해 stdout 출력
        print("STDERR (final):", stderr)  # 결과 확인을 위해 stderr 출력
        self._running = False

        # 성공 여부 판단
        if "successful run completed" in stdout.lower() or "successful run completed" in stderr.lower():
            self.result_signal.emit("success")
        else:
            self.result_signal.emit("failure")

        self.progress_signal.emit(100)  # 테스트 완료 후 진행률 100%로 설정

