#!/bin/bash

# 현재 스크립트의 절대 경로 계산 (심볼릭 링크도 정확히 처리)
SCRIPT_PATH="$(realpath "$0")"
PROJECT_PATH="$(dirname "$SCRIPT_PATH")"
DESKTOP_PATH="$HOME/Desktop"  # 바탕화면 경로
LAUNCHER_NAME="hardware_test_launcher.desktop"

# main_ui.py의 절대 경로
MAIN_UI_PATH="$PROJECT_PATH/main_ui.py"

# 아이콘 경로 설정 (원하는 아이콘으로 변경 가능)
ICON_PATH="/usr/share/icons/hicolor/48x48/apps/python.png"

# main_ui.py 경로가 실제 존재하는지 확인
if [[ ! -f "$MAIN_UI_PATH" ]]; then
  echo "Error: $MAIN_UI_PATH does not exist. Please check the script location."
  exit 1
fi

# .desktop 파일 생성
echo "[Desktop Entry]
Version=1.0
Type=Application
Name=Hardware Test Automation
Comment=Run hardware test automation UI
Exec=python3 $MAIN_UI_PATH
Icon=$ICON_PATH
Terminal=false
Categories=Utility;Application;" > "$DESKTOP_PATH/$LAUNCHER_NAME"

# 실행 권한 부여
chmod +x "$DESKTOP_PATH/$LAUNCHER_NAME"

# .desktop 파일을 신뢰할 수 있는 파일로 설정
gio set "$DESKTOP_PATH/$LAUNCHER_NAME" metadata::trusted true 2>/dev/null || \
echo "바탕화면 관리자가 gio를 지원하지 않으면 수동으로 파일을 실행 가능하도록 설정해 주세요."

# 완료 메시지
echo "Launcher created successfully at: $DESKTOP_PATH/$LAUNCHER_NAME"
echo "바탕화면에서 아이콘을 더블클릭하면 프로그램이 실행됩니다."

