'''First 8 bytes: 89 50 4e 47 0d 0a 1a 0a (PNG File Signature)
Last 12 bytes: 00 00 00 00 49 45 4e 44 ae 42 60 82 (.....IEND.B'.|)

Then chunks:
IHDR = Header
PLTE = Palette Table
IDAT = Image Data
IEND = End of File
'''

# hexdump -C {img_name}

end_hex = b"\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"

with open('image.png', 'ab') as f:
    f.write(b"Hello World! This is my secret!")

# NEXT

with open('image.png', 'rb') as f:
    content = f.read()
    offset = content.index(end_hex)
    f.seek(offset + len(end_hex))
    print(f.read())

###

with open('image.png', 'ab') as f, open('procexp64.exe', 'rb') as e:
    f.write(e.read())

###

with open('image.png', 'rb') as f:
    content = f.read()
    offset = content.index(end_hex)
    f.seek(offset + len(end_hex))

    with open('newexe.exe', 'wb') as e:
        e.write(f.read())
