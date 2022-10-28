.DEFAULT_GOAL := help
.PHONY: clean configure help lint login start stop

ROOT       := .
DISTDIR    := ${ROOT}/dist
BINDIR     := ${DISTDIR}/bin
LOGDIR     := ${DISTDIR}/logs
SECRETSDIR := ${DISTDIR}/secrets

${LOGDIR}:
	@mkdir -p "$@"

${SECRETSDIR}:
	@mkdir -p "$@"

${SECRETSDIR}/password: ${SECRETSDIR}
	@SECRETSDIR="${SECRETSDIR}" ./configure.sh

build: ## build containers
build:
	@docker compose build

bump:
	@pre-commit autoupdate

configure: ## configure project secrets
configure: ${LOGDIR} ${SECRETSDIR}
	@SECRETSDIR="${SECRETSDIR}" ./configure.sh

clean: ## clean project
clean:
	@${RM} -rf "${BINDIR}" "${DISTDIR}" "${SECRETSDIR}"
	@docker compose down --remove-orphans --volumes
	@pipx run pre-commit clean &> /dev/null && pipx run pre-commit gc &> /dev/null && pipx run pre-commit uninstall &> /dev/null

help: ## display this help
help:
	@echo "Usage: make [target] [argument=value] ..."
	@echo
	@egrep "^(.+)\:\s+##\ (.+)" ${MAKEFILE_LIST} | column -t -c 2 -s ":#"
	@echo

lint: ## lint project files
lint:
	@pipx run pre-commit run --all

login: ## open login
login:
	@open http://localhost:8080

start: ## start services
start: ${SECRETSDIR}/password ${LOGDIR}
	@docker compose up --build --detach

stop: ## stop services
stop:
	@docker compose down --remove-orphans --volumes
