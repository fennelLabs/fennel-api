module "gce-container" {
  source = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"  # Upgrade the version if necessary.

  container = {
    image = "us-east1-docker.pkg.dev/whiteflag-0/fennel-docker-registry/fennel-api:latest"
  }
}

resource "google_compute_instance" "fennel-api" {
  name         = "fennel-api-instance"
  machine_type = "e2-small"
  zone         = "us-east1-b"
  
  boot_disk {
    initialize_params {
      image = module.gce-container.source_image
    }
  }

  #metadata_startup_script = "echo Hello, World!"
  
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

  # Setting the startup script to start the Docker image
  metadata_startup_script = <<EOF
#!/bin/bash
sudo docker run \
  -p 8080:8080 \
  --env ENV_VAR_NAME=ENV_VAR_VALUE \
  "us-east1-docker.pkg.dev/whiteflag-0/fennel-docker-registry/fennel-api:latest"
EOF

  service_account {
    scopes = ["cloud-platform"]
  }
}
