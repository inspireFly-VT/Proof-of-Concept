# SPDX-FileCopyrightText: 2024 Ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of sending and recieving data with the rfm9x FSK radio.
# Author: Jerry Needell
import board
import time
import busio
import digitalio
import rfm9xfsk
from DataToAX25_sat import encode_ax25_frame
from DataToAX25_sat import decode_ax25_frame

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.GP8)
RESET = digitalio.DigitalInOut(board.GP9)

# Initialize SPI bus.
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)

# Initialze RFM radio
rfm9xfsk = rfm9xfsk.RFM9xFSK(spi, CS, RESET, RADIO_FREQ_MHZ)

# set the time interval (seconds) for sending packets
transmit_interval = 5

# Print out some chip state:
print("Temperature: {0}C".format(rfm9xfsk.temperature))
print("Frequency: {0}mhz".format(rfm9xfsk.frequency_mhz))
print("Bit rate: {0}kbit/s".format(rfm9xfsk.bitrate / 1000))
print("Frequency deviation: {0}hz".format(rfm9xfsk.frequency_deviation))

# Send a packet.  Note you can only send a packet up to 60 bytes in length.
# This is a limitation of the radio packet size, so if you need to send larger
# amounts of data you will need to break it into smaller send calls.  Each send
# call will wait for the previous one to finish before continuing.
rfm9xfsk.send(bytes("Hello world!\r\n", "utf-8"))
print("Sent hello world message!")

# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 60 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.
print("Waiting for packets...")
time_now = time.monotonic()
can_send = True
hasPicture = False

# Send joke to groundstation
SATjoke = b'\x20'
# Send simple health data periodically
SATbeacon = b'\x21'
# Send simple health data and that SAT has a picture
SATbeaconPic = b'\x22'
# Send state of health
SATSOH = b'\x25'
# Send state of health and that SAT has a picture
SATSOHpic = b'\x26'
# Send the picture
SATselfie = b'\x28'

# Satellite print 'no-op' to console
GSnoop = b'\x10'
# Reset the satellite
GShardReset = b'\x11'
# Put satellite into listen mode
GSshutdown = b'\x12'
# Evaluate string as code
GSquery = b'\x13'
# Evaluate block as code
GSexecuteCommand = b'\x14'
# Satellite send joke to ground station
GSjokeReply = b'\x15'
# Satellite send state of health
GSsendSOH = b'\x16'
# Enable picture taking mode
GStakePic = b'\x31'
# Send picture packet at N down
GSrecievePicNFromSat = b'\x32'
# Send picture packet at N+1 down
GSrecievePicNPlusOneFromSat = b'\x34'
# Ground station is sending picture up
GSsendPicToSat = b'\x34'

satelliteMode = SATbeacon
PictureIndex = 0

while True:
    packet = rfm9xfsk.receive(timeout=transmit_interval)
    # Optionally change the receive timeout from its default of 0.5 seconds:
    # packet = rfm9xfsk.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been received
        # if can_send == True:
#             print("Hello world, how are you today?")
            if(satelliteMode == SATbeacon):
                message = bytes("Hello world! :D", "UTF-8")
                
            ax25_message = encode_ax25_frame(message, 'K4KDJ', 'K4KDJ', satelliteMode)
#             print(len(ax25_message))         
            print(ax25_message)
            rfm9xfsk.send(ax25_message)
            print(satelliteMode)
            # can_send = False
    else:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw bytes): {0}".format(packet))
        # And decode to ASCII text and print it too.  Note that you always
        # receive raw bytes and need to convert to a text format like ASCII
        # if you intend to do string processing on your data.  Make sure the
        # sending side is sending ASCII data before you try to decode!
        groundStationCommand, fcsCorrect = decode_ax25_frame(packet)
        
        message = "No Message"
        
        if(groundStationCommand == GSnoop):
            print("Recieved Command: No_op")
        elif(groundStationCommand == GShardReset):
            print("RecievedCommand: Hard Reset")
        elif groundStationCommand == GSshutdown:
            print("RecievedCommand: Shut Down")
        elif groundStationCommand == GSquery:
            print("RecievedCommand: Query")
        elif groundStationCommand == GSexecuteCommand:
            print("RecievedCommand: Execute Command")
        elif groundStationCommand == GSjokeReply:
            print("RecievedCommand: Joke Reply")
        elif groundStationCommand == GSsendSOH:
            print("RecievedCommand: Send SOH")
            satelliteMode = SATSOH
            message = "Sattelite Mode: Send State Of Health"
        elif groundStationCommand == GStakePic:
            print("RecievedCommand: Take Picture")
            satelliteMode = SATbeaconPic
            message = "Satellite Mode : Beacon With Picture"
        elif groundStationCommand == GSrecievePicNFromSat:
            print("RecievedCommand: Send Pic " + str(PictureIndex))
            satelliteMode = SATselfie
            message = "Satellite Mode: Send Pic " + str(PictureIndex)
        elif groundStationCommand == GSrecievePicNPlusOneFromSat:
            PictureIndex = PictureIndex+1
            print("RecievedCommand: Send Pic " + str(PictureIndex))
            satelliteMode = SATselfie
            message = "Satellite Mode: Send Pic " + str(PictureIndex)            
        elif groundStationCommand == GSsendPicToSat:
            print("RecievedCommand: Recieve Pic from GS")
        else:
            print("RecievedCommand: Unknown")
            
        ax25_message = encode_ax25_frame(message, 'K4KDJ', 'K4KDJ', satelliteMode)

        rssi = rfm9xfsk.last_rssi
        print("Received signal strength: {0} dB".format(rssi))

