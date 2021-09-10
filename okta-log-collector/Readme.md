# Collecting Okta Event Logs for Log Aggregation Tools

This script was first created by @RobsRepo, compatible with 2.7. Now it has been transfomred into python 3 or greater.
This Python script will pull Okta logs into a format that is easily parsable by log aggregation tools such as Elasticsearch, SumoLogic and Splunk. Run it using a cron job or some kind of scheduler. With Sumo Logic you can run this as a script source.

## Key Points About this Script
  - This script will produce a file called "output-<current date>.log".
  - It will bring back at most 1000 entries on each outbound call. 
  - It will continue to call until there aren't anymore event logs to pull.
  - There is a system lock on this script when it is initially started to prevent another process from running this script more than once.
  - It will record the last published date of the log that it collected (stored in startTime.properties) and upon the next time this script is invoked it will retrieve event logs from this published time.

# Prerequisites
-	You will need Python 3 or greater
-	You will need the "zc.lockfile" library. Install it using “pip install zc.lockfile”

# Setup
1. Install the prerequisites.
2. Add the necessary Okta configuration information inside `config.properties`.
3. You can omit the contents for `startime.properties`. However, if you would like to have this script start collecting events before the current time, you will need to add the following line by line:
 * YEAR
 * MONTH
 * Day
 * Hour
 * Minute
 * Second
 
# Run the Script OR Configuration for background:
1. To run directly in background using python command:
  `python3 okta-log-collector.py &`
  
2. To create linux service [Ubuntu]
  - Download all files from [okta-log-collector](https://github.com/0ccupi3R/automation-scripts/new/main/okta-log-collector) repo and copy it in `/opt` directory.
  - Now create service file :
```yaml
  [Unit]
  Description=Okta Log Collector Script

  [Service]
  Restart=always
  User=root
  WorkingDirectory=/opt/okta-log-collector
  ExecStart=/usr/bin/python3 /opt/okta-log-collector/okta-log-collector.py

  [Install]
  WantedBy=multi-user.target
```

# Ingesting Okta logs to Elasticsearch:
  ## Method-1: Using Filebeat Module [recommended]
  - Edit the file `/etc/filebeat/modules.d/okta.yml`
  ```yaml
  # Module: okta
  # Docs: https://www.elastic.co/guide/en/beats/filebeat/7.13/filebeat-module-okta.html

  - module: okta
    system:
      enabled: true
      # You must configure the URL with your Okta domain and provide an
      # API token to access the logs API.
      var.url: https://<organization_name>.okta.com/api/v1/logs
      var.api_key: '<token>'
  ```
  
  ## Method-2: Using Logstash to send logs to Elasticsearch or AWS S3 bucket [Please generate Acess Keys for authenticaion]
  - Create a new configuration file `/etc/logstash/conf.d/okta.yml`
  ```yaml
    input {
      file {
        path => "/opt/okta-log-collector/output-*.log"
        start_position => "beginning"
      }
    }
    output {
      s3 {
        #access_key_id => "ACCESS_KEY"
        #secret_access_key => "SECRET_KEY"
        region => "eu-west-1"
        bucket => "your_bucket"
        size_file => 2048     (in Bytes)
        time_file => 5        (in Minutes)
        codec => "plain"
      }
  
      elasticsearch {
        hosts => ["localhost:9200"]
        index => "okta-logs-%{+YYYY.MM.dd}"
        #user => "elastic"
        #password => "changeme"
      }
    }
  ```
  
# Special Thanks
  @RobsRepo - [https://github.com/RobsRepo]
