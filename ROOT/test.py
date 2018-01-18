def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

s = "011010000110100100000"
#b'\xd0\xd2UUT'
#b'hi*\xaa\xaa\x00'
print(len(s))
print(bitstring_to_bytes(s))