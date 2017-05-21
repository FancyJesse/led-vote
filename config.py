"""
This file contains all of the configuration values for ledvote
Update this file with values for your specific settings/configuration
Please read the short descriptions before altering a value
"""

# The server's host IP address
# Find it by using the terminal command 'ifconfig'
# Default value '?' will attempt to locate
# the IP address automatically
host = '?'

# The port the server should listen to
# Be sure to correctly port-forward if you wish to
# connect via the Internet
port = 1330

# The LED blink delay
# The delay occurs when the LED turns on and after the LED
# LED turns off, so constant triggers won't leave the LED
# on constantly
# Value measured in seconds
blink_delay = 0.2

# The LED Pin and ID list used to setup the GPIO board
# The format for value is a tuple of - ( GPIO_PIN , LED_ID )
#
# GPIO_PIN - the GPIO Pin number used for the LED
#            Consult the GPIO and breadboard when attempting
#            to identify the correct GPIO pin numbers
#
# LED_ID - an ID of your choosing to help identify the LED
#          Values must be unique from one another and
#          must begin with ' led_ ' as this prefix is
#          checked throughout the script
# Values must be correctly formatted or will result in errors
led_info = [
		(21, 'white'),
		(5, 'red'),
		(25, 'orange'),
		(22, 'yellow'),
		(23, 'green'),
		(17, 'blue'),
		(18, 'cyan'),
		(4, 'purple'),
]
