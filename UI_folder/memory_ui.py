from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt5.QtCore import QThread
from functions.memory_test_function import MemoryTestWorker

class MemoryTestUI:
    def __init__(self):
        self.layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        # 메모리 관련 불량 테스트 수평 레이아웃 설정
        horizontal_layout = QHBoxLayout()

        # 메모리 관련 불량 테스트 제목 라벨 추가
        self.add_memory_test_title_label(horizontal_layout, "메모리 관련 불량 테스트")

        # 버튼들을 수직 레이아웃에 추가하여 제목 라벨 오른쪽에 배치
        button_layout = QVBoxLayout()
        self.add_memory_test_button(button_layout, "Memtester 불량 테스트", "Memtester 테스트 결과", self.start_memtester_test, test_type="memtester")
        self.add_memory_test_button(button_layout, "Stress-ng 불량 테스트", "Stress-ng 테스트 결과", self.start_stress_test, test_type="stress")

        # 수평 레이아웃에 버튼 레이아웃 추가
        horizontal_layout.addLayout(button_layout)

        # 전체 레이아웃에 수평 레이아웃 추가
        self.layout.addLayout(horizontal_layout)

    def get_layout(self):
        return self.layout

    def add_memory_test_title_label(self, layout, label_text):
        # 제목 라벨을 생성하여 버튼처럼 보이도록 스타일 적용
        title_label = QLabel(label_text)
        title_label.setStyleSheet("""
            background-color: #d3d3d3;  /* 밝은 회색 배경색 */
            border: 2px solid #000000;  /* 검은색 테두리 */
            padding: 10px;              /* 안쪽 여백 */
            border-radius: 5px;         /* 둥근 모서리 */
            font-weight: bold;          /* 텍스트 굵게 */
            font-size: 14px;            /* 텍스트 크기 */
        """)
        title_label.setFixedHeight(100)  # 라벨의 높이 설정
        title_label.setFixedWidth(150)  # 라벨의 너비 설정
        layout.addWidget(title_label)

    def add_memory_test_button(self, layout, button_text, label_text, callback=None, test_type=None):
        horizontal_layout = QHBoxLayout()

        button = QPushButton(button_text)
        button.setEnabled(False)
        button.setFixedHeight(40)
        if callback:
            button.clicked.connect(lambda: callback(test_type))
        horizontal_layout.addWidget(button)

        if test_type == "memtester":
            self.memtester_button = button
        elif test_type == "stress":
            self.stress_button = button

        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setFixedWidth(150)
        horizontal_layout.addWidget(progress_bar)

        if test_type == "memtester":
            self.memtester_progress_bar = progress_bar
        elif test_type == "stress":
            self.stress_progress_bar = progress_bar

        result_label = QLabel(label_text)
        horizontal_layout.addWidget(result_label)

        if test_type == "memtester":
            self.memtester_result_label = result_label
        elif test_type == "stress":
            self.stress_result_label = result_label

        layout.addLayout(horizontal_layout)

    def start_memtester_test(self, test_type):
        # Memtester 테스트 시작
        self.start_memory_test(test_type)

    def start_stress_test(self, test_type):
        # Stress-ng 테스트 시작
        self.start_memory_test(test_type)

    def start_memory_test(self, test_type):
        # 모든 테스트 버튼 비활성화 콜백 호출
        if hasattr(self, 'start_memory_test_callback'):
            self.start_memory_test_callback(False)

        # QThread 및 Worker 설정
        self.thread = QThread()
        self.worker = MemoryTestWorker(test_type=test_type)

        # Worker를 쓰레드에 연결
        self.worker.moveToThread(self.thread)

        # 시그널과 슬롯 연결
        self.thread.started.connect(self.worker.run_memory_test)
        self.worker.progress_signal.connect(lambda progress: self.update_memory_progress(progress, test_type))
        self.worker.result_signal.connect(lambda result: self.update_memory_result(result, test_type))
        self.worker.result_signal.connect(lambda: self.set_test_buttons_enabled(True))
        self.worker.result_signal.connect(lambda: self.start_memory_test_callback(True))  # 테스트가 끝나면 버튼 활성화
        self.worker.result_signal.connect(self.thread.quit)

        # 쓰레드 시작
        self.thread.start()

    def update_memory_progress(self, progress, test_type):
        if test_type == "memtester" and hasattr(self, 'memtester_progress_bar'):
            self.memtester_progress_bar.setValue(progress)
        elif test_type == "stress" and hasattr(self, 'stress_progress_bar'):
            self.stress_progress_bar.setValue(progress)

    def update_memory_result(self, result, test_type):
        if test_type == "memtester" and hasattr(self, 'memtester_result_label'):
            if result == "success":
                self.memtester_result_label.setText("Memtester 테스트 통과!")
                self.memtester_result_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.memtester_result_label.setText("테스트 실패")
                self.memtester_result_label.setStyleSheet("color: red; font-weight: bold;")
        elif test_type == "stress" and hasattr(self, 'stress_result_label'):
            if result == "success":
                self.stress_result_label.setText("Stress-ng 테스트 통과!")
                self.stress_result_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.stress_result_label.setText("테스트 실패")
                self.stress_result_label.setStyleSheet("color: red; font-weight: bold;")

    def set_test_buttons_enabled(self, enabled):
        if hasattr(self, 'memtester_button'):
            self.memtester_button.setEnabled(enabled)
        if hasattr(self, 'stress_button'):
            self.stress_button.setEnabled(enabled)

