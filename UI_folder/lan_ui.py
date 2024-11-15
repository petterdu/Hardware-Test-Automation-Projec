from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt5.QtCore import QThread
from functions.lan_test_function import LanTestWorker

class LanTestUI:
    def __init__(self):
        self.layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        # LAN 포트 불량 테스트 버튼 추가
        self.add_lan_test_button("LAN 포트 불량 테스트", "LAN 포트 테스트 결과", self.start_lan_test)

    def get_layout(self):
        return self.layout

    def add_lan_test_button(self, button_text, label_text, callback=None):
        horizontal_layout = QHBoxLayout()

        button = QPushButton(button_text)
        button.setEnabled(False)
        button.setFixedHeight(40)
        if callback:
            button.clicked.connect(callback)
        horizontal_layout.addWidget(button)
        self.lan_test_button = button

        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setFixedWidth(150)
        horizontal_layout.addWidget(progress_bar)
        self.lan_test_progress_bar = progress_bar

        result_label = QLabel(label_text)
        horizontal_layout.addWidget(result_label)
        self.lan_test_result_label = result_label

        self.layout.addLayout(horizontal_layout)

    def start_lan_test(self):
        # 코드 구현 (LAN 테스트 시작)
        pass

    def set_test_buttons_enabled(self, enabled):
        if hasattr(self, 'lan_test_button'):
            self.lan_test_button.setEnabled(enabled)

