"""
This file contains all of the configuration values for ledvote
Update this file with values for your specific settings/configuration
Please read the short descriptions before altering a value
"""

# Option to display what is logged without
# having to constantly check log files
# 0 - Logs are written quietly
# 1 - Logs are displayed onto console as well
LOG_DISPLAY = 1

# Directory used to store log files
# Leave value None for Home directory ('~')
DIR_LOG = None

# Directory used to store sqlite-database file
# Leave value None for Home directory ('~')
DIR_DATABASE = None

# The server's IP address
# Find it by using the terminal command 'ifconfig'
# Default value 'AUTO-FIND' will attempt to locate
# the IP address automatically
SERVER_ADDRESS = 'AUTO-FIND'

# The port the server should listen to
# Be sure to correctly port-forward if you wish to
# connect via the Internet
SERVER_PORT = 1321

# The LED blink delay
# The delay occurs when the LED turns on and after the LED
# LED turns off, so constant triggers won't leave the LED
# on constantly
# Value measured in seconds
LED_BLINK_DELAY = 0.2

# The LED Pin and ID list used to setup the GPIO board
# The format for value is a tuple of - ( GPIO_PIN , LED_ID )
#
# GPIO_PIN - the GPIO Pin number used for the LED
#            Consult the GPIO and breadboard when attempting
#            to identify the correct GPIO pin numbers
#
# LED_ID - an ID of your choosing to help identify the LED
#          Values must be unique from one another
# Values must be correctly formatted or will result in errors
LED_INFO = [
		(6, 'ledRed'),
		(4, 'ledYellow'),
]

