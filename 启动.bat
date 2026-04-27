@echo off
echo ========================================
echo   知晓智能家居客服 - 启动中...
echo ========================================
echo.

echo [1/2] 设置 API Key...
set DASHSCOPE_API_KEY=sk-f15f35b5d91e424bba6eed6acfecab5a

echo [2/2] 启动服务...
echo.

D:\Anaconda\envs\pytorch\python.exe -m streamlit run app.py

pause
