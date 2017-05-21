LED-Vote
========================================================================
Navigation: **Server repository** | [Client repository](https://github.com/FancyJesse/led-vote-client)

[![status](https://img.shields.io/badge/Project%20Status-work--in--progress-green.svg)](#)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=jesus_andrade45%40yahoo%2ecom&lc=US&item_name=GitHub%20Projects&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

Users register, login, and vote for an LED color. Once a vote is received, it is saved to a database, and the corresponding LED color blinks on the connected Raspberry-PI GPIO board.

**Current webpage:** [ledvote.fancyjesse.com](http://ledvote.fancyjesse.com)



Introduction
------------------------------------------------------------------------
A Raspberry-Pi project written in Python that utilizes the GPIO board and network.
A server is created and provides connect clients with a list of LED colors.
The colors are predefined via the **config.py** file and will correspond to an LED connected to the GPIO board.
The client has the ability to select an LED color, and once it is selected, the corresponding LED will blink on the GPIO board.

Clients are also able to register a username to track their selections, and the selections of every other participant.
These values are presented via a [webpage](http://ledvote.fancyjesse.com).


Prerequisites
------------------------------------------------------------------------
Raspberry-Pi with GPIO pins

Breadboard with LED lights

Python3


Installation
------------------------------------------------------------------------
Before the installation, be sure to update & upgrade your current packages
```
$ apt-get update && apt-get upgrade
```

Be sure you have RPi.GPIO package installed
```
$ apt-get install rpi.gpio
```

Project also requires bcrypt
```
$ pip install bcrypt
```

To download the LED-Vote project use the following:

git
```
$ git clone https://github.com/FancyJesse/led-vote
```


Setup - GPIO
------------------------------------------------------------------------
TODO


Usage
------------------------------------------------------------------------
Before executing the program, review and adjust the settings in **config.py**. The settings include the network name and port to listen to. As well as the GPIO pins to use with regards to the LEDs.

Once your settings are set, execute **led.py** directly to test out the LEDs.
This should give you an idea of whether your GPIO settings are configured correctly.
```
$ python3 ./ledvote.py
```


License
------------------------------------------------------------------------
See the file "LICENSE" for license information.


Authors
------------------------------------------------------------------------
FancyJesse
