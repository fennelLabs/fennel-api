module "gce-container" {
  source = "terraform-google-modules/container-vm/google"
  version = "~> 2.0" 

  container = {
    image = "ubuntu-os-cloud/ubuntu-2004-lts"
  }
}

resource "google_storage_bucket_object" "startup" {
  name   = "fennel-api-terraform-start.sh"
  bucket = "whiteflag-0-admin"
  source = "fennel-api-terraform-start.sh"

  content_type = "text/plain"
}


resource "google_compute_address" "fennel-api-ip" {
  name = "fennel-api-ip"
}

resource "google_compute_instance" "fennel-api" {
  name         = "fennel-api-instance"
  machine_type = "e2-small"
  zone         = "us-east1-b"

  can_ip_forward = true
  tags = ["public-server"]
  
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network    = "whiteflag-sandbox-vpc"
    subnetwork = "public-subnet"
     access_config {
      nat_ip = google_compute_address.fennel-api-ip.address
    }
  }

 metadata = {
    startup-script-url = "gs://whiteflag-0-admin/fennel-api-terraform-start.sh"
    gce-container-declaration = module.gce-container.metadata_value
    google-logging-enabled    = "true"
    google-monitoring-enabled = "true"
  }
 
  service_account {
    scopes = ["cloud-platform"]
  }
}
