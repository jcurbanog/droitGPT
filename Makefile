.PHONY: run-backend run-frontend run

run-backend:
	. venv/bin/activate && python backend/api.py
run-frontend:
	cd app && ng serve

run:
	npm start
