# with open('photo.jpg', 'ab') as f:
#     f.write(b"Hello World")

with open('photo.jpg', 'rb') as f:
    content = f.read()
    offset = content.index(bytes.fromhex('FFD9'))

    f.seek(offset + 2)
    print(f.read())

###

import PIL.Image
import io

img = PIL.Image.open('heart.png')
byte_arr = io.ByteIO()
img.save(byte_arr, format='PNG')

with open('photo.jpg', 'ab') as f:
    f.write(byte_arr.getvalue())

###

with open('test.jpg', 'rb') as f:
    content = f.read()
    offset = content.index(bytes.fromhex('FFD9'))

    f.seek(offset + 2)

    new_img = PIL.Image.open(io.ByteIO(f.read()))
    new_img.save("new_image.png")

### executable

with open('photo.jpg', 'ab') as f, open('procexp64.exe', 'rb') as e:
    f.write(e.read())

#

with open('photo.jpg', 'rb') as f:
    content = f.read()
    oddset = content.index(bytes.fromhex('FFD9'))

    f.seek(offset + 2)

    with open('newfile.exe', 'wb') as e:
        e.write(f.read())