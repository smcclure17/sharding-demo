

terraform {
  required_providers {
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "1.15.0"
    }
  }
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
        value = "76.19.98.199"
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
        value = "76.19.98.199"
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
        value = "76.19.98.199"
      }
    }
  }
}

# Adding users to each shard
resource "google_sql_user" "shard-1-user" {
  name     = "sean"
  instance = google_sql_database_instance.shard-1.name
  password = "changeme"
  project  = "sharding-demo"
}
resource "google_sql_user" "shard-2-user" {
  name     = "sean"
  instance = google_sql_database_instance.shard-2.name
  password = "changeme"
  project  = "sharding-demo"
}
resource "google_sql_user" "shard-3-user" {
  name     = "sean"
  instance = google_sql_database_instance.shard-3.name
  password = "changeme"
  project  = "sharding-demo"
}

# TODO:
# - Add databases to each shard (covid)
# - Automatically set up billing for each shard
