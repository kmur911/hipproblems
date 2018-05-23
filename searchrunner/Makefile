build:
	docker-compose build

up: down build
	docker-compose up

down:
	docker-compose down

test:
	docker build . -t searchrunner/base
	docker run searchrunner/base --rm --net="host" python -m searchrunner.scraperapi_test

clean: down
	docker rmi searchrunner/base
	