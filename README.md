LED-Vote
========================================================================
Navigation: [Client Repository](https://github.com/FancyJesse/led-vote-client)

Introduction
------------------------------------------------------------------------
A Raspberry-Pi project written in Python that utilizes the GPIO board and network.
A server is created and runs on a network. Users are then able to register an account and will
have the option to vote for a color. The colors are predefined via the **config.py** file and 
will correspond to an LED connected to the GPIO board. When a vote for a color is received, 
the corresponding LED will blink. Votes are stored in a database and displayed on a webpage (TODO).

Prerequisites
------------------------------------------------------------------------
Raspberry-Pi with GPIO pins

Breadboard with LED lights

Python3


Installation
------------------------------------------------------------------------
Before the installation, be sure to update & upgrade your current packages
```
$ sudo apt-get update && sudo apt-get upgrade
```

Be sure you have RPi.GPIO package installed
```
$ sudo apt-get install rpi.gpio
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
```
$ cd
$ nano config.py
```

To execute the program, simply call **ledvote.py**
```
$ cd
$ ./ledvote.py
```

*Note: You might have to explicitly call python3 to run it*
```
$ python3 ./ledvote.py
```

Ideally you will want the program to run in the background, enter the following command for this:
```
$ screen -d -m -S [screen-name] [application-to-run] 
```

View a list of screens currently running:
```
$ screen -ls
```

To reattach the screen use:
```
$ screen -r [screen-name]
```

The program is continuous, so it will have to be forcefully stopped. (Will change with later versions)


Release History
------------------------------------------------------------------------
* 0.4.5
	* Added additional server request handlers
	* Now returns correctly-cased username after successful login
	* Reordered server request handlers
* 0.4.0
	* Adjusted initial setup logic so modules can be loaded individually
	* Configured database creation logic so new led_id columns are automatically added
	* Adjusted logic for gathering and sending LED user votes 
	* Renamed database columns
	* Renamed variables
* 0.3.1
	* Text fixes
* 0.3.0
	* Initial release


License
------------------------------------------------------------------------
See the file "LICENSE" for license information.


Authors
------------------------------------------------------------------------
FancyJesse
