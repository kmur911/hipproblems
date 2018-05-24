build:
	-docker network create searchrunner_network
	docker-compose build

up: down build
	docker-compose up

down:
	docker-compose down

test:
	docker build -t searchrunner/test tests
	docker run --rm --network searchrunner_network searchrunner/test python -m scraperapi_test

clean: down
	-docker rmi searchrunner/scraper
	-docker rmi searchrunner/aggregator
	-docker rmi searchrunner/test
	-docker network rm searchrunner_network
	