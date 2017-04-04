build: check-env
	docker build -t $(DOCKERHUB_REPO)/pylint-server .

push: check-env
	docker push $(DOCKERHUB_REPO)/pylint-server

run: check-env
	docker run --name linter --rm $(DOCKERHUB_REPO)/pylint-server

dev : check-env
	docker run --name linter --rm -p 5000:5000 -v $(PWD)/src:/app/src $(DOCKERHUB_REPO)/pylint-server python pylint_server.py

local:
	cd src && python pylint_server.py

check-env:
ifndef DOCKERHUB_REPO
    $(error DOCKERHUB_REPO is undefined)
endif