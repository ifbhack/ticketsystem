VENV = venv
PY = ./venv/bin/python3
PIP = ./venv/bin/pip
FLASK = ./venv/bin/flask
FLASK_VARS = FLASK_APP=ticket FLASK_ENV=development

venv/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

instance/flaskr.sqlite:
	$(FLASK_VARS) $(FLASK) init-db 

run: venv/bin/activate instance/ticket.db
	$(FLASK_VARS) $(FLASK) run

test: venv/bin/activate
	$(PY) -m unittest discover -p "*_test.py"
