@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
echo 创建项目内 Python 环境并安装固定依赖，需要联网访问 PyPI。
if not exist ".venv\Scripts\python.exe" python -m venv .venv
if errorlevel 1 goto failed
".venv\Scripts\python.exe" -m pip --isolated install --index-url https://pypi.org/simple -r requirements.lock.txt
if errorlevel 1 goto failed
".venv\Scripts\python.exe" -m pip check
if errorlevel 1 goto failed
echo 安装完成，请运行 START_AI_SERVER.bat。
pause
exit /b 0
:failed
echo 安装失败。请检查 Python 3.12、网络连接及控制台错误。
pause
exit /b 1
