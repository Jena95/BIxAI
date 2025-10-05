variable "project_id" {
description = "GCP project id where resources will be created"
type = string
}


variable "region" {
description = "GCP region to create regional resources in"
type = string
default = "us-central1"
}


variable "zone" {
description = "GCP zone (optional)"
type = string
default = "us-central1-a"
}


variable "vpc_connector_cidr" {
description = "CIDR range to allocate for the Serverless VPC connector (small /28 recommended)"
type = string
default = "10.8.0.0/28"
}
