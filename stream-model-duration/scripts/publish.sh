#!/usr/bin/env bash

# Replace with your actual ACR name
ACR_NAME=mlregistrynairobi
IMAGE_NAME=stream-model-duration
TAG=latest

FULL_IMAGE_NAME=${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${TAG}

echo "publishing image ${LOCAL_IMAGE_NAME} to ACR..."

# Tag the local image
docker tag ${LOCAL_IMAGE_NAME} ${FULL_IMAGE_NAME}

# Login to ACR
az acr login --name ${ACR_NAME}

# Push to ACR
docker push ${FULL_IMAGE_NAME}

echo "✅ Image pushed to Azure Container Registry: ${FULL_IMAGE_NAME}"
