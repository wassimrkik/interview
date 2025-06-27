variable "region" {
  default = "europe-west1"
}

variable "limits" {
  default = false
}
variable "service-name" {
  default = "interview"
}

variable "public_access" {
  default = true
}

variable "repo-name" {
  default = "interview"
}

variable "repo-description" {
  default = "a repo to test deployment"
}

variable "api-key" {
  type = string
  default = "check tfvars"
}