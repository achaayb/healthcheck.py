# healthcheck.py

healthcheck.py is a simple command-line tool for monitoring the health of web servers. It allows users to add, remove, and list servers to be monitored, and performs regular health checks on them to ensure they are responding with a 200 status code.

All server data is stored in an SQLite database called healthcheck.db, which includes two tables: servers and checks. The servers table contains information about each server, including its name and URL. The checks table contains a log of all health checks performed on each server, including the timestamp and whether the server was healthy or not.

The tool is easily customizable, allowing users to set the interval at which the health checks are performed and the timeout for waiting for a response

## Usage

To run the tool, simply execute the healthcheck.py script with the desired command-line options:

```
python healthcheck.py --add name url     Add a new server to monitor
python healthcheck.py --remove name      Remove a server from monitoring
python healthcheck.py --list             List all servers being monitored
python healthcheck.py                    Run health checks on all servers at specified interval
```

### Optional Arguments

    --interval: the interval (in seconds) at which the health checks are performed. Default is 60 seconds.
    --timeout: the timeout (in seconds) for waiting for a response from the server. Default is 5 seconds.
    
### Requirements

This tool requires no external dependencies beyond Python 3.x.
