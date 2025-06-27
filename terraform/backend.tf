terraform {
  backend "gcs" {
    bucket = "wassim-test-1"
    prefix = "terraform/state-interview"
  }
}
