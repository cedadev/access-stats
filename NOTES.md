# Notes on download stats requirements
Update in progress



# CEDA Download statistics requirements 

## Definition and scope

An archive download metrics system is required for monitoring and reporting. This is often referred to as “download stats”. 
The system has a defined list of download methods, for example, the main FTP download server or the DAP service. These 
services have records of accesses in log files or similar. The download records need bringing together so that an 
aggregate view can be reported on. 

# Underlying common requirements
In all use cases there are common underlying requirements about records that are reflected in reports:
 - It's possible to flag or filter bots and other invalid records.
 - There is a maintained list of services that the records apply to. 
 - The records are as complete as possible for all defined services.
 - There is nothing that compromises our GDPR compliance.
 - The records are as up to date as possible. Records should be available within a week, at the latest. 
 - Definitions and workflows are clear and simple enough, so that the interpretation of a report is understandable.
 - Monitoring is in place so that problems are resolved in a timely manner.
 - Raw log files are kept as backup if reprocessing is needed.

## Download stats use cases

### User Looking for Popular Data
An archive user wants to see the popularity of a dataset to gauge if it is what other researchers are using. 
Requires some basic metrics visible from the catalogue page. The numbers of interest here are size, accesses, 
and estimated number of users. Possibility, some normalised metrics related to the dataset size/number of 
files would be of interest. They may want to dig a little deeper to see which bits of the dataset are popular, 
trends and show this is a simple visualisation that all our users can comprehend. Public stats webpage should 
explain definitions / limitations for typical archive users. 

### Data Provider Reporting
A data provider wants to see how their datasets are being used in order to report to funders and user groups. 
The reports can take the form of numbers, tables, graphs or charts. The visual representation of the metrics is 
dependent on the report so access to the raw numbers is needed. In addition links to a public stats page may 
be included in the reports. Some data providers may screenshot graphs and include these in reporting. 
The metrics needed vary from funder, data provider. There are lots of metrics that data providers would like, 
but are not possible/easy to collect. These extra metrics should be possible as post-processing workflows, 
but nice presentation and scheduled post-processing runs are out of scope of the vanilla download stats system.    

### Data Provider Usage Tracking
A data provider wants to assess which datasets are most or least popular to help prioritise work. More 
popular datasets may warrant more effort to optimise bang for buck. Less popular datasets may be discontinued.  
Or perhaps less popular datasets require more effort to improve their  usefulness. The ability to dig into the 
data download metrics is needed. Key metrics are number of users and accesses over time. The ability to 
differentiate which bits of the data are used is relevant here. 

### Data Centre Reporting
A data centre wants to see how their datasets are being used in order to report to funders, user groups 
and other stakeholders. Very similar to data provider reporting but for all the data centre holdings. 
Constructing a narrative around popular data allows the data centre to demonstrate the purpose of 
the data centre. 

### Data Centre Usage Tracking
A data centre wants to track use to prioritise work. Similar to data providers, but they also include 
distribution methods and user agent analysis to know how users are working as much as which data they 
are using. Downloads can influence retention times and inform cost benefit analysis. Knowing the top 
ten datasets can influence work on reducing queries but updating documentation. 


## Other relivent repos

 - https://gitlab.ceda.ac.uk/cedadev/cci_stats WMS stats repo.
 - https://gitlab.ceda.ac.uk/cedadev/cci_download_stats stats processor for CCI stats. Has some extra filtering.
 - https://gitlab.ceda.ac.uk/cedadev/download_stats_app Inital repo for download stats app - ignore.


## Spesific Access stats requests

### MO for Hadley centre reporting
Met Office Hadly Centre Pipeline contract 2024-2027 required quarterly reporting from 2nd week of January onwards. These will be within returns the Met Office have to make to government. We will be required to provide download/access stats for:
 - HadObs datassets via the CEDA Archive
 - CMIP data via the CEDA Archive
Other statistics will be sought from the ESGF interfaces.

### CCI reporting
(Alison to add sometime here)

### EDS Annual reporting
In May every year some stats go in the EDS annual reporting. This is generally total downloads number, volume, Estimates of number of 
users. Likely to have summary by data centre in future years. These are sometimes combinned with metrics from other 
data centre services. Caviates are we don't know the JASMIN direct access numbers and these are likely to be subtantially more 
in terms of volume.

