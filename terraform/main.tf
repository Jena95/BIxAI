terraform {
required_version = ">= 1.1.0"


required_providers {
google = {
source = "hashicorp/google"
version = ">= 4.0.0"
}
}
}

provider "google" {
project = var.project_id
region = var.region
zone = var.zone
}

#Enable required APIs

resource "google_project_service" "enabled_apis" {
for_each = toset([
"run.googleapis.com",
"aiplatform.googleapis.com",
"bigquery.googleapis.com",
"secretmanager.googleapis.com",
"cloudbuild.googleapis.com",
"artifactregistry.googleapis.com",
"vpcaccess.googleapis.com",
"compute.googleapis.com",
"logging.googleapis.com",
"monitoring.googleapis.com",
])


project = var.project_id
service = each.key
disable_on_destroy = false
}

# Create service accounts
resource "google_service_account" "backend_sa" {
account_id = "analytics-backend-sa"
display_name = "Analytics Backend Service Account"
project = var.project_id
}


resource "google_service_account" "cicd_sa" {
account_id = "cicd-sa"
display_name = "CI/CD Service Account"
project = var.project_id
}

# Iam bindinngs
locals {
backend_roles = [
"roles/bigquery.jobUser",
"roles/bigquery.dataViewer",
"roles/aiplatform.user",
"roles/secretmanager.secretAccessor",
"roles/logging.logWriter",
]


cicd_roles = [
"roles/run.admin",
"roles/artifactregistry.writer",
"roles/iam.serviceAccountUser",
]
}


resource "google_project_iam_member" "backend_role_bindings" {
for_each = toset(local.backend_roles)
project = var.project_id
role = each.key
member = "serviceAccount:${google_service_account.backend_sa.email}"
}


resource "google_project_iam_member" "cicd_role_bindings" {
for_each = toset(local.cicd_roles)
project = var.project_id
role = each.key
member = "serviceAccount:${google_service_account.cicd_sa.email}"
}

#Artifact Registery

resource "google_artifact_registry_repository" "analytics_repo" {
provider = google
project = var.project_id
location = var.region
repository_id = "analytics-repo"
description = "Docker repo for analytics backend"
format = "DOCKER"
}


# Serverless VPC Access Connector (for Cloud Run to access VPC/private resources)
resource "google_vpc_access_connector" "analytics_connector" {
project = var.project_id
region = var.region
name = "analytics-connector"
ip_cidr_range = var.vpc_connector_cidr
network        = "default"
}

