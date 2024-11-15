import os
import subprocess
import time

class LibraryInstaller:
    def __init__(self):
        self.scripts_path = os.path.join(os.path.dirname(__file__), 'scripts')

    def check_libraries(self):
        # sh 스크립트를 실행해서 필요한 라이브러리 확인
        try:
            script_path = os.path.join(self.scripts_path, "check_libraries.sh")
            result = subprocess.run(['bash', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode()

            if "설치해야 합니다" in output:
                return False, "일부 라이브러리가 설치되어 있지 않습니다."
            else:
                return True, "모든 라이브러리가 설치되어 있습니다."
        except Exception as e:
            return False, f"오류 발생: {str(e)}"

    def install_libraries(self, progress_callback):
        # 설치 진행 상태를 보여주기 위한 스크립트 실행
        try:
            script_path = os.path.join(self.scripts_path, "install_libraries.sh")
            command = f"bash {script_path}"  # 비밀번호는 install_libraries.sh에서 처리됨
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            current_progress = 0

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    if current_progress < 90:
                        current_progress += 1  # 점진적으로 퍼센티지를 증가시킴 (90%까지)
                    progress_callback(current_progress, "설치 진행 중: " + output.strip())
                    time.sleep(0.1)  # 설치 과정과 더 자연스럽게 동기화하기 위해 지연을 추가

            # 설치가 완료되면 퍼센티지를 100%로 설정
            if process.returncode == 0:
                progress_callback(100, "설치 완료")
            else:
                progress_callback(0, "설치 실패")

        except Exception as e:
            progress_callback(0, f"오류 발생: {str(e)}")

