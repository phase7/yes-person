# Azure Deployment Design

**Date:** 2026-03-22
**Status:** Approved

## Goal

Make yes-person deployable to Azure via a manual `make` workflow. First step in a multi-cloud deployment strategy (AWS and GCP to follow).

## Decisions

- **Target:** Azure Container Apps
- **Trigger:** Manual — `make az-up` or individual `make az-*` targets
- **IaC:** Terraform (`infra/azure/`) — manages infra only
- **Image lifecycle:** Makefile — handles build, push, deploy
- **Image registry:** Azure Container Registry (ACR)
- **State:** Local `terraform.tfstate` (gitignored); can be promoted to Azure Blob backend later

## Azure Resources (Terraform-managed)

1. **Resource Group** — container for all yes-person Azure resources
2. **Azure Container Registry (ACR)** — stores the Docker image
3. **Container App Environment** — managed hosting environment
4. **Container App** — running yes-person service (port 8000, pulls from ACR)

## Repo Structure Added

```
infra/
  azure/
    main.tf                   # resource definitions
    variables.tf              # configurable inputs
    outputs.tf                # acr_login_server, app_url
    terraform.tfvars.example  # committed; actual .tfvars gitignored
Makefile                      # new az-* targets appended
```

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `prefix` | `"yes-person"` | Prefix for all resource names |
| `location` | `"eastus"` | Azure region |
| `image_tag` | `"latest"` | Container image tag to deploy |

## Makefile Targets

| Target | Purpose |
|--------|---------|
| `az-init` | `terraform -chdir=infra/azure init` |
| `az-apply` | Provision/update infra via Terraform |
| `az-destroy` | Tear down all Azure resources |
| `az-build` | `docker build -t yes-person .` |
| `az-push` | Tag and push image to ACR (reads `acr_login_server` from terraform output) |
| `az-deploy` | `az containerapp update` with latest image — no Terraform needed for routine redeploys |
| `az-up` | Full deploy: `az-apply` + `az-build` + `az-push` + `az-deploy` |

## Image Flow

```
docker build → docker tag → docker push → ACR
                                           ↓
                              az containerapp update (az-deploy)
```

## Security

- ACR credentials wired via Terraform-managed identity grant — no passwords stored in code or config
- `terraform.tfvars` and `terraform.tfstate` gitignored

## .gitignore Additions

```
infra/azure/.terraform/
infra/azure/terraform.tfstate
infra/azure/terraform.tfstate.backup
infra/azure/*.tfvars
```

## Prerequisites (developer machine)

- `az` CLI, logged in (`az login`)
- `docker`
- `terraform`

## Outputs

- `acr_login_server` — consumed by `az-push` Makefile target
- `app_url` — printed after deploy for immediate verification
