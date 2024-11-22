from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QProgressBar
from PyQt5.QtCore import QThread
from functions.disk_test_function import DiskTestWorker

class DiskTestUI(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        # 디스크 테스트 버튼 및 결과 레이블 추가
        horizontal_layout = QHBoxLayout()

        self.disk_test_button = QPushButton("모든 디스크 불량 테스트")
        self.disk_test_button.setFixedHeight(40)
        self.disk_test_button.clicked.connect(self.start_all_disk_tests)
        horizontal_layout.addWidget(self.disk_test_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(150)
        horizontal_layout.addWidget(self.progress_bar)

        self.result_label = QLabel("테스트 결과 대기 중")
        horizontal_layout.addWidget(self.result_label)

        self.layout.addLayout(horizontal_layout)

    def get_layout(self):
        return self.layout

    def set_test_buttons_enabled(self, enabled):
        # 테스트 버튼 활성화/비활성화
        self.disk_test_button.setEnabled(enabled)

    def start_all_disk_tests(self):
        # QThread를 사용하여 디스크 테스트 작업 실행
        self.thread = QThread()
        self.worker = DiskTestWorker()

        self.worker.moveToThread(self.thread)

        # 스레드 시작 시 작업 실행 연결
        self.thread.started.connect(self.worker.run_disk_test)
        self.worker.result_signal.connect(self.update_disk_result)
        self.worker.result_signal.connect(self.thread.quit)

        # 스레드 시작
        self.thread.start()

    def update_disk_result(self, result):
        # 결과 업데이트
        partition, status = result.split(":")
        if status.strip() == "success":
            self.result_label.setText(f"{partition} 테스트 성공!")
            self.result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.result_label.setText(f"{partition} 테스트 실패")
            self.result_label.setStyleSheet("color: red; font-weight: bold;")

        # 진행률 업데이트
        current_progress = self.progress_bar.value()
        progress_increment = 100 // len(self.worker.partitions)  # 파티션 개수에 따라 진행률 조정
        self.progress_bar.setValue(current_progress + progress_increment)

