import os
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QProgressBar
from PyQt5.QtCore import QThread
from functions.lan_test_function import LanTestWorker


class LanTestUI(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.initUI()
        self.is_lan_active = False  # LAN 활성화 여부를 저장

    def initUI(self):
        # LAN 포트 테스트 버튼 및 결과 레이블 추가
        horizontal_layout = QHBoxLayout()

        self.lan_test_button = QPushButton("LAN 포트 불량 테스트")
        self.lan_test_button.setFixedHeight(40)
        self.lan_test_button.clicked.connect(self.start_lan_test)
        horizontal_layout.addWidget(self.lan_test_button)

        self.ping_test_button = QPushButton("핑 테스트")
        self.ping_test_button.setFixedHeight(40)
        self.ping_test_button.setEnabled(False)  # 초기에는 비활성화
        self.ping_test_button.clicked.connect(self.start_ping_test)
        horizontal_layout.addWidget(self.ping_test_button)

        # 로딩 GIF 설정
        base_path = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(base_path, "loading.gif")
        self.loading_movie = QMovie(gif_path)
        self.loading_label = QLabel(self)
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setFixedSize(30, 30)
        self.loading_label.setScaledContents(True)
        self.loading_label.hide()  # 초기에는 숨김 상태

        # 결과 레이블 추가
        self.result_label = QLabel("테스트 결과 대기 중")

        # 로딩 GIF와 결과 레이블 순서 변경
        horizontal_layout.addWidget(self.loading_label)
        horizontal_layout.addWidget(self.result_label)

        self.layout.addLayout(horizontal_layout)

    def get_layout(self):
        return self.layout

    def set_test_buttons_enabled(self, enabled):
        # 테스트 버튼 활성화/비활성화
        self.lan_test_button.setEnabled(enabled)
        self.ping_test_button.setEnabled(False)  # 초기에는 핑 테스트 버튼을 비활성화

    def start_lan_test(self):
        # QThread를 사용하여 LAN 테스트 작업 실행
        self.thread = QThread()
        self.worker = LanTestWorker()

        self.worker.moveToThread(self.thread)

        # 스레드 시작 시 작업 실행 연결
        self.thread.started.connect(self.worker.check_lan_port_status)
        self.worker.result_signal.connect(self.update_result)
        self.worker.result_signal.connect(self.thread.quit)

        # 초기 상태
        self.is_lan_active = False  # LAN 활성화 여부 초기화

        # 스레드 시작
        self.thread.start()

    def start_ping_test(self):
        # 핑 테스트 버튼을 누르면 '핑 테스트 중' 문구 표시
        self.result_label.setText("핑 테스트 중...")
        self.result_label.setStyleSheet("color: blue; font-weight: bold;")
        self.loading_label.show()
        self.loading_movie.start()
        self.ping_test_button.setEnabled(False)  # 핑 테스트 중에는 버튼 비활성화

        # QThread를 사용하여 핑 테스트 작업 실행
        self.ping_thread = QThread()
        self.ping_worker = LanTestWorker()

        self.ping_worker.moveToThread(self.ping_thread)

        # 스레드 시작 시 작업 실행 연결
        self.ping_thread.started.connect(self.ping_worker.run_ping_test)
        self.ping_worker.result_signal.connect(self.update_ping_result)
        self.ping_worker.result_signal.connect(self.ping_thread.quit)

        # 스레드 시작
        self.ping_thread.start()

    def update_result(self, result):
        # 결과 업데이트
        if "활성화됨 (UP)" in result:
            self.result_label.setText(f"{result} - 핑 테스트를 마저 진행해 주세요")
            self.result_label.setStyleSheet("color: green; font-weight: bold;")
            self.is_lan_active = True  # LAN 포트 활성화 상태로 설정
        else:
            self.result_label.setText(result)
            self.result_label.setStyleSheet("color: red; font-weight: bold;")

        # 핑 테스트 버튼 활성화/비활성화
        self.ping_test_button.setEnabled(self.is_lan_active)

    def update_ping_result(self, result):
        # 핑 테스트 완료 시 로딩 GIF 숨김
        self.loading_label.hide()
        self.loading_movie.stop()

        # 핑 테스트 결과 업데이트
        if "성공" in result:
            self.result_label.setText(result)
            self.result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.result_label.setText(result)
            self.result_label.setStyleSheet("color: red; font-weight: bold;")
        self.ping_test_button.setEnabled(False)  # 핑 테스트 후에는 버튼 비활성화

