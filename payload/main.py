from time import sleep
from ssd1351 import Display
from machine import Pin, SPI
from Camera import *
import os

spi = SPI(0, baudrate=14500000, sck=Pin(18), mosi=Pin(19))  # Using machine.SPI directly
display = Display(spi, dc=Pin(14), cs=Pin(21), rst=Pin(7))  # Adjust pin assignments

print("Displaying RaspberryPiWB128x128.raw image...")
display.draw_image('RaspberryPiWB128x128.raw', 0, 0, 128, 128)

spi = SPI(1,sck=Pin(10), miso=Pin(8), mosi=Pin(11), baudrate=8000000)
cs = Pin(9, Pin.OUT)
# button = Pin(15, Pin.IN,Pin.PULL_UP)
onboard_LED = Pin(25, Pin.OUT)
cam = Camera(spi, cs)

def TakePicture(imageName, resolution):
    onboard_LED.on()
    finalImageName = imageName
    # Read the last number used from the file
    try:
        with open('last_num.txt', 'r') as f:
            last_num = int(f.read())
    except OSError:
        # If the file doesn't exist, start from 1
        last_num = 1
    # Add the number to the image name
    finalImageName += str(last_num) + '.jpg'
    cam.resolution = resolution
    #Kept getting an error saying to add 500ms of delay
    sleep_ms(500)
    cam.capture_jpg()
    sleep_ms(500)
    cam.saveJPG(finalImageName)
    onboard_LED.off()
    # Increment the number and write it back to the file
    with open('last_num.txt', 'w') as f:
        f.write(str(last_num + 1))



# def TakePicture(imageName, resolution, interval, count):
#     cam.resolution = resolution
#     for x in range(count):
#         if x!=0:
#             endImageName = imageName + str(x + 1) + '.jpg'
#             try:
#                 uos.remove(endImageName)
#             except:
#                 print("File does not exist")
#     for x in range(count): 
#         endImageName = imageName + str(x + 1) + '.jpg'
#         TakePicture(endImageName, resolution)
#         sleep_ms(500)
#         if x==0:
#             uos.remove(endImageName)
#         sleep_ms(interval)

def TakePicture(imageName, resolution):
    onboard_LED.on()
    finalImageName = imageName
    if not '.jpg' in finalImageName:
        finalImageName = finalImageName + '.jpg'
    cam.resolution = resolution
    #Kept getting an error saying to add 500ms of delay
    sleep_ms(500)
    cam.capture_jpg()
    sleep_ms(500)
    cam.saveJPG(finalImageName)
    onboard_LED.off()

def TakeMultiplePictures(imageName, resolution, interval, count):
    cam.resolution = resolution
    for x in range(count):
        if x!=0:
            endImageName = imageName + str(x + 1) + '.jpg'
            try:
                uos.remove(endImageName)
            except:
                print("File does not exist")
    for x in range(count): 
        endImageName = imageName + str(x + 1) + '.jpg'
        TakePicture(endImageName, resolution)
        sleep_ms(500)
        if x==0:
            uos.remove(endImageName)
        sleep_ms(interval)

# TakePicture('inspireFly_Capture_#', '320x240')
TakeMultiplePictures('inspireFly_Capture', '640x480', 500, 2)


#Check image for blue bits
#If set percentage of blue bits exists, 
