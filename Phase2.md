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
    "telemetry_topic": "<Topic name to use to to send telemetry>",
    "control_topic": "<Topic name to use for control signals>"
    "payload_type": "<The type of payload to use, PROTOBUF or JSON">

### AWS Provider
This is the configuration to be used in the AWS provider section

    "providers":[{
        "type": "aws",
        "thing_id": "<thing id on AWS>",
        "endpoint": "<url endpoint to AWS account>",
        "port": "<MQTT port to use 8883 or 443>",
        "root": "<AWS Root Public Certificate>",
        "cert": "<AWS Thing Public Certificate>",
        "private": "<AWS Thing Private Key>",
        "mode": "<Mode of communication, STAND or SHADW>
    }]

## Use Cases
This is the configuration of the use cases that can be done

    "use-case": "<the use case to use>",
    "use-cases" :[{
        "use-case": "<name of the use case>",
        "push": <how many seconds should it push the data>,
        "payload_type": "<JSON or PROTOBUF type of payload>",
        "devices":[<list of device names to used for this use-case>]
    }]

## Devies
This will enable or disable device that will be read/write.  It will list out the sensor setup details as well.

    "devices":[{
        "type": "<Type of device to use>",
        "name": "<Friendly name of the sensor>",
        "direction":"<which direction should the pin be in: OUT or IN>"
        "pin": <The pin where to read or write value>
    },{
        "type": "<Type of psudo file path to use>",
        "name": "<Friendly name of the sensor>",
        "location": "<psudo file path>"
    },{
        "type": "<Type of utility to use>",
        "name": "<Friendly name of the sensor>"
    }]

### LED
This device is switch on/off the LED.  Here is an example of the LED device

    {
        "type": "led",
        "name": "Green",
        "pind": 23,
        "direction": "OUT"
    }


### DHT11
This device will read the temperature/humidity using the one-wire protocol.

    {
        "type": "dht11",
        "name": "DHT-11",
        "pind": 16,
        "direction": "OUT"
    }

### CPU Temp
This device will read the CPU Temperature using sysfs

    {
        "type": "cputemp",
        "name": "CPU Temperature",
        "sysfs": "/sys/class/thermal/thermal_zone0/temp"
    }

### CPU Percentage
This device will read the CPU precentage using PSUtils

    {
        "type": "cpuprec",
        "name": "CPU Precentage"
    }    
    
### Memory Available
This device will read the memory available using PSUtils

    {
        "type": "memavail",
        "name": "Memory Available"
    } 

## Logging
The following configuration will highlight the logging configuraton

    "logging":{
        "level": "<the level of loggign to echo to console, NONE, DEBUG, INFO, WARNING, ERROR or CRITICAL>"
        "error-file": "<the location where the error and critical message will be stored in file>"
    }

# Message Structure
There are two topics for standard MQTT, one for device to cloud (telemetry) and the other cloud to device (control).   Each message will have a the following properties at least, does not matter what direction.

*   timestamp - This is the current EPOC of the device or cloud
*   message_type - The type of message being transmitted
*   device_id - The device, client or thing name

The message_type supported are

*   CNTL - Control Switch on/off
*   TELE - Telemetry Sending
*   CNFG - Configuration change
*   TIMS - Time Sync Msg via NTP

