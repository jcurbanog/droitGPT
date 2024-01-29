.PHONY: run-backend run-frontend run python-format

run-backend:
	. backend/venv/bin/activate && python backend/api.py
python-format:
	. backend/venv/bin/activate && isort --profile black . && black -t 'py310' --line-length=100 .

run-frontend:
	cd app && npm install && ng serve

run:
	npm start && npm install
