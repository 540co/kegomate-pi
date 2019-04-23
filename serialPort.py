import config
import serial
import flowmeter

class SerialPort:

    device = None
    baudrate = None
    ser = None
    flowmeters = []

    def __init__(self, device, baudrate):
        config.printMessage("############################")
        config.printMessage("# INITIALIZING SERIAL PORT #")
        config.printMessage("############################")

        self.device = device
        self.baudrate = baudrate
        self.initialize()

        config.printMessage("> Finished Initializing Serial Port\n")


    def initialize(self):
        config.printMessage("> Initializing Serial Port at '" + self.device + "' and at " + str(self.baudrate) + " baudrate")
        self.ser = serial.Serial(self.device, self.baudrate, serial.EIGHTBITS, serial.PARITY_NONE)
        self.ser.flushInput()

    def addFlowmeter(self, number):
        outputNumber = 1 if (number % 2) else 0
        fm = flowmeter.Flowmeter("flow" + str(outputNumber), "keg" + str(number))
        self.flowmeters.append(fm)
        config.printMessage("> Flowmeter '" + fm.name + "' (on device '" + self.device + "') added for '" + fm.kegId + "'")

    def getFlowMeter(self, name):
        retVal = None
        for fm in self.flowmeters:
            if(fm.name == name):
                retVal = fm
        return retVal
