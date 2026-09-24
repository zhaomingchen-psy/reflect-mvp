#!/bin/bash
# PsyCLIENT MVP 一键启动：双击本文件即可
cd "$(dirname "$0")"
( sleep 1.5 && open http://localhost:8000 ) &
echo "PsyCLIENT MVP 启动中… 浏览器将自动打开 http://localhost:8000"
echo "关闭：在本窗口按 Ctrl+C，或直接关掉这个终端窗口"
python3 server.py
