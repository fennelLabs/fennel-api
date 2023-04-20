module "gce-container" {
  source = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"  # Upgrade the version if necessary.

  container = {
    #image = "https://us-east1-docker.pkg.dev/whiteflag-0/fennel-docker-registry/fennel-api:latest"
    image = "cos-stable-85-13310-1041-0"
  }
}

resource "google_compute_instance" "fennel-api" {
  name         = "fennel-api-instance"
  machine_type = "e2-small"
  zone         = "us-east1-b"
  
  boot_disk {
    initialize_params {
      image = "cos-stable-85-13310-1041-0"
    }
  }

  #metadata_startup_script = "echo Hello, World!"
  metadata_startup_script = "#!/bin/bash\ndocker run us-east1-docker.pkg.dev/whiteflag-0/fennel-docker-registry/fennel-api:latest"
  
  network_interface {
    network = "default"
    access_config {}
  }

 
 metadata = {
    # Required metadata key.
    gce-container-declaration = module.gce-container.metadata_value
    google-logging-enabled    = "true"
    google-monitoring-enabled = "true"
  }
 
  service_account {
    scopes = ["cloud-platform"]
  }
}
