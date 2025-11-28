format:
	@./backend/.venv/bin/black .
	@./backend/.venv/bin/ruff check --fix .