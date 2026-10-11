@echo off
chcp 65001 >nul
setlocal
set PYTHONDONTWRITEBYTECODE=1
set "UOM_AI_ENV=%~dp0..\..\UOM-Helper-AI\.venv"
cd /d "%~dp0"
echo 在扩展目录外创建 Python 环境并安装固定依赖，需要联网访问 PyPI。
if not exist "%UOM_AI_ENV%\Scripts\python.exe" python -B -m venv "%UOM_AI_ENV%"
if errorlevel 1 goto failed
"%UOM_AI_ENV%\Scripts\python.exe" -B -m pip --isolated install --no-compile --index-url https://pypi.org/simple -r requirements.lock.txt
if errorlevel 1 goto failed
"%UOM_AI_ENV%\Scripts\python.exe" -B -m pip check
if errorlevel 1 goto failed
echo 安装完成，请运行 START_AI_SERVER.bat。
pause
exit /b 0
:failed
echo 安装失败。请检查 Python 3.12、网络连接及控制台错误。
pause
exit /b 1
