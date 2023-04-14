provider "google" {
  project     = var.project_id
  region      = var.region
  ##credentials = file("whiteflag-0.json")
}