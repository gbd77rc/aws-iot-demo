# Introduction
This demo shows how the publish/subscribing to the standard topics work and how the shadow could also work.

## Commands
To run the tests on either the Raspberry PI or dev machine do the following

    python3 -m unittest discover testing/ -v

To run the demo do the following either on device or dev

    python3 -m demo.runner -c ./config.json


## Configuration
The configuration of the demo is held in the config.json file.  The root, cert, private elements are the most important as they point to the actual certificates download from the AWS IoT console.  These certs are not stored in github etc.  So the actual setttings here do not matter.


    {
        "aws": {
            "telemetry_topic": "telemetry/rpi-1",
            "control_topic": "control/rpi-1",
            "client_id": "rpi-1",
            "thing_id": "iot-demo-rpi-1",
            "endpoint": "a1bqyju1450wf9-ats.iot.eu-west-1.amazonaws.com",
            "port": 8883,
            "root": "./certs/root-ca.pem",
            "cert": "./certs/8098cdfe96-certificate.pem.crt",
            "private": "./certs/8098cdfe96-private.pem.key"
        },
        "sensor": {
            "temp_pin": 4,
            "polling": 20.0
        },
        "leds": {
            "blink": 500,
            "colours": [{
                "colour": "Green",
                "pin": 26
            }, {
                "colour": "Yellow",
                "pin": 19
            }, {
                "colour": "Red",
                "pin": 13
            }]
        },
        "logging": {
            "level": "debug",
            "location": "./logs/errors.log"
        }
    }


## Shadow State
The following json document is how the state should be.  This can be replicated in the desired or reported elements

    {
        "lights":{
            "green": "off",
            "yellow": "off",
            "red": "off"
        },
        "sensors":{
            "temperature":0,
            "humidity":0,
            "cpu_temp: 0
        }
    }

Now if you set any of the sensors in the AWS console they will be ignore as they cannot be a desired state, only the lights can be.
    