import config

class KegomateSerialMessage:

    tag = None
    serial = None
    messageId = None
    payloadLength = None
    crc = None
    trailer = None
    values = []

    TICKS_PER_GALLON = 4994
    FL_OZ_PER_GALLON = 128
    NUMBER_OF_TICKS = 65535

    def __init__(self, serial, messageId, payloadLength):
        config.printMessage("############################################")
        config.printMessage("# BEGIN PROCESSING KEGOMATE SERIAL MESSAGE #")
        config.printMessage("############################################")

        self.serial = serial
        self.messageId = messageId
        self.payloadLength = payloadLength
        self.process()

        config.printMessage("> Finished Processing Message\n")

    def process(self):
        config.printMessage("> Processing Message ID of " + str(self.messageId.encode('hex')))

        if(self.messageId.encode('hex') == "0010"):
            self.processMeterReading()
        elif(self.messageId.encode('hex') == "0001"):
            self.processHelloMessage()
        else:
            config.printMessage("Error: Not able to process unrecognized message_id")
        self.processFooter()

    def processTypeLengthValue(self):
        tlv = {}
        tlv['tag'] = self.serial.read(1)
        tlv['length'] = self.serial.read(1).encode('hex')
        tlv['value'] = self.serial.read(int(tlv['length'], 16))
        return tlv

    def processMeterReading(self):
        config.printMessage("> Identified as a Meter Reading Message")
        self.values.append(self.processTypeLengthValue())
        self.values.append(self.processTypeLengthValue())

        for i in self.values:
            if(i['tag'].encode('hex') == "01"):
                config.printMessage("> Flow Meter Name: " + i['value'])
            elif(i['tag'].encode('hex') == "02"):
                rawValue = i['value'].encode('hex')
                meterReading = rawValue[2] + rawValue[3] + rawValue[0] + rawValue[1]
                config.printMessage("> Flow Meter Reading: " + str(int(meterReading, 16)))
            else:
                config.printMessage("Error: Unknown tag value")


    def processHelloMessage(self):
        config.printMessage("> Identified as a Hello Reading Message")
        self.values.append(self.processTypeLengthValue())
        self.values.append(self.processTypeLengthValue())
        self.values.append(self.processTypeLengthValue())

        for i in self.values:
            if(i['tag'].encode('hex') == "01"):
                rawValue = i['value'].encode('hex')
                firmwareVersion = rawValue[0] + rawValue[1]
                config.printMessage("> Firmware Version: " + str(int(firmwareVersion, 16)))
            elif(i['tag'].encode('hex') == "02"):
                rawValue = i['value'].encode('hex')
                protocolVersion = rawValue[2] + rawValue[3] + rawValue[0] + rawValue[1]
                config.printMessage("> Protocal Version: " + str(int(protocolVersion, 16)))
            elif(i['tag'].encode('hex') == "03"):
                config.printMessage("> Board Serial Number: " + i['value'])
            elif(i['tag'].encode('hex') == "04"):
                rawValue = i['value'].encode('hex')
                millis = rawValue[2] + rawValue[3] + rawValue[0] + rawValue[1]
                config.printMessage("> Uptime in Milliseconds: " + str(int(millis, 16)))
            elif(i['tag'].encode('hex') == "05"):
                rawValue = i['value'].encode('hex')
                days = rawValue[2] + rawValue[3] + rawValue[0] + rawValue[1]
                config.printMessage("> Uptime in Milliseconds: " + str(int(days, 16)))
            else:
                config.printMessage("Error: Unknown tag value")

    def processFooter(self):
        self.crc = self.serial.read(2)
        self.trailer = self.serial.read(2)
        config.printMessage("> CRC is " + self.crc.encode('hex'))

    def getFlowMeterName(self):
        retVal = None
        for i in self.values:
            if(i['tag'].encode('hex') == "01"):
                retVal = i['value']
        return retVal

    def getFlowMeterReading(self):
        retVal = None
        for i in self.values:
            if(i['tag'].encode('hex') == "02"):
                rawValue = i['value'].encode('hex')
                meterReading = rawValue[2] + rawValue[3] + rawValue[0] + rawValue[1]
                retVal = int(meterReading, 16)
        return retVal

    def getHexMessageId(self):
        return self.messageId.encode('hex')

    def clearValues(self):
        del self.values[:]

    def kegomateAmountConversation(self, first, last):
        if(last < first):
            last = last + NUMBER_OF_TICKS # DOES THE MATH FOR RECYCLE ON TICKS
        retVal = (last-first) * self.FL_OZ_PER_GALLON / float(self.TICKS_PER_GALLON)
        return retVal
