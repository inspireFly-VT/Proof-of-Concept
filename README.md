# Proof-of-Concept
This repository houses all the code and documentation for the payload proof of concept.

The final product of this repository will be a set of code that mimics the mission of ContentCube. This will include the following:
1. A main bus file. This code beacons via radio every 30 seconds, and will tell the payload to take a picture. It will then retrieve the picture from the payload, and feed it to the radio. 
2. Radio code, to allow for the beacon and image transfer to happen
3. Payload code, that listens for the 'take picture' command from the main bus. Once heard, it will take a picture, and transfer the picture back to the main bus.
4. Ground station code, which will request the main bus to send the picture over the radio.

To run this properly, a total of three raspberry PI's will be needed. The payload PI needs to be running micropython, and the main bus and ground station PIs need to be running circuitpython.
