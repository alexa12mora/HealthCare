# General readme file

# 🛠️ Requisites
- Conda
- Postgresql

# 📥 How to install:
Clone the project

```bash
git clone git@github.com:alexa12mora/HealthCare.git
```

## Environment

Navigate to the `HealthCare` folder  

Create a virtual environment using conda Windows/Linux:   
`conda env create -f environment.yml`

Then activate the environment using:  
`conda activate hc_env`   

Then run this command
`conda env update -f environment.yml`  
This command can be executed in case there are changes in the environment.yml and thus update the environment without having to create it again


## Database configuration

### Install Postgresql database

Run this in the terminal.
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

### Enter postgres sql

```bash
sudo -u postgres psql
```
### Create user

```sql
CREATE USER admin_hcare PASSWORD 'admin123';
```

### Assign superuser permissions to a user

```sql
ALTER ROLE admin_hcare WITH SUPERUSER;
```

### Create database

```sql
CREATE DATABASE healthcare;
```

## Look at the frontend and backend configurations in these other readme files.

### [Backend](https://github.com/alexa12mora/HealthCare/blob/main/backend/readme.md)

### [Frontend](https://github.com/alexa12mora/HealthCare/blob/main/frontend/readme.md)