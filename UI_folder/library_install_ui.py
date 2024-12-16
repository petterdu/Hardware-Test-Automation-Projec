from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from functions.library_install_checker import LibraryInstaller

class LibraryInstallerUI:
    def __init__(self):
        self.installer = LibraryInstaller()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.initUI()
        self.install_callback = None

    def initUI(self):
        self.status_label = QLabel("라이브러리 설치 상태 확인 중...")
        self.status_label.setFixedWidth(300)
        self.layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(150)
        self.layout.addWidget(self.progress_bar)

        self.install_button = QPushButton("라이브러리 설치")
        self.install_button.setEnabled(False)
        self.install_button.setFixedWidth(100)
        self.install_button.clicked.connect(self.install_libraries)
        self.layout.addWidget(self.install_button)

    def get_layout(self):
        return self.layout

    def check_libraries(self):
        success, message = self.installer.check_libraries()
        self.status_label.setText(message)
        if not success:
            self.install_button.setEnabled(True)
        else:
            self.install_button.setEnabled(False)
        if self.install_callback:
            self.install_callback(success)

    def install_libraries(self):
        def progress_callback(progress, message):
            truncated_message = (message[:30] + '...') if len(message) > 30 else message
            self.progress_bar.setValue(progress)
            self.status_label.setText(truncated_message)

        self.installer.install_libraries(progress_callback)

        # 설치 완료 후 버튼 상태 업데이트
        success, message = self.installer.check_libraries()
        self.status_label.setText(message)
        if self.install_callback:
            self.install_callback(success)

