numnber = 1
print("test " + str(numnber+1))
from bchlib import BCH

# bch = BCH(t=6, m=8) t is the number of correctable errors, m is variable, n = 2^m -1 is total size of packet
# size of usable data, k = n - t*m, size of fec code is b = t*m, so k + b = n
# current values of t=6 and m=8 allow for a packet size of 255, usable data size of 207, and 6 errors can be corrected
# This design is currently limited by the radio only being able to send 60 byte packets. If that issue can be resolved,
# and we get up to the advertised 255 byte packets, we are groovin


def bytes_to_bits_binary(byte_data):
    bits_data = bin(int.from_bytes(byte_data, byteorder='big'))[2:]
    return bits_data


def bchenc(msg):
    # Generate a BCH code encoder
    bch = BCH(6, m=8)
    fec = bch.encode(msg)
    # print(fec)
    encodedMessage = msg + fec
    return encodedMessage


def bchdec(msg):
    # Generate a BCH code decoder
    bch = BCH(6, m=8)

    # Separate data and error correction code
    data, ECE = bytearray(msg[:-bch.ecc_bytes]), bytearray(msg[-bch.ecc_bytes:])

    # Decode and correct errors
    numErrors = bch.decode(data=data, recv_ecc=ECE)
    bch.correct(data=data, ecc=ECE)

    return numErrors, data, ECE


msg = b'\xAA\xAA'
msgTx = bchenc(msg)
print(msgTx)
# msgTx = b'\xab\xac\x9a\x81\x05`C\xc7' #testing out data corruption
# print(msgTx)
# print(bytes_to_bits_binary(msgTx))
numErrors, msgRx, FEC = bchdec(msgTx)
print("Number of errors detected: " + str(numErrors))
print(msgRx)
print(FEC)



# Code from example file
# help(BCH)
# max_data_len = bch.n // 8 - (bch.ecc_bits + 7) // 8
#
# print('max_data_len: %d' % (max_data_len,))
# print('ecc_bits: %d (ecc_bytes: %d)' % (bch.ecc_bits, bch.ecc_bytes))
# print('useable bits for data: %d' % (bch.n - bch.ecc_bits))
# print('m, field order: %d' % (bch.m,))
# print('n, max code word size: %d (%d bytes)' % (bch.n, bch.n // 8))
# print('prim_poly: 0x%x' % (bch.prim_poly,))
# print('t, correctable errors: %d' % (bch.t,))