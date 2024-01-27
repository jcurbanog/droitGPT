.PHONY: run-backend run-frontend run

run-backend:
	. venv/bin/activate && python backend/api.py
python-format:
	isort --profile black .
	black -t 'py310' --line-length=100 .

run-frontend:
	cd app && npm install && ng serve

run:
	npm start && npm install
