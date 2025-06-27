resource "google_cloud_run_v2_service" "default" {
  name                = var.service-name
  location            = var.region
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "europe-west1-docker.pkg.dev/patricio-poc-1/${google_artifact_registry_repository.my-repo.name}/interview"

      dynamic "resources" {
        for_each = var.limits ? [1] : []
        content {
          limits = {
            cpu    = "2"
            memory = "1024Mi"
          }
        }
      }
    }
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  count       = var.public_access == true ? 1 : 0
  location    = var.region
  service     = google_cloud_run_v2_service.default.name
  policy_data = data.google_iam_policy.noauth.policy_data
}

resource "google_artifact_registry_repository" "my-repo" {
  repository_id = var.repo-name
  description   = var.repo-description
  location      = var.region
  format        = "DOCKER"
}