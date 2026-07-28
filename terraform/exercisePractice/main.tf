provider "google" {
  project     = "devopslearning-495605"
  region      = "asia-south1"
  zone         = "asia-south1-a"
  credentials = file("service.json")
}


resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
  auto_create_subnetworks = false
  routing_mode = "REGIONAL"
}

resource "google_compute_subnetwork" "subnet" {
  name = "terraform-subnet"
  network = google_compute_network.vpc_network.id   #self_link
  ip_cidr_range = "10.0.0.0/24"
  region = "asia-south1"
}

resource "google_compute_firewall" "firewall" {
  name = "terraform-firewall"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports = ["22", "80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_instance" "vm_instance" {
  name = "terraform-vm"
  machine_type = "e2-micro"
  zone = "asia-south1-a"
  network_interface {
    network = google_compute_network.vpc_network.id
    subnetwork = google_compute_subnetwork.subnet.id

    access_config {
      // Ephemeral IP
    }
  }
  boot_disk {
    initialize_params {
      image = "ubuntu-2204-lts"
    }
  }

  metadata = {
    ssh-keys = "vicky@vicky-HP-EliteBook-850-G1:${file("~/.ssh/googlecloud.pub")}"
  }
}   