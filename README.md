# Terraform: GCP Infra for Analytics Assistant (Step 1)


This Terraform bundle provisions the Step 1 baseline infra for the Natural Language Business Analytics Assistant on GCP.


## What it creates
- Enables required APIs
- Creates two service accounts: `analytics-backend-sa`, `cicd-sa`
- Grants recommended IAM roles at the project level (adjust for least privilege)
- Artifact Registry repository (`analytics-repo`)
- Serverless VPC Access Connector (`analytics-connector`)
- Secret Manager secret `my-external-api-key` with one version


## Usage
1. Install Terraform (>= 1.1)
2. Authenticate: `gcloud auth application-default login` OR set `GOOGLE_APPLICATION_CREDENTIALS` to a JSON key
3. Create a terraform.tfvars with at minimum:


```
project_id = "your-gcp-project-id"
region = "us-central1"
example_secret_value = "my-secret-value"
```


4. Initialize & apply:


```
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

_________________________

pip install -r requirements.txt

test in local:

uvicorn app.main:app --reload

You can also chec: curl http://127.0.0.1:8000/api/
