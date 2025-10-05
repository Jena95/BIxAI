output "backend_service_account_email" {
value = google_service_account.backend_sa.email
}


output "cicd_service_account_email" {
value = google_service_account.cicd_sa.email
}


output "artifact_registry_repo" {
value = google_artifact_registry_repository.analytics_repo.repository_id
}


output "vpc_connector_name" {
value = google_vpc_access_connector.analytics_connector.name
}
