# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Example to send a packet periodically
# Author: Jerry Needell
#
import time
import board
import busio
import digitalio
import rfm9xfsk
# from circuitpython_rfm import rfm9xfsk

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip.
CS = digitalio.DigitalInOut(board.GP8)
RESET = digitalio.DigitalInOut(board.GP9)

# Initialize SPI bus.
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)

# Initialze RFM radio
rfm9xfsk = rfm9xfsk.RFM9xFSK(spi, CS, RESET, RADIO_FREQ_MHZ)

# set the time interval (seconds) for sending packets
transmit_interval = 10

# Note that the radio is configured in LoRa mode so you can't control sync
# word, encryption, frequency deviation, or other settings!

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9xfsk.tx_power = 23


# initialize counter
counter = 0
# send a broadcast mesage
rfm9xfsk.send(bytes("message number {}".format(counter), "UTF-8"))

# Wait to receive packets.
print("Waiting for packets...")
# initialize flag and timer
send_reading = False
time_now = time.monotonic()
while True:
    # Look for a new packet - wait up to 2 seconds:
    packet = rfm9xfsk.receive(timeout=2.0)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw bytes): {0}".format(packet))
        # send reading after any packet received
    if time.monotonic() - time_now > transmit_interval:
        # reset timeer
        time_now = time.monotonic()
        # clear flag to send data
        send_reading = False
        counter = counter + 1
#         message = b"\x48\x65\x6C\x6C\x6F\x20\x57\x6F\x72\x6C\x64\x21\x20\x54\x68\x69\x73\x20\x69\x73\x20\x61\x20\x74\x65\x73\x74\x20\x6D\x65\x73\x73\x61\x67\x65\x21\x20\x3A\x44\x20\x48\x6F\x70\x65\x66\x75\x6C\x6C\x79\x20\x74\x68\x69\x73\x20\x77\x6F\x72\x6B\x73\x2C\x20\x77\x68\x69\x63\x68\x20\x6D\x65\x61\x6E\x73\x20\x49\x20\x68\x61\x76\x65\x20\x73\x75\x63\x63\x65\x73\x73\x66\x75\x6C\x6C\x79\x20\x69\x6E\x74\x65\x72\x63\x65\x70\x74\x65\x64\x20\x74\x68\x65\x20\x62\x65\x61\x63\x6F\x6E\x21\x0A"
#         message = b"\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00"
        message = b"\xFF\x00\xFF\x00\x48\x65\x6C\x6C\x6F\x20\x57\x6F\x72\x6C\x64\x21\x20\x54\x68\x69\x73\x20\x69\x73\x20\x61\x20\x74\x65\x73\x74\x20\x6D\x65\x73\x73\x61\x67\x65\x21\x20\x3A\x44\x20\x48\x6F\x70\x65\x66\x75\x6C\x6C\x79\x20\x74\x68\x69\x73\x20\x77\x6F\x72\x6B\x73\x2C\x20\x77\x68\x69\x63\x68\x20\x6D\x65\x61\x6E\x73\x20\x49\x20\x68\x61\x76\x65\x20\x73\x75\x63\x63\x65\x73\x73\x66\x75\x6C\x6C\x79\x20\x69\x6E\x74\x65\x72\x63\x65\x70\x74\x65\x64\x20\x74\x68\x65\x20\x62\x65\x61\x63\x6F\x6E\x21\x0A"
        print(message)
        rfm9xfsk.send(message)
#         rfm9xfsk.send(bytes("message number {}".format(counter), "UTF-8"))

