VENV = venv
PY = ./venv/bin/python3
PIP = ./venv/bin/pip
FLASK = ./venv/bin/flask
FLASK_VARS = FLASK_APP=ticket FLASK_ENV=development

.PHONY: test run coverage todo

venv/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

test: venv/bin/activate
	$(PY) -m coverage run -m unittest discover -p "*_test.py" -s "tests/"

instance/ticket.db: test
	$(FLASK_VARS) $(FLASK) init-db 

run: instance/ticket.db
	$(FLASK_VARS) $(FLASK) run

coverage: test
	$(PY) -m coverage report --omit="venv/*,*_test.py" -m

todo:
	find ticket/ -name "*.py" -exec sh -c 'grep "TODO:*" {} | sed "s/^.*# //" ' \;
