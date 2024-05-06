# Pico_comms_b
# Receives hexadecimal data and converts it to a JPEG image

from easy_comms import Easy_comms
from time import sleep
import binascii

com1 = Easy_comms(uart_id=0, baud_rate=9600)
com1.start()

count = 0
while True:
    # Send a message
    com1.send(f'hello, {count}')
    
    # Check for messages
    message = com1.read()
    
    if message is not None:
        # Decode bytes to string and remove prefix if present
        message = message.decode('utf-8')
        
        try:
            # Decode the received message from hexadecimal to binary
            image_data = binascii.unhexlify(message)
        except Exception as e:
            print(f"Decoding error: {e}")
            continue
        
        # Save the received binary data as a .jpg file
        with open(f'received_image_{count}.jpg', 'wb') as f:
            f.write(image_data)
            
        print(f"Image received and saved: received_image_{count}.jpg")
    
    sleep(1)
    count += 1
