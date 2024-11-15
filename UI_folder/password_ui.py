from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import os

class PasswordUI:
    def __init__(self):
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)  # 수평 레이아웃을 좌측 정렬로 설정
        self.password_file_path = os.path.join(os.getcwd(), 'functions/scripts/password.txt')
        self.initUI()

    def initUI(self):
        # 비밀번호 초기화
        self.init_password()

        # 비밀번호 입력 UI 설정
        self.password_label = QLabel("비밀번호: ")
        self.password_label.setFixedWidth(60)  # 라벨 너비 고정
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # 비밀번호 입력 시 숨김
        self.password_input.setFixedWidth(150)  # 입력 필드의 너비 설정
        self.layout.addWidget(self.password_input)

        # password.txt 파일에서 비밀번호 읽어오기
        try:
            with open(self.password_file_path, 'r') as file:
                saved_password = file.read().strip()
                self.password_input.setText(saved_password)
        except Exception as e:
            print("비밀번호 파일 읽기 중 오류 발생: {}".format(str(e)))

        self.password_confirm_button = QPushButton("확인")
        self.password_confirm_button.setFixedWidth(80)  # 버튼 너비 고정
        self.password_confirm_button.clicked.connect(self.update_password)
        self.layout.addWidget(self.password_confirm_button)

    def get_layout(self):
        return self.layout

    def init_password(self):
        default_password = "cona"
        if not os.path.exists(self.password_file_path) or os.stat(self.password_file_path).st_size == 0:
            try:
                with open(self.password_file_path, 'w') as file:
                    file.write(default_password)
            except Exception as e:
                print("비밀번호 파일 생성 중 오류 발생: {}".format(str(e)))

    def update_password(self):
        # 입력된 비밀번호를 password.txt에 반영
        password = self.password_input.text()
        try:
            # 파일에 비밀번호 저장
            with open(self.password_file_path, 'w') as file:
                file.write(password)
                print("비밀번호가 업데이트되었습니다.")
        except Exception as e:
            print(f"비밀번호 업데이트 중 오류 발생: {str(e)}")

