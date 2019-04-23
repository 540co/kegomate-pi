import config
import struct
import ksm
import serialPort
import serial
import requests
import sys

mainLoopFlag = True
serialPorts = []
flowmeterCounter = 0

# The OPTIONAL second command line attribute would be the serial port
if(len(sys.argv) > 1):
    config.printMessage("> Serial port '" + sys.argv[1] + "' passed from command line")
    config.serialDevices[0] = sys.argv[1]
else:
    config.printMessage("> No Serial port passed from command line (Defaulting to '" + config.serialDevices[0] + "')")

# The OPTIONAL third command line attribute would be the starting keg number (requires serial port passed in as well)
if(len(sys.argv) > 2):
    config.printMessage("> Starting Keg Number of '" + sys.argv[2] + "' passed from command line")
    flowmeterCounter = int(sys.argv[2])
else:
    config.printMessage("> No Starting Keg Number passed from command line (Defaulting to '" + str(flowmeterCounter) + "')")

def initializeSerialPorts():
    global mainLoopFlag
    global serialPorts
    global flowmeterCounter

    # Logic to initialize the Serial Ports
    if(hasattr(config, 'seriaLBaudRate') == False or
       hasattr(config, 'serialDevices') == False or
       len(config.serialDevices) == 0):
        config.printMessage("ERROR: Couldn't Initialize Serial Ports")
        mainLoopFlag = False
    else: # Only initialize if the Congifurations appear in order
        for device in config.serialDevices:
            sp = serialPort.SerialPort(device, config.seriaLBaudRate)
            sp.addFlowmeter(flowmeterCounter) # Adding flow0
            flowmeterCounter += 1
            sp.addFlowmeter(flowmeterCounter) # Adding flow1
            flowmeterCounter += 1
            serialPorts.append(sp)

initializeSerialPorts()

while mainLoopFlag:
    try:
################################################################################
# For more information on how the kegboard message is structured, visit:
# https://github.com/Kegbot/kegboard/blob/master/docs/source/serial-protocol.rst
################################################################################
        header_message = "KBSP v1:"

        # Identify the beginning of a relevant serial message beginning with
        prefix = serialPorts[0].ser.read_until(header_message)[-8:]

        # Parse out the message_id for processing
        raw_read = serialPorts[0].ser.read(2) #raw serial read
        message_id = raw_read[1] + raw_read[0] #little endian conv

        # Parse out the payload length from message header for processing
        raw_read = serialPorts[0].ser.read(2) #raw serial read
        payload_len = raw_read[1] + raw_read[0] #little endian conv

        kegomate = ksm.KegomateSerialMessage(serialPorts[0].ser, message_id, payload_len)

        # Check to see if the event
        for fm in serialPorts[0].flowmeters:
            if(fm.isEventComplete()):
                config.printMessage("> An event has ended and will now be logged for " + fm.kegId)
                eventAmount = kegomate.kegomateAmountConversation(fm.firstTickOfEvent, fm.lastTick)
                config.printMessage('> %.2f fl oz was consumed' % eventAmount)
                data = {}
                data["tapId"] = fm.kegId
                data["volume"] = eventAmount

                # Only register consumption is it's greater than 1 tick
                if(eventAmount >= 0.05):
                    r = requests.post(url = config.STITCH_URL, json = data)

                fm.resetEvent()


        # If it's a meter reading event... update ticker and reset timer
        if(kegomate.getHexMessageId() == "0010"):
            fm = serialPorts[0].getFlowMeter(kegomate.getFlowMeterName())
            fm.processTick(kegomate.getFlowMeterReading())
            fm.resetTimer()
        #else: # Else, check the timers on the flowmeters for completed events
            #for fm in serialPorts[0].flowmeters:
                #for w

        kegomate.clearValues()
    except:
        print("Keyboard Interrupt")
        break
