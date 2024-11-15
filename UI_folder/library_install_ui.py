from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from functions.library_install_checker import LibraryInstaller

class LibraryInstallerUI:
    def __init__(self):
        self.installer = LibraryInstaller()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)  # 좌측 정렬 고정
        self.initUI()

    def initUI(self):
        # 설치 상태를 표시하는 라벨
        self.status_label = QLabel("라이브러리 설치 상태 확인 중...")
        self.status_label.setFixedWidth(300)  # 고정된 길이로 설정하여 위치 고정
        self.layout.addWidget(self.status_label)

        # 설치 진행 퍼센티지를 표시하는 진행 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(150)  # 고정된 길이로 설정
        self.layout.addWidget(self.progress_bar)

        # 설치 버튼은 진행 바 바로 옆에 고정된 위치로 배치
        self.install_button = QPushButton("라이브러리 설치")
        self.install_button.setEnabled(False)
        self.install_button.setFixedWidth(100)  # 버튼 크기 고정
        self.install_button.clicked.connect(self.install_libraries)
        self.layout.addWidget(self.install_button)

    def get_layout(self):
        return self.layout

    def check_libraries(self):
        # 라이브러리 확인 기능 호출
        success, message = self.installer.check_libraries()
        self.status_label.setText(message)
        if not success:
            self.install_button.setEnabled(True)
        else:
            self.install_button.setEnabled(False)

    def install_libraries(self):
        # 설치 진행 상태 업데이트
        def progress_callback(progress, message):
            truncated_message = (message[:30] + '...') if len(message) > 30 else message  # 메시지 길이 제한
            self.progress_bar.setValue(progress)
            self.status_label.setText(truncated_message)

        # 설치 기능 호출
        self.installer.install_libraries(progress_callback)
        self.install_button.setEnabled(False)  # 설치 완료 후 버튼 비활성화
