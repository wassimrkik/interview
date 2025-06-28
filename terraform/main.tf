resource "google_cloud_run_v2_service" "default" {
  name                = var.service-name
  location            = var.region
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "europe-west1-docker.pkg.dev/${var.project}/${var.service-name}/interview"
      env {
        name = "OPEN_API_KEY"
        value_source {
          secret_key_ref {
            secret  = "api_key"
            version = "latest"
          }
        }
      }

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

resource "google_secret_manager_secret" "secret" {
  secret_id = "api_key"
  replication {
    auto {

    }
  }
}

resource "google_secret_manager_secret_version" "default" {
  secret      = google_secret_manager_secret.secret.id
  secret_data = var.api-key
}

data "google_project" "project" {
}

resource "google_secret_manager_secret_iam_member" "secret-access" {
  secret_id  = google_secret_manager_secret.secret.id
  role       = "roles/secretmanager.secretAccessor"
  member     = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  depends_on = [google_secret_manager_secret.secret]
}
