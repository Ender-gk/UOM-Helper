@echo off
chcp 65001 >nul
setlocal
set PYTHONDONTWRITEBYTECODE=1
set "UOM_AI_ENV=%~dp0..\..\UOM-Helper-AI\.venv"
title UOM AI OCR Server
echo ==================================================
echo   UOM 视频培训助手 - AI 验证码引擎正在启动...
echo   服务地址: http://127.0.0.1:8899
echo   请保持此窗口打开！浏览器插件将自动调用此引擎
echo ==================================================
cd /d "%~dp0"
if exist "%UOM_AI_ENV%\Scripts\python.exe" (
  "%UOM_AI_ENV%\Scripts\python.exe" -B uom_ai_server.py
) else (
  python -B uom_ai_server.py
)
if errorlevel 1 echo 启动失败，请检查 Python 环境、requirements.txt 依赖及端口占用。
pause
