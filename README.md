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
