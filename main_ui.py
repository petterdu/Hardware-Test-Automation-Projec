import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from UI_folder.cpu_ui import CpuTestUI
from UI_folder.library_install_ui import LibraryInstallerUI
from UI_folder.password_ui import PasswordUI
from UI_folder.gpu_ui import GpuTestUI
from UI_folder.memory_ui import MemoryTestUI
from UI_folder.disk_ui import DiskTestUI
from UI_folder.lan_ui import LanTestUI
from UI_folder.usb_ui import UsbTestUI

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        self.layout = QVBoxLayout()

        # 라이브러리 설치 UI 추가
        self.library_installer_ui = LibraryInstallerUI()
        self.layout.addLayout(self.library_installer_ui.get_layout(), stretch=0)
        self.library_installer_ui.install_callback = self.on_library_check_complete  # 콜백 설정

        # 비밀번호 UI 추가
        self.password_ui = PasswordUI()
        self.layout.addLayout(self.password_ui.get_layout(), stretch=0)

        # CPU 테스트 UI 추가
        self.cpu_test_ui = CpuTestUI()
        self.layout.addLayout(self.cpu_test_ui.get_layout(), stretch=0)
        #self.cpu_test_ui.start_cpu_test_callback = lambda: self.set_buttons_during_test(self.cpu_test_ui)
        self.cpu_test_ui.start_cpu_test_callback = lambda success=False: self.set_buttons_during_test(self.cpu_test_ui, success)

        # GPU 테스트 UI 추가
        self.gpu_test_ui = GpuTestUI()
        self.layout.addLayout(self.gpu_test_ui.get_layout(), stretch=0)
        #self.gpu_test_ui.start_gpu_test_callback = lambda: self.set_buttons_during_test(self.gpu_test_ui)
        self.gpu_test_ui.start_gpu_test_callback = lambda success=False: self.set_buttons_during_test(self.gpu_test_ui, success)

        # 메모리 테스트 UI 추가
        self.memory_test_ui = MemoryTestUI()
        self.layout.addLayout(self.memory_test_ui.get_layout(), stretch=0)
        #self.memory_test_ui.start_memory_test_callback = lambda: self.set_buttons_during_test(self.memory_test_ui)
        self.memory_test_ui.start_memory_test_callback = lambda success=False: self.set_buttons_during_test(self.memory_test_ui, success)


        # 디스크 테스트 UI 추가
        self.disk_test_ui = DiskTestUI()
        self.layout.addLayout(self.disk_test_ui.get_layout(), stretch=0)
        #self.disk_test_ui.start_disk_test_callback = lambda: self.set_buttons_during_test(self.disk_test_ui)
        self.disk_test_ui.start_disk_test_callback = lambda success=False: self.set_buttons_during_test(self.disk_test_ui, success)

        # LAN 포트 테스트 UI 추가
        self.lan_test_ui = LanTestUI()
        self.layout.addLayout(self.lan_test_ui.get_layout(), stretch=0)
        #self.lan_test_ui.start_lan_test_callback = lambda: self.set_buttons_during_test(self.lan_test_ui)
        self.lan_test_ui.start_lan_test_callback = lambda success=False: self.set_buttons_during_test(self.lan_test_ui, success)


        # USB 포트 테스트 UI 추가
        self.usb_test_ui = UsbTestUI()
        self.layout.addLayout(self.usb_test_ui.get_layout(), stretch=0)
        #self.usb_test_ui.start_usb_test_callback = lambda: self.set_buttons_during_test(self.usb_test_ui)
        self.usb_test_ui.start_usb_test_callback = lambda success=False: self.set_buttons_during_test(self.usb_test_ui, success)
        
        
        self.setLayout(self.layout)
        self.setWindowTitle("하드웨어 검사 프로그램 - 메인 UI")

        # 라이브러리 확인 및 설치 시작
        self.library_installer_ui.check_libraries()

    def set_all_buttons_enabled(self, enabled):
        """모든 버튼 활성화 또는 비활성화"""
        self.cpu_test_ui.set_test_buttons_enabled(enabled)
        self.gpu_test_ui.set_test_buttons_enabled(enabled)
        self.memory_test_ui.set_test_buttons_enabled(enabled)
        self.disk_test_ui.set_test_buttons_enabled(enabled)
        self.lan_test_ui.set_test_buttons_enabled(enabled)
        self.usb_test_ui.set_test_buttons_enabled(enabled)

    def set_buttons_during_test(self, active_ui, success):
        """특정 UI의 버튼만 활성화하거나, 테스트 완료 시 복구"""
        if not success:
            # 테스트 중: 모든 버튼 비활성화, 선택된 UI만 활성화
            self.set_all_buttons_enabled(False)
            active_ui.set_test_buttons_enabled(True)
        else:
            # 테스트 완료: 모든 버튼 복구
            self.set_all_buttons_enabled(True)


    def on_library_check_complete(self, success):
        """라이브러리 확인 완료 후 호출"""
        self.set_all_buttons_enabled(success)  # 라이브러리가 설치된 경우만 활성화


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.setGeometry(100, 100, 600, 800)  # 창의 크기와 위치 설정 (너비 600, 높이 800)
    ui.show()
    sys.exit(app.exec_())

