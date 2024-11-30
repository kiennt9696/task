# Task Management API

## Requirements

* Docker Compose 1.21.2+
* Python 3.6 +

## Run with Docker Compose

```bash
# building the container
sudo docker-compose build

# starting up a container
sudo docker-compose up
```

## Build the virtual environment

```bash
virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install -r test-requirements.txt
```

## Swagger definition

```http
http://localhost:5002/v1/swagger.json
```

## Health Check

```http
http://localhost:5002/v1/ping
```

## Run app
```html
python -m task
```

## Launch tests
```html
python -m pytest -sv --cov-report xml:test_coverage/coverage.xml  --cov-report term-missing --cov=task task/tests
```

## Build image
```shell
docker image build --network=host --build-arg http_proxy=$(PROXY) --build-arg https_proxy=$(PROXY) --build-arg NO_PROXY=127.0.0.1 -t task-management-api:1.0.0 .
```
### Deploy
```shell
docker-compose up -d
```