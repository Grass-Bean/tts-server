@echo off
call .venv\Scripts\Activate
uv run client.py
deactivate