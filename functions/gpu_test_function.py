import subprocess
import time
from PyQt5.QtCore import QObject, pyqtSignal

class GpuTestWorker(QObject):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)

    def run_gpu_test(self):
        # GPU 테스트 명령어 설정
        command = ['bash', './functions/scripts/hardware_test.sh', 'gpu']

        try:
            # GPU 테스트 실행
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            success_found = False
            progress = 0
            score_threshold = 300  # 내장 그래픽 미니 PC 기준 평균 점수
            final_score = None
            error_message = None

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())  # 디버깅용으로 출력 확인

                    # 진행률 업데이트: 일정 비율로 점진적으로 증가시킴
                    if progress < 90:
                        progress += 1
                    self.progress_signal.emit(progress)

                    # 출력에서 "Score"라는 단어가 있는지 확인하여 성공 여부 판단
                    if "Score" in output:
                        try:
                            final_score = int(output.split("Score:")[1].strip())
                        except ValueError:
                            final_score = None

                    # 에러 메시지 확인
                    if any(error_keyword in output.lower() for error_keyword in ["error", "failed", "glx"]):
                        error_message = output.strip()

                time.sleep(1)  # 1초마다 업데이트

            # 테스트가 끝난 후 진행률을 100%로 설정
            self.progress_signal.emit(100)

            stdout, stderr = process.communicate()

            # 디버깅: 명령어의 전체 출력 확인
            print("STDOUT:", stdout)
            print("STDERR:", stderr)

            # 테스트 결과 확인 및 시그널로 전달
            if final_score is not None:
                if final_score >= score_threshold:
                    self.result_signal.emit(f"success: score {final_score}")
                else:
                    self.result_signal.emit(f"failure: score too low ({final_score})")
            elif error_message:
                self.result_signal.emit(f"failure: {error_message}")
            else:
                self.result_signal.emit("failure: unknown reason")

        except Exception as e:
            print(f"GPU 테스트 실행 중 오류 발생: {str(e)}")
            self.result_signal.emit(f"failure: exception {str(e)}")

