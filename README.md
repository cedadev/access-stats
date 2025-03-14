# access-stats

`access-stats` is a Django application that provides useful visualisations of access data from an Elasticsearch endpoint.  
The access data is an index of data downloads from the CEDA archive, and data deposits to the CEDA archive, via various methods.  

## Configuration

### [`access_stats/settings.py`](access_stats/settings.py)

Main Django settings file with some custom settings.  
Use `PUBLIC_SITE` setting to limit the site and api to non-sensitive user data.  
In the playbook this is fully overwritten using a template.  

### `access_stats/settings_local.py`

Sensitive settings placed here while debugging/not using the playbook.  
Template can be found at [access_stats/settings_local.py.tmpl](access_stats/settings_local.py.tmpl).  

### `access_stats/settings.yml`

Contains credentials and configuration for Elasticsearch connection.  
Template can be found at [access_stats/settings.yml.tmpl](access_stats/settings.yml.tmpl).  


## Set up

### Poetry Setup

1. Install Poetry (if not already installed)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies
   ```bash
   # Create virtual environment and install dependencies
   poetry install
   ```

3. Create local settings from template
   ```bash
   cp access_stats/settings_local.py.tmpl access_stats/settings_local.py
   cp access_stats/settings.yml.tmpl access_stats/settings.yml
   # Edit these files with your configuration
   ```

### Django Setup

1. Apply migrations
   ```bash
   poetry run python manage.py migrate
   ```

2. Start development server
   ```bash
   poetry run python manage.py runserver
   ```

### Managing Dependencies

First add the dependency to poetry as normal `poetry add <dependency_name>`

Then run `poetry export -f requirements.txt --output requirements.txt --without-hashes`