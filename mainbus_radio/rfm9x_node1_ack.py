# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Example to send a packet periodically between addressed nodes with ACK
# Author: Jerry Needell
#
import time
import board
import busio
import digitalio
import adafruit_rfm9x

# set the time interval (seconds) for sending packets
transmit_interval = 10

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip.
# set GPIO pins as necessary -- this example is for Raspberry Pi
CS = digitalio.DigitalInOut(board.GP8)
RESET = digitalio.DigitalInOut(board.GP9)

# Initialize SPI bus.
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# set delay before sending ACK
rfm9x.ack_delay = 0.1
# set node addresses
rfm9x.node = 0xfa
rfm9x.destination = 0xfb
rfm9x.coding_rate = 8
rfm9x.spreading_factor = 7
rfm9x.baudrate = 1320000
# initialize counter
counter = 0
ack_failed_counter = 0
# send startup message from my_node
rfm9x.send_with_ack(bytes("startup message from node {}".format(rfm9x.node), "UTF-8"))

# Wait to receive packets.
print("Waiting for packets...")
# initialize flag and timer
time_now = time.monotonic()
while True:
    # Look for a new packet: only accept if addresses to my_node
    packet = rfm9x.receive()
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw header):", [hex(x) for x in packet[0:4]])
        print("Received (raw payload): {0}".format(packet[4:]))
        print("RSSI: {0}".format(rfm9x.last_rssi))
        # send reading after any packet received
    if time.monotonic() - time_now > transmit_interval:
        # reset timeer
        time_now = time.monotonic()
        counter += 1
        # send a  mesage to destination_node from my_node
        if not rfm9x.send_with_ack(
            bytes("message from node node {} {}".format(rfm9x.node, counter), "UTF-8")
        ):
            ack_failed_counter += 1
            print(" No Ack: ", counter, ack_failed_counter)
