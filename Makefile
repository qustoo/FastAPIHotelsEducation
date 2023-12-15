create_env:
	@echo "Creating  virtual environment..."
	python -m venv venv
	.\venv\Scripts\activate
	@echo "Virtual environment created"
install_depends:
	@echo "Installing dependencies..."
	pip install -r .\requirements.txt
	@echo "Done"
migrate:
	@echo "Running migration..."
	pyhon -m alembic check
	python -m alembic upgrade head
black:
	python -m black .
flake8:
	python -m flake8 .
isort:
	python -m isort
up:
	docker-compose -f docker-compose.yml up -dependencies
down:
	docker-compose -f docker-compose.yml down
run:
	@echo "Running the app..."
	uvicorn app.main:app --reload --port 8000 