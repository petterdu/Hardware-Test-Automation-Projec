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

            progress = 0
            score_threshold = 300  # 테스트 성공 기준 점수
            final_score = None
            error_message = None

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())  # 디버깅용

                    # 진행률 업데이트
                    if progress < 90:
                        progress += 1
                    self.progress_signal.emit(progress)

                    # "Score"를 포함한 출력에서 점수 추출
                    if "Score:" in output:
                        try:
                            final_score = int(output.split("Score:")[1].strip())
                        except ValueError:
                            final_score = None

                    # 에러 메시지 확인
                    if any(keyword in output.lower() for keyword in ["error", "failed", "glx"]):
                        error_message = output.strip()

                time.sleep(1)  # 1초 간격 업데이트

            # 테스트 완료 후 진행률 100%로 설정
            self.progress_signal.emit(100)

            stdout, stderr = process.communicate()

            # 디버깅: 전체 출력 확인
            print("STDOUT:", stdout)
            print("STDERR:", stderr)

            # 테스트 결과 판단
            if final_score is not None:
                if final_score >= score_threshold:
                    self.result_signal.emit(f"success: 점수 {final_score}")
                else:
                    self.result_signal.emit(f"failure: 점수 낮음 ({final_score})")
            elif error_message:
                self.result_signal.emit(f"failure: {error_message}")
            else:
                self.result_signal.emit("failure: 알 수 없는 이유")

        except Exception as e:
            print(f"GPU 테스트 실행 중 오류 발생: {str(e)}")
            self.result_signal.emit(f"failure: 예외 발생 {str(e)}")

