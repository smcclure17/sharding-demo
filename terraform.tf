

terraform {
  required_providers {
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "1.15.0"
    }
  }
}

variable "IPV4_ADDRESS" {
  type = string
}

# Obviously, we'd want different passwords for each instance
# but for the sake of this demo, just use one pass for everything.
variable "UNIVERSAL_PASSWORD" {
  type = string
}

# Create a new project
# # haven't tested this b/c I already created the project, but I think this should work.
# resource "google_project" "sharding-demo-project" {
#   name       = "sharding-demo"
#   project_id = "sharding-demo-project"
# }

# Initializing each shard SQL server
resource "google_sql_database_instance" "shard-1" {
  project          = "sharding-demo"
  name             = "demo-shard-1"
  database_version = "POSTGRES_14"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "sean-mac"
        value = var.IPV4_ADDRESS
      }
    }
  }
}
resource "google_sql_database_instance" "shard-2" {
  project          = "sharding-demo"
  name             = "demo-shard-2"
  database_version = "POSTGRES_14"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "sean-mac"
        value = var.IPV4_ADDRESS
      }
    }
  }
}
resource "google_sql_database_instance" "shard-3" {
  project          = "sharding-demo"
  name             = "demo-shard-3"
  database_version = "POSTGRES_14"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "sean-mac"
        value = var.IPV4_ADDRESS
      }
    }
  }
}

# Adding users to each shard
resource "google_sql_user" "shard-1-user" {
  name     = "sean"
  instance = google_sql_database_instance.shard-1.name
  password = var.UNIVERSAL_PASSWORD
  project  = "sharding-demo"
}
resource "google_sql_user" "shard-2-user" {
  name     = "sean"
  instance = google_sql_database_instance.shard-2.name
  password = var.UNIVERSAL_PASSWORD
  project  = "sharding-demo"
}
resource "google_sql_user" "shard-3-user" {
  name     = "sean"
  instance = google_sql_database_instance.shard-3.name
  password = var.UNIVERSAL_PASSWORD
  project  = "sharding-demo"
}

# TODO:
# - Add databases to each shard (covid)
# - Automatically set up billing for each shard
