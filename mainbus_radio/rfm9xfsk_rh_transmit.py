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
        print("No message received")
        rfm9xfsk.send(bytes("message number {}".format(counter), "UTF-8"))
