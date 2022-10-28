# Quick Start

This repository contains a Docker Compose project that:
 
- Starts a Vault instance w/ project secrets (`localhost:8200`)
- Starts a Jenkins controllers configured with JcasC+Vault  (`localhost:8080`)
- Starts a Deployments API server (Python gRPC) (`localhost:50051`)
- Creates a build job for this projects local repository folder (`./`)
- Creates a build job for this projects GitHub repository (`origin`)
- Creates a Dockerized Deployments API client (Python gRPC)

At this time, the client (`make client`) simply calls `CreateDeployment`, `QueueDeployment`, and `DeleteDeployment`, which uses the Jenkins API as its deployment backend.

## Requirements

- Docker (https://docs.docker.com/get-docker/)
- Python 3 (`brew install python3`)
- Protobuf (`brew install protobuf`)
- Go/protoc-gen-openapiv2 (`brew install go;go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2@latest`)

## Configure Secrets and Services

If you would like to build the GitHub source and avoid the GitHub API limits, you can configure the GitHub API username and access token:

```bash
% export GITHUB_USERNAME=<your-github-username>
% export GITHUB_ACCESS_TOKEN=<your-github-peronal-access-token>
```

Then run the configuration script to generate the required services configuration and secrets

```bash
% make configure

Creating build folder               [build]
Creating env files folder           [build/env]
Creating logs folder                [build/logs]
Creating ssh folder                 [build/ssh]
Creating Vault root token           [build/env/vault.server: VAULT_DEV_ROOT_TOKEN_ID]
Creating Jenkins admin password     [build/env/jenkins.administrator: JENKINS_ADMIN_USERNAME]
Creating Jenkins controller config  [build/env/jenkins.controller]
Creating Jenkins node config        [build/env/jenkins.node]
Generating Jenkins SSH keys         [build/ssh/jenkins/id_rsa]
Starting/Restarting Vault           [vault: http://localhost:8200]
Loading Jenkins admin credentuals   [vault: cubbyhole/ssh/jenkins]
Loading Jenkins ssh keys            [vault: cubbyhole/jenkins/admininistrator]
Loading GitHub API credentials      [vault: cubbyhole/github]
```

Configurations, keys, and secrets will be placed in the relevant `./build/` folders:

```bash
% tree build

build
├── env
│   ├── jenkins.administrator
│   ├── jenkins.controller
│   ├── jenkins.node
│   └── vault.server
└── ssh
    └── jenkins
        ├── id_rsa
        └── id_rsa.pub
```

Configurations, keys, and secrets are loaded into Vault in the `cubbyhole` secrets store for the generated Vault token:

```bash
% vault kv list cubbyhole/

Keys
----
github
jenkins/administrator
ssh/jenkins
```

## Start/Stop Services

Start/Stop all remaining services:

```bash
% make start
% make stop
```

## Login to Jenkins

```bash
% make get-jenkins-password | pbcopy
% open http://localhost:8080
```

## Login to Vault

```bash
% make get-vault-token | pbcopy
% open http://localhost:8200
```

## Running the Client

Run the command line client:

```bash
# in the Docker image
% docker run --net=host api-client --help

# or locally in Python
% source .venv/bin/activate
% deployctl --help
...
```

## Running the Service

Run the service:

```bash
# in the Docker image
% docker run -ti api-server

# or locally in Python
% source .venv/bin/activate
% deployctl service run
```
