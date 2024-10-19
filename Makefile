default:
	@echo "Targets include: test, collectstatic"

build:
	docker compose build

up:
	docker compose up -d

build_up:
	docker compose up -d --build

down:
	docker compose down -v