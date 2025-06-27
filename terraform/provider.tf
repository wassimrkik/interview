provider "google" {
  project = "patricio-poc-1"
  region  = "europe-west9"
  #zone        = "europe-west9-a"
}

provider "google-beta" {
  project = "patricio-poc-1"
}