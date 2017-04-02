build:
	docker build -t ebreton/pylint-server .
	docker push ebreton/pylint-server

run:
	docker run --rm ebreton/pylint-server

dev:
	docker run --rm -v $PWD/pylint_server.py:/app/pylint_server.py -p 5000:5000 ebreton/pylint-server