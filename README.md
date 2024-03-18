

# ETL with Docker, Python, and MySQL

This project demonstrates setting up an ETL (Extract, Transform, Load) pipeline using Docker, Python, and MySQL. It includes two Python scripts for fetching US exchange rates and recording MySQL table changes over time. The pipeline is scheduled to run periodically using cron.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Scheduled Jobs](#scheduled-jobs)
- [Getting Started](#getting-started)
  - [Clone the Repository](#clone-the-repository)
  - [Create network](#create-network)
  - [Create volume](#create-volume)
  - [Build Docker Images](#build-docker-images)
  - [Run the Containers](#run-the-containers)

## Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

## Project Structure

- **Dockerfile:** Contains instructions for building the Docker image.
- **docker-compose.yml:** Configuration file for defining services, networks, and volumes.
- **requirements.txt:** Python dependencies for the project.
- **get_rate.py:** Python script to fetch US exchange rates and insert/update data in MySQL.
- **mysql_info.py:** Python script to record MySQL table changes over time.
- **config.toml:** Configuration file containing MySQL connection details.
- **README.md:** Project documentation.

## Configuration

Update the `config.toml` file with your MySQL connection details.
Corresponds to the mysql service in docker-compose.yml

```toml
[MySQL]
host = "database_mysql"
port = "3306"
driver = "mysql"
username = "root"
password = "your-password"
db_name = "crontabDB"
```


## Scheduled Jobs

- **get_rate.py:** Fetches US exchange rates every hour.
- **mysql_info.py:** Records MySQL table changes every 5 minutes.

## Getting Started

### Clone the Repository

```
git clone https://github.com/YoZhenYeh/ETL_crontab
```
### Create network
Corresponds to the network in docker-compose.yml
```
docker network create my_network
```

### Create volume
Corresponds to the volume in docker-compose.yml
```
docker volume create todo-mysql-data
```

### Build Docker Images

```
docker image build -t ubuntu_cron:2.0 .
```

### Run the Containers

```
docker compose -f docker-compose.yml up -d
```
