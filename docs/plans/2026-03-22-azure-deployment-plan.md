# Azure Deployment Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deploy yes-person to Azure Container Apps via a manual `make az-up` workflow backed by Terraform-managed infrastructure.

**Architecture:** Terraform provisions a Resource Group, ACR, managed identity, Log Analytics workspace, Container App Environment, and Container App. The Makefile handles the image lifecycle (build → push → deploy). `az-apply` is idempotent infra management; `az-deploy` handles routine redeployments without re-running Terraform.

**Tech Stack:** Terraform (azurerm ~3.0, random providers), Azure Container Apps, Azure Container Registry, az CLI, Docker, Make.

---

### Task 1: Add Terraform entries to .gitignore

**Files:**
- Modify: `.gitignore`

**Step 1: Append Terraform ignores**

Add these lines to `.gitignore`:

```
# Terraform
infra/azure/.terraform/
infra/azure/.terraform.lock.hcl
infra/azure/terraform.tfstate
infra/azure/terraform.tfstate.backup
infra/azure/*.tfvars
```

**Step 2: Verify the file looks correct**

Run: `cat .gitignore`
Expected: existing entries plus the five new Terraform lines at the bottom.

**Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: gitignore terraform state and local tfvars"
```

---

### Task 2: Create infra/azure/variables.tf

**Files:**
- Create: `infra/azure/variables.tf`

**Step 1: Create the directory and file**

```bash
mkdir -p infra/azure
```

Create `infra/azure/variables.tf` with this exact content:

```hcl
variable "prefix" {
  description = "Prefix for all Azure resource names (hyphens stripped from ACR name)"
  type        = string
  default     = "yes-person"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "container_image" {
  description = "Initial container image. Use az-deploy to update after first push."
  type        = string
  default     = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
}
```

**Step 2: Verify file exists**

Run: `cat infra/azure/variables.tf`
Expected: file contents printed without error.

---

### Task 3: Create infra/azure/main.tf

**Files:**
- Create: `infra/azure/main.tf`

**Step 1: Create the file**

Create `infra/azure/main.tf` with this exact content:

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Random suffix so ACR name is globally unique
resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.prefix}-rg"
  location = var.location
}

resource "azurerm_container_registry" "acr" {
  name                = "${replace(var.prefix, "-", "")}${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = false
}

resource "azurerm_user_assigned_identity" "app_identity" {
  name                = "${var.prefix}-identity"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
}

resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_user_assigned_identity.app_identity.principal_id
}

resource "azurerm_log_analytics_workspace" "logs" {
  name                = "${var.prefix}-logs"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "env" {
  name                       = "${var.prefix}-env"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.logs.id
}

resource "azurerm_container_app" "app" {
  name                         = var.prefix
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app_identity.id]
  }

  registry {
    server   = azurerm_container_registry.acr.login_server
    identity = azurerm_user_assigned_identity.app_identity.id
  }

  template {
    container {
      name   = "yes-person"
      image  = var.container_image
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}
```

**Step 2: Initialize and validate**

Run: `terraform -chdir=infra/azure init`
Expected: "Terraform has been successfully initialized!"

Run: `terraform -chdir=infra/azure validate`
Expected: "Success! The configuration is valid."

---

### Task 4: Create infra/azure/outputs.tf

**Files:**
- Create: `infra/azure/outputs.tf`

**Step 1: Create the file**

Create `infra/azure/outputs.tf` with this exact content:

```hcl
output "acr_login_server" {
  description = "ACR login server hostname (used by az-push)"
  value       = azurerm_container_registry.acr.login_server
}

output "acr_name" {
  description = "ACR registry name (used by az acr login)"
  value       = azurerm_container_registry.acr.name
}

output "app_name" {
  description = "Container App name (used by az-deploy)"
  value       = azurerm_container_app.app.name
}

output "resource_group_name" {
  description = "Resource group name (used by az-deploy)"
  value       = azurerm_resource_group.rg.name
}

output "app_url" {
  description = "Public HTTPS URL of the deployed app"
  value       = "https://${azurerm_container_app.app.ingress[0].fqdn}"
}
```

**Step 2: Validate again**

Run: `terraform -chdir=infra/azure validate`
Expected: "Success! The configuration is valid."

---

### Task 5: Create infra/azure/terraform.tfvars.example

**Files:**
- Create: `infra/azure/terraform.tfvars.example`

**Step 1: Create the file**

Create `infra/azure/terraform.tfvars.example` with this exact content:

```hcl
# Copy this file to terraform.tfvars and edit as needed.
# terraform.tfvars is gitignored — never commit it.

# prefix    = "yes-person"   # change if deploying multiple environments
# location  = "eastus"       # az account list-locations --output table
```

**Step 2: Verify it is committed but .tfvars is ignored**

The `.gitignore` entry `infra/azure/*.tfvars` will ignore `terraform.tfvars` but NOT `terraform.tfvars.example` (no wildcard match). Verify:

Run: `git check-ignore infra/azure/terraform.tfvars.example`
Expected: no output (file is NOT ignored — correct, it should be committed).

Run: `git check-ignore infra/azure/terraform.tfvars`
Expected: `infra/azure/terraform.tfvars` (file IS ignored — correct).

**Step 3: Commit Terraform infra files**

```bash
git add infra/azure/variables.tf infra/azure/main.tf infra/azure/outputs.tf infra/azure/terraform.tfvars.example
git commit -m "feat: add Terraform infra for Azure Container Apps"
```

Note: Do NOT add `infra/azure/.terraform/` or `infra/azure/.terraform.lock.hcl` — the `.terraform/` directory is gitignored, but `.terraform.lock.hcl` is typically committed to pin provider versions. Add it:

```bash
git add infra/azure/.terraform.lock.hcl
git commit -m "chore: commit terraform provider lock file"
```

---

### Task 6: Add az-* targets to Makefile

**Files:**
- Modify: `Makefile`

**Step 1: Append the new targets**

The existing `Makefile` ends at line 26 (`docker-up`). Append the following after the last target.

First, update the `.PHONY` line at the top to include the new targets:

Old line 1:
```makefile
.PHONY: dev test test-update lint format install docker-build docker-up
```

New line 1:
```makefile
.PHONY: dev test test-update lint format install docker-build docker-up az-init az-apply az-destroy az-build az-push az-deploy az-up
```

Then append after line 26:

```makefile

# Azure deployment targets
# Prerequisites: az CLI (logged in), docker, terraform

az-init:
	terraform -chdir=infra/azure init

az-apply:
	terraform -chdir=infra/azure apply

az-destroy:
	terraform -chdir=infra/azure destroy

az-build:
	docker build -t yes-person .

az-push:
	$(eval ACR_SERVER := $(shell terraform -chdir=infra/azure output -raw acr_login_server))
	$(eval ACR_NAME := $(shell terraform -chdir=infra/azure output -raw acr_name))
	az acr login --name $(ACR_NAME)
	docker tag yes-person $(ACR_SERVER)/yes-person:latest
	docker push $(ACR_SERVER)/yes-person:latest

az-deploy:
	$(eval ACR_SERVER := $(shell terraform -chdir=infra/azure output -raw acr_login_server))
	$(eval APP_NAME := $(shell terraform -chdir=infra/azure output -raw app_name))
	$(eval RG_NAME := $(shell terraform -chdir=infra/azure output -raw resource_group_name))
	az containerapp update \
		--name $(APP_NAME) \
		--resource-group $(RG_NAME) \
		--image $(ACR_SERVER)/yes-person:latest
	@echo "App URL: $$(terraform -chdir=infra/azure output -raw app_url)"

az-up: az-apply az-build az-push az-deploy
```

**Step 2: Verify make can parse the file**

Run: `make --dry-run az-build`
Expected: prints `docker build -t yes-person .` without errors.

**Step 3: Commit**

```bash
git add Makefile
git commit -m "feat: add az-* Makefile targets for Azure deployment"
```

---

### Task 7: End-to-end smoke test (requires Azure login)

This task validates the full deploy flow. Skip if you don't have Azure credentials available yet.

**Prerequisites:**
- `az login` (or `az login --use-device-code` for headless)
- `az account set --subscription <your-subscription-id>` if you have multiple subscriptions
- Docker daemon running

**Step 1: Initialize Terraform**

Run: `make az-init`
Expected: providers downloaded, "Terraform has been successfully initialized!"

**Step 2: Preview the infra plan**

Run: `terraform -chdir=infra/azure plan`
Expected: plan shows ~8 resources to create, no errors.

**Step 3: Provision infra**

Run: `make az-apply`
Expected: Terraform applies ~8 resources. Takes ~3-5 minutes. Ends with outputs printed.

**Step 4: Build and push image**

Run: `make az-build az-push`
Expected: Docker build completes, `az acr login` succeeds, image pushed.

**Step 5: Deploy**

Run: `make az-deploy`
Expected: Container App updated, app URL printed.

**Step 6: Verify**

Run: `curl $(terraform -chdir=infra/azure output -raw app_url)/health`
Expected: `{"status":"ok"}`

**Step 7: Tear down (if this was a test run)**

Run: `make az-destroy`
Expected: all Azure resources deleted.
