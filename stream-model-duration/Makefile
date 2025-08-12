# Set the current datetime tag
LOCAL_TAG := $(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME := stream-model-duration:$(LOCAL_TAG)
FINAL_IMAGE_NAME := ride-predictor-fn:vFinal

# Replace with your actual ACR name
ACR_NAME := mlregistrynairobi
ACR_LOGIN_SERVER := $(ACR_NAME).azurecr.io
ACR_IMAGE_NAME := $(ACR_LOGIN_SERVER)/ride-predictor-fn:latest

SHELL := /bin/bash

.PHONY: all test quality_checks build integration_test publish setup clean

all: integration_test

test:
	pytest integration-test/tests/

quality_checks:
	isort .
	black .
	pylint --recursive=y .

build: quality_checks test
	docker build -t $(LOCAL_IMAGE_NAME) .

integration_test: build
	docker tag $(LOCAL_IMAGE_NAME) $(FINAL_IMAGE_NAME)
	cd integration-test && ./run.sh

publish: build integration_test
	docker tag $(LOCAL_IMAGE_NAME) $(ACR_IMAGE_NAME)
	az acr login --name $(ACR_NAME)
	docker push $(ACR_IMAGE_NAME)
	az functionapp restart --name ride-predictor-fn --resource-group mlflow-rg

setup:
	pipenv install --dev
	pre-commit install

clean:
	- docker image rm $(LOCAL_IMAGE_NAME) $(FINAL_IMAGE_NAME) || true
