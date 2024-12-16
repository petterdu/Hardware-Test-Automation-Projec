import os
import subprocess
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar, QWidget
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QMovie
from functions.usb_test_function import UsbTestWorker

class UsbTestUI(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.initUI()
        self.start_usb_test_callback = None  # 콜백 추가

    def initUI(self):
        # USB 테스트 버튼 및 결과 레이블 추가
        horizontal_layout = QHBoxLayout()

        self.usb_test_button = QPushButton("USB 불량 테스트")
        self.usb_test_button.setFixedHeight(40)
        self.usb_test_button.clicked.connect(self.start_usb_test)
        horizontal_layout.addWidget(self.usb_test_button)

        # 프로그레스 바 추가
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(150)
        horizontal_layout.addWidget(self.progress_bar)

        # USB 상태 레이블
        self.usb_status_label = QLabel("USB 상태: 검색 중...")
        horizontal_layout.addWidget(self.usb_status_label)

        # 결과 레이블
        self.result_label = QLabel("테스트 결과 대기 중")
        horizontal_layout.addWidget(self.result_label)

        # 로딩 GIF 설정
        base_path = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(base_path, "loading.gif")
        self.loading_movie = QMovie(gif_path)
        self.loading_label = QLabel(self)
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setFixedSize(30, 30)
        self.loading_label.setScaledContents(True)
        self.loading_label.hide()  # 초기에는 숨김 상태
        horizontal_layout.addWidget(self.loading_label)

        self.layout.addLayout(horizontal_layout)

    def get_layout(self):
        return self.layout

    def set_test_buttons_enabled(self, enabled):
        if hasattr(self, 'usb_test_button'):
            self.usb_test_button.setEnabled(enabled)

    def detect_usb(self):
        """현재 연결된 USB 경로를 검색"""
        try:
            result = subprocess.run(["lsblk", "-ln", "-o", "NAME,MOUNTPOINT"], stdout=subprocess.PIPE, text=True)
            devices = result.stdout.strip().split("\n")
            for device in devices:
                parts = device.split()
                if len(parts) == 2 and "/media" in parts[1]:  # 마운트된 경로 확인
                    return parts[1]  # USB 마운트 경로 반환
        except Exception as e:
            print(f"USB 검색 중 오류 발생: {e}")
        return None

    def start_usb_test(self):
        usb_path = self.detect_usb()
        if not usb_path:
            self.usb_status_label.setText("USB 상태: USB가 감지되지 않았습니다.")
            self.result_label.setText("USB를 연결한 후 다시 시도해 주세요.")
            return

        self.usb_status_label.setText(f"USB 상태: {usb_path}에 연결됨")

        self.set_test_buttons_enabled(False)  # 모든 버튼 비활성화

        # 로딩 GIF 및 프로그레스 바 초기화
        self.loading_label.show()
        self.loading_movie.start()
        self.progress_bar.setValue(0)

        # QThread 및 Worker 설정
        self.thread = QThread()
        self.worker = UsbTestWorker(usb_path)
        self.worker.moveToThread(self.thread)

        # 시그널 연결
        self.worker.usb_status_signal.connect(self.update_usb_status)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.result_signal.connect(self.update_result)

        self.thread.started.connect(self.worker.run_usb_test)
        self.worker.result_signal.connect(lambda: self.loading_label.hide())
        self.worker.result_signal.connect(lambda: self.loading_movie.stop())
        self.worker.result_signal.connect(lambda: self.set_test_buttons_enabled(True))
        self.worker.result_signal.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def update_usb_status(self, status):
        """USB 상태 레이블 업데이트"""
        self.usb_status_label.setText(status)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def update_result(self, result):
        """USB 테스트 결과 업데이트"""
        if "USB 불량 테스트 성공!" in result:
            self.result_label.setText(result)
            self.result_label.setStyleSheet("color: green; font-weight: bold;")  # 초록색과 굵게 설정
        elif "USB 불량 테스트 실패!" in result:
            self.result_label.setText(result)
            self.result_label.setStyleSheet("color: red; font-weight: bold;")  # 실패 시 빨간색과 굵게 설정
        else:
            self.result_label.setText(result)
            self.result_label.setStyleSheet("")  # 기본 스타일


