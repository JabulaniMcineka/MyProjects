# Deploying to Azure App Service (Free Tier)

## Prerequisites
- Azure account (free at portal.azure.com)
- Azure CLI installed: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
- Docker Desktop running

## Step 1 — Login to Azure
```bash
az login
```

## Step 2 — Create a Resource Group
```bash
az group create --name health-analytics-rg --location southafricanorth
```

## Step 3 — Create an Azure Container Registry
```bash
az acr create --resource-group health-analytics-rg \
  --name healthanalyticsregistry \
  --sku Basic \
  --admin-enabled true
```

## Step 4 — Build & Push Docker Image
```bash
# Login to registry
az acr login --name healthanalyticsregistry

# Build image
docker build -t health-analytics-api .

# Tag image
docker tag health-analytics-api healthanalyticsregistry.azurecr.io/health-analytics-api:v1

# Push image
docker push healthanalyticsregistry.azurecr.io/health-analytics-api:v1
```

## Step 5 — Create App Service Plan (Free Tier)
```bash
az appservice plan create \
  --name health-analytics-plan \
  --resource-group health-analytics-rg \
  --sku B1 \
  --is-linux
```

## Step 6 — Deploy Web App
```bash
az webapp create \
  --resource-group health-analytics-rg \
  --plan health-analytics-plan \
  --name health-analytics-api \
  --deployment-container-image-name healthanalyticsregistry.azurecr.io/health-analytics-api:v1
```

## Step 7 — Your API is live!
```
https://health-analytics-api.azurewebsites.net
https://health-analytics-api.azurewebsites.net/docs
```

## Update after code changes
```bash
docker build -t health-analytics-api .
docker tag health-analytics-api healthanalyticsregistry.azurecr.io/health-analytics-api:v1
docker push healthanalyticsregistry.azurecr.io/health-analytics-api:v1
az webapp restart --name health-analytics-api --resource-group health-analytics-rg
```
