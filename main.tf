module "gce-container" {
  source = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"  # Upgrade the version if necessary.

  container = {
    #image = "https://us-east1-docker.pkg.dev/whiteflag-0/fennel-docker-registry/fennel-api:latest"
    image = "ubuntu-os-cloud/ubuntu-2004-lts"
  }
}

resource "google_compute_instance" "fennel-api" {
  name         = "fennel-api-instance"
  machine_type = "e2-small"
  zone         = "us-east1-b"
  
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  #metadata_startup_script = "echo Hello, World!"
  metadata_startup_script = <<EOF
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io
    gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin us-east1-docker.pkg.dev
    docker pull us-east1-docker.pkg.dev/whiteflag-0/fennel-docker-registry/fennel-api:latest
    docker run -dit -p 8080:8080 --name fennel-api us-east1-docker.pkg.dev/whiteflag-0/fennel-docker-registry/fennel-api:latest
  EOF  
  
  #"#!/bin/bash\ndocker run us-east1-docker.pkg.dev/whiteflag-0/fennel-docker-registry/fennel-api:latest"
  
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
