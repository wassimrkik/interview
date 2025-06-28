terraform {
  backend "gcs" {
    bucket = "interview-tfstate-1"
    prefix = "terraform/state-interview"
  }
}
