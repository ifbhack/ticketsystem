VENV = venv
PY = ./venv/bin/python3
PIP = ./venv/bin/pip

venv/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

test: venv/bin/activate
	$(PY) -m unittest discover -p "*_test.py"
