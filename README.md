LED-Vote
========================================================================
[![status](https://img.shields.io/badge/Project%20Status-work--in--progress-green.svg)](#)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=jesus_andrade45%40yahoo%2ecom&lc=US&item_name=GitHub%20Projects&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

Users register, login, and vote for an LED color. Once a vote is received, it is saved to a database, and the corresponding LED color blinks on the connected Raspberry-PI GPIO board.

**Current webpage:** [ledvote.fancyjesse.com](http://ledvote.fancyjesse.com)



Introduction
------------------------------------------------------------------------
A Raspberry-Pi project written in Python that utilizes the GPIO board and network capabilities.
The GPIO board is configured with multiple LEDs that correspond with the **config.py** file.
The LED ID and GPIO-pin number are identified as well within this file.
This configuration allows LEDs to be manipulated and handled through the **led.py** script.

A server script is also provided, which handles clients requesting to handle the LEDs.
Once a client is connected, the server listens for a JSON message which identifies a valid ID for the LED (defined in **config.py**), then calls the corresponding LED to blink.

In addition to the server, clients are also able to send LED blink requests through a dynamic webpage.
This webpage provides clients buttons that correspond to the available LEDs. Once a button is click, a connection is established to the server and the JSON message for the LED to blink is sent. 

LED selections are also recorded and stored on a database. Clients are able to register and login to track their LED selections.
The webpage mentioned earlier displays statistics about the LED selections, such as the LED colors most selected and top contributors.

See a working example of this project on this [webpage](http://ledvote.fancyjesse.com).


Prerequisites
------------------------------------------------------------------------
Raspberry-Pi with GPIO pins

Breadboard with LEDs

Python3

MySQL


Installation
------------------------------------------------------------------------
Before the installation, be sure to update & upgrade your current packages
```
$ apt-get update && apt-get upgrade
```

Install the RPi.GPIO package
```
$ apt-get install rpi.gpio
```

Install MySQL and driver (required for vote tracking)
```
$ apt-get install mysql-server --fix-missing 
$ apt-get install php5-mysqlnd
```

Clone the LED-Vote project
```
$ git clone https://github.com/FancyJesse/led-vote
```


Setup - GPIO
------------------------------------------------------------------------
TODO


Setup - Database
------------------------------------------------------------------------
In order to track votes, an SQL tables are required.
These tables can be automatically created my running **InitTables.php**.
```
$ php php/scripts/InitTables.php 
```


Usage
------------------------------------------------------------------------
Before executing the program, review and adjust the settings in **config.py**. The settings include the network name and port to listen to. As well as the GPIO pins to use with regards to the LEDs.

*Note: If the server port number is changed, be sure to also update it in vote.php*

Once your settings are set, execute **led.py** directly to test out the LEDs.
This should give you an idea of whether your GPIO settings are configured correctly.
```
$ python3 ./led.py
```

Begin the server to start listening for LED requests from clients.
Once a request is accepted, the corresponding LED will blink.
```
$ python3 ./server.py
```

A sample webpage and scripts is provided in the [php folder](php).


License
------------------------------------------------------------------------
See the file "LICENSE" for license information.


Authors
------------------------------------------------------------------------
FancyJesse
