##########################
# CONFIGURATION SETTINGS #
##########################

# This variable determines whether or not outputs are printed out to the console
verboseMode = True # True | False

# This variable (in seconds) equates to the amount of time that needs to elapse
# before a drink Even is captured
postEventTimeCheck = 2 # in Seconds

# This value sets the baudrate for the serial port (Should be 115200 for kegbot)
seriaLBaudRate = 115200

# This array holds all of the values of the devices for serial reading.  If
# multiple are in the list, a failure to initialize ANY of the ports will result
# in a failure to read from any ports.
#
# Example with a single port:
#   serialDevices = ['/dev/ttyACM0']
#
# Example with multiple ports defined
#   serialDevices = ['/dev/ttyACM0', '/dev/ttyACM1']
serialDevices = ['/dev/ttyACM0']

# Starting Keg ID
startingKegId = 0

# Stitch function for post_drink
STITCH_URL = "[INSERT URL HERE]"


############################################################################
# END OF CONFIGURATION... A FEW COMMON FUNCTIONS ARE INCLUDED HERE AS WELL #
############################################################################

# Method for printing messages if verboseMode is enabled
def printMessage(message):
    if verboseMode:
        print(message)

# Setter Function For Verbose Mode
def setVerboseMode(vm):
    global verboseMode
    verboseMode = vm
