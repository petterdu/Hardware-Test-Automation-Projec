from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt5.QtCore import QThread
from functions.gpu_test_function import GpuTestWorker

class GpuTestUI:
    def __init__(self):
        self.layout = QVBoxLayout()
        self.initUI()
        self.start_gpu_test_callback = None  # 콜백 함수 추가

    def initUI(self):
        self.add_gpu_test_button("GPU 불량 테스트", "GPU 테스트 결과", self.start_gpu_test)

    def get_layout(self):
        return self.layout

    def add_gpu_test_button(self, button_text, label_text, callback=None):
        horizontal_layout = QHBoxLayout()

        button = QPushButton(button_text)
        button.setEnabled(False)
        button.setFixedHeight(40)
        if callback:
            button.clicked.connect(callback)
        horizontal_layout.addWidget(button)
        self.gpu_test_button = button

        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setFixedWidth(150)
        horizontal_layout.addWidget(progress_bar)
        self.gpu_test_progress_bar = progress_bar

        result_label = QLabel(label_text)
        horizontal_layout.addWidget(result_label)
        self.gpu_test_result_label = result_label

        self.layout.addLayout(horizontal_layout)

    def start_gpu_test(self):
        if self.start_gpu_test_callback:
            self.start_gpu_test_callback(False)

        self.thread = QThread()
        self.worker = GpuTestWorker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run_gpu_test)
        self.worker.progress_signal.connect(self.update_gpu_progress)
        self.worker.result_signal.connect(self.update_gpu_result)
        self.worker.result_signal.connect(lambda: self.set_test_buttons_enabled(True))
        self.worker.result_signal.connect(lambda: self.start_gpu_test_callback(True))
        self.worker.result_signal.connect(self.thread.quit)

        self.thread.start()

    def update_gpu_progress(self, progress):
        if hasattr(self, 'gpu_test_progress_bar'):
            self.gpu_test_progress_bar.setValue(progress)

    def update_gpu_result(self, result):
        if hasattr(self, 'gpu_test_result_label'):
            if "success" in result:
                score = result.split(":")[1].strip()
                self.gpu_test_result_label.setText(f"GPU 테스트 통과! 점수: {score}")
                self.gpu_test_result_label.setStyleSheet("color: green; font-weight: bold;")
            elif "failure" in result:
                self.gpu_test_result_label.setText(result)
                self.gpu_test_result_label.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.gpu_test_result_label.setText("테스트 실패")
                self.gpu_test_result_label.setStyleSheet("color: red; font-weight: bold;")

    def set_test_buttons_enabled(self, enabled):
        if hasattr(self, 'gpu_test_button'):
            self.gpu_test_button.setEnabled(enabled)

