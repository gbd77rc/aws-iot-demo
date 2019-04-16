# Introduction
This document is the design of phase 2 flow.

1. Load configuration
1. workout provider and click off connection
1. Workout Use Case to run
1. Load devices for use case
1. If shadow then start the handshake between AWS Cloud Shadow and Device Shadow
1. Trigger polling or shadow run

## Common Functionality
This module will have various features that can be used by all other modules.

*   Publisher
*   Singleton

### Publisher
The publish class will support the following features

*   registry of event, who and optional callback handle
*   unregistry of event and who
*   dispatch the event message to all registered subscribers to that event
*   get the count of subscribers, all if the event is not specified

### Singleton
The singleton class will enforce that same internal instance to be used by all instances created.  

## Configuration Module
This module will load the configuration JSON file.  It will create multiple configuration objects, one per area.  The areas are 

* Use Case with Device configuration
* Provider

For the Use Case, an event will be raised whenever it changes via topic message or shadow.

Switching between standard topics and shadow will only be supported with manual change on the device.  Also it will depend if the provide supports this type of feature.  Currently only AWS does.

Each configuration module will have a base/interface class that will support specific features

* Read the configuration file
* Get the specific module configuration

## Provider Module
This module will select the specified cloud provider and check that it can connect with the configuration information contained the JSON.

Each provider will have a base/interface class that will suppport specific features

* Connect to the provider
* Disconnect from the provider
* Loopback test - Send message on command topic and subscribe to it to check that it is the same message sent
* Start - Start the polling loop
* Stop - Stop the polling loop
* Report - List the amount of messages sent/recieved, total size of messages send/recieved so far

## Use Cases
This module will select specific use cases, 

Each use-case will have a group of devices, polling and payload type. 

Each use-case will have a base/interface class that will support specific features

* Initialise Devices
* Start Use-Case
* Stop Use-Case

