SRC_DIR=./protos
DST_DIR=./src/python/deployments/grpc
VENV=.venv
VERSION=latest

all: clean build check dist


build: build-client build-server


build-api-server: ${VENV} ${DST_DIR}
	docker compose build --pull --progress=quiet api-server

build-api-client: ${VENV} ${DST_DIR}
	docker build . \
		--file=api-client/Dockerfile  \
		--tag=api-client:${VERSION}


build-jenkins-controller:
	docker compose build --pull --progress=quiet jenkins-controller


build-jenkins-node:
	docker compose build --pull --progress=quiet jenkins-node



check:


configure:
	@./configure.sh


clean:


client: build-api-client
	docker run --net=host api-client:${VERSION}


depends: ${VENV}
	${VENV}/bin/poetry install

.PHONY: dist
dist: ${VENV}
	@${VENV}/bin/poetry build

distclean: clean
	@docker compose down --remove-orphans --volumes 2> /dev/null || exit 0
	@rm -rf ${VENV} build


generate: ${VENV} ${DST_DIR}
	@${VENV}/bin/python -m grpc_tools.protoc \
		-I ${SRC_DIR} \
		--python_out=${DST_DIR} \
		--pyi_out=${DST_DIR} \
		--grpc_python_out=${DST_DIR} \
		--descriptor_set_out=${DST_DIR}/deployments.pb \
		--include_imports \
		--include_source_info \
		--openapiv2_out=${DST_DIR} \
			${SRC_DIR}/deployments.proto

install: install-python-package


install-python-package:
	poetry install

get-jenkins-password:
	@grep JENKINS_ADMIN_PASSWORD ./build/env/jenkins.administrator | cut -d '=' -f2


get-vault-token:
	@grep VAULT_DEV_ROOT_TOKEN_ID ./build/env/vault.server | cut -d '=' -f2


reconfigure: distclean configure


start-api-server: build-api-server
	docker compose up --no-recreate --detach api-server


start-jenkins-controller: build-jenkins-controller
	docker compose up --no-recreate --detach jenkins-controller


start-jenkins-node: build-jenkins-node
	docker compose up --no-recreate --detach jenkins-node


stop-api-server:
	docker compose stop api-server


stop-jenkins-controller:
	docker compose stop jenkins-controller


stop-jenkins-node:
	docker compose stop jenkins-node


start: start-jenkins-node start-jenkins-controller start-api-server


stop: stop-api-server stop-jenkins-node stop-jenkins-controller


test: generate
	${VENV}/bin/coverage run
	${VENV}/bin/coverage xml
	${VENV}/bin/coverage report

${DST_DIR}:
	@mkdir -p ${DST_DIR}


${VENV}:
	python3 -m venv ${VENV}
	${VENV}/bin/pip install --upgrade pip poetry
	# .venv/bin/pip install --upgrade pip grpcio-tools jenkins-job-builder jinja2 python-jenkins > /dev/null
