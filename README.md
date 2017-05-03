# GIANT
## Problem
Intrusion Analysts are wasting their time going between browsers, urls, and terminals to run different types of applications.

## Solution
GIANT (Goliath, Intrusion Analyst Network Toolkit) seeks to remove those issues. The analyst will have access to a Web GUI along with a command line application for the analysts that want to be a little closer to their data.

## Installation
### Supported Distributions
This project is designed and developed with CentOS or RedHat in mind. They are the only supported distributions, but there have been some successes with running this on windows. It could presumably run on anything that can handle docker.

### Packages and first run
First this project requires installation of a few packages   
 
```
yum install epel-release # Turns on linux's extra packages (epel) repo  
yum install docker pip git # Requires docker for docker and pip for the later installation of docker-compose  
pip install docker-compose  
cd /opt # Optional (depends on where you want to put it)  
git clone https://github.com/giantproject/giant.git  
cd giant/containers  
docker-compose up --build   
```  
Now you should go take a break, this is going to take awhile if it's the first build. 
Once it's done building you should be able to navigate to it via your browser simply by typing <ipOfYourBuildMachine>:5000  and you should be greeted with the landing page. 


## Tools
### IPINFO
This is simply a wrapper around the ipinfo.io web app. It provides IP Geolocation about the given IP. 

### Whois
This uses the python-whois package and simply runs the whois lookups on the provided domains. It returns the information in a JSON dump.

### Whatis
This doesn't utilize any outside API calls. This tool is meant for the young (or experienced) analyst who may not know what is significant, if anything, about a specific port and protocol. The analyst can query a port and gets back a data dump from a database containing some basic RFC information on the providedports

### Event
This is for creating an event, assuming that the analyst is in an environment that they had to log some form of event information. At this point it only handles simple fields: event, description, and analyst's comments. 

### Web Client
This is the aggregation point for all of the tools. This simply links to all of the other tool containers and gives the user the ability to access the fields without having to know the various ports everything is pointing to. 