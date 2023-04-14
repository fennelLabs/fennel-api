resource "google_compute_instance" "fennel-api" {
  name         = "fennel-api-instance"
  machine_type = "t2a-standard-1"
  zone         = "us-east1"
  
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  #metadata_startup_script = "echo Hello, World!"
  
  network_interface {
    network = "default"
    access_config {}
  }

  # Provisioning a GCP artifact registry instance
  metadata = {
    # Required to authenticate with Artifact Registry
    "google-artifactregistry-repo" = "fennel-docker-registry"
    # The Docker image to run
    "google-artifactregistry-image" = "fennel-api:latest"
  }

  # Setting the startup script to start the Docker image
  metadata_startup_script = <<EOF
#!/bin/bash
sudo docker run \
  -p 8080:8080 \
  --env ENV_VAR_NAME=ENV_VAR_VALUE \
  "us-east1-docker.pkg.dev/\${google_compute_project()}/fennel-docker-registry/fennel-api:latest"
EOF

  service_account {
    scopes = ["cloud-platform"]
  }
}
