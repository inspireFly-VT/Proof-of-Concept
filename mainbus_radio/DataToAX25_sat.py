import binascii

def encode_ax25_frame(data: bytes, dest_callsign: str, source_callsign: str, operatingMode: bytes) -> bytes:
    """
    Encodes a data payload into an AX.25 frame.

    Args:
        data (bytes): The data payload to be transmitted.
        dest_callsign (str): Destination callsign (6 characters).
        source_callsign (str): Source callsign (6 characters).

    Returns:
        bytes: The AX.25 frame.
    """
    # Start flag (0x7E)
    ax25_frame = b'\x7E'
    
    # Kiss 1
    ax25_frame += b'\xc0'

    # Destination address (7 bytes)
    dest_address = f"{dest_callsign}"
    dest_address_bytes = bytes(dest_address, 'ascii')
    shifted_dest_address = bytes([byte << 1 for byte in dest_address_bytes])
    ax25_frame += shifted_dest_address
    ax25_frame += b'\x40'
    ax25_frame += b'\x61'

    # Source address (7 bytes)
    source_address = f"{source_callsign}"
    source_address_bytes = bytes(source_address, 'ascii')
    shifted_source_address = bytes([byte << 1 for byte in source_address_bytes])
    ax25_frame += shifted_source_address
    ax25_frame += b'\x40'
    ax25_frame += b'\x62'

    # Control field (0x03 for UI frames)
    ax25_frame += b'\x03'

    # Protocol ID (0xF0 for no layer 3 protocol)
    ax25_frame += b'\xF0'

    # operatingMode
    ax25_frame += operatingMode

    #Data
    ax25_frame += data
    
    #Kiss 2
    ax25_frame += b'\xc0'

    # FCS (Frame Check Sequence) - Calculate CRC16 and append
    crc = calculate_crc16(ax25_frame)
    ax25_frame += crc.to_bytes(2, 'big')

    # End flag (0x7E)
    ax25_frame += b'\x7E'

    return ax25_frame

def calculate_crc16(data: bytes) -> int:
    crc = 0x1D0F #CCITT-False is 0xFFFF, 
    poly = 0x1021  # CRC-CCITT polynomial

    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF  # Limit to 16 bits

    return crc

def decode_ax25_frame(frame):
    if len(frame) < 14:
        print("Invalid AX.25 frame")
        operatingMode = b'\xFF'
        fcsCorrect = False
        return operatingMode, fcsCorrect

    # AX.25 frame structure:
    # Flag (1 byte) | Destination (7 bytes) | Source (7 bytes) | Control (1 byte) | Protocol ID (1 byte) | Data | FCS (2 bytes) | Flag (1 byte)

    flag1 = frame[:1]
    kiss1 = frame[1:2]
    destination = frame[2:9]
    source = frame[9:16]
    control = frame[16:17]
    protocol_id = frame[17:18]
    operatingMode = frame[18:19]
    data = frame[19:-4]  # Data field
    fcs = frame[-4:-3]  # Frame Check Sequence
    flag2 = frame[-1:]

    # Convert bytes to ASCII for destination and source addresses
    destination_address = ''.join(chr(byte >> 1) for byte in destination)
    source_address = ''.join(chr(byte >> 1) for byte in source)

    # Print decoded information
#     print("Flag1:", flag1)
#     print("Destination Address:", destination_address)
#     print("Source Address:", source_address)
#     print("Control:", control)
#     print("Protocol ID:",protocol_id)
    print("Operation:", operatingMode)
    print("Data:", data)
    print("FCS:", fcs)
#     print("Flag2:", flag2)
    
    test = b''
    test = test + flag1
    test = test + destination
    test = test + source
    test = test + control
    test = test + protocol_id
    test = test + operatingMode
    test = test + data
    newCrc = calculate_crc16(test).to_bytes(2, 'big')
    
    fcsCorrect = False
    if(newCrc == fcs):
        fcsCorrect = True
        
    return operatingMode, fcsCorrect
        
    
# # Example usage
# data_payload = b"Hello, world!"
# dest_callsign = "K4KDJ"
# source_callsign = "K4KDJ"
# ax25_frame = encode_ax25_frame(data_payload, dest_callsign, source_callsign)
# print("AX.25 Frame:", ax25_frame.hex())
# decode_ax25_frame(ax25_frame)