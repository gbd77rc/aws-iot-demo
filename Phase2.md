# Introduction
This phase is to refactor the messaging within the system.  It will allow either the shadow or standard topics.  With standard topic we will use protobuf.  Each features to implemented are:

*   Remove logging from AWS Side as it is swamping display
*   Add in bandwidth calculation
*   Define what is send and recieved and what topics
*   Add in possible ACK/NAK handling on standard topics
*   Refactor providers to have an interface so that switching out providers can be done via the configuration setup
*   Configuration to allow shadow mode only if aws provider selected

# Sensors
The sensors to be used are 
*   Current DHT11 for external temperature and humidity
*   Current CPU temperature 
*   Current CPU Precentage
*   Current Memory Available

# Configuration
The following configuration options will be available.

## Cloud Provider
The configuration will have a section per provider and option to say which provider to use.  The root configuration will also include the following options for cloud providers

    "cloud": "<provider key>"
    "push_interval": "<Time interval in seconds for telemetry push, 0 is disabled>"
    "telemetry_topic": "<Topic name to use to to send telemetry>"
    "control_topic": "<Topic name to use for control signals>"

### AWS Provider
This is the configuration to be used in the AWS provider section

    "aws":{
        "thing_id": "<thing id on AWS>",
        "endpoint": "<url endpoint to AWS account>",
        "port": "<MQTT port to use 8883 or 443>",
        "root": "<AWS Root Public Certificate>",
        "cert": "<AWS Thing Public Certificate>",
        "private": "<AWS Thing Private Key>"
    }

## Devies
This will enable or disable device that will be read/write.  It will list out the sensor setup details as well.

    "devices":[{
        "type": "<Type of device to monitor>",
        "name": "<Friendly name of the sensor>",
        "enabled": <true or false to enable the device>,
        "locations": [{
            "type": "<the type of location pin or sysfs>"
            "sysfs": "<the pseudo file system from where to read the information>",
            "pin":{
                "number": <the pin number to use>,
                "direction": "<which direction IN or OUT>",
                "name": "<The name of the pin>
            }
        }]
    }]

### LED
This device is switch on/off the LED.  Here is an example of the LED device

    {
        "type": "led",
        "name": "Green",
        "enabled": true,
        "locatons": [{
            "type": "pin",
            "pin":{
                "number": 23,
                "direction": "OUT",
                "name": "LED-1"
            }
        }]
    }


### DHT11
This device will read the temperature/humidity using the one-wire protocol.

    {
        "type": "dht11",
        "name": "DHT-11",
        "enabled": true,
        "locatons": [{
            "type": "pin",
            "pin":{
                "number": 16,
                "direction": "IN",
                "name": "DHT11-1"
            }
        }]
    }

### CPU Temp
This device will read the CPU Temperature using sysfs

    {
        "type": "cputemp",
        "name": "CPU Temperature",
        "enabled": true,
        "locatons": [{
            "type": "sysfs",
            "sysfs": "/sys/class/thermal/thermal_zone0/temp"
        }]
    }

### CPU Percentage
This device will read the CPU precentage using PSUtils

    {
        "type": "cpuprec",
        "name": "CPU Precentage",
        "enabled": true,
    }    
    
### Memory Available
This device will read the memory available using PSUtils

    {
        "type": "memavail",
        "name": "Memory Available",
        "enabled": true,
    } 

## Logging
The following configuration will highlight the logging configuraton

    "logging":{
        "level": "<the level of loggign to echo to console, NONE, DEBUG, INFO, WARNING, ERROR or CRITICAL>"
        "error-file": "<the location where the error and critical message will be stored in file>"
    }