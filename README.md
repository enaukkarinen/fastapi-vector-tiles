https://github.com/igorbenav/FastAPI-boilerplate/tree/main/src/app/core

https://github.com/StefanVDWeide/fastapi-api-template/tree/master/app

fastapi dev app/main.py
uv pip install -r pyproject.toml
uv run fastapi dev app/main.py
uv run ruff check

http://127.0.0.1:8000/vectors/1/2/3




For those using a venv created with uv venv:

    Open the Command Palette (shift + apple + p)
    select "Python: Select Interpreter"
    select the python version at .venv/bin/python

This works with the VSCode debugger