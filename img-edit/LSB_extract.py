import numpy as np
import PIL.Image

image = PIL.Image.open('encoded.png', 'r')
img_arr = np.array(list(image.getdata()))

channels = 4 if image.mode == 'RGBA' else 3

pixels = img_arr.size //channels

secret_bits = [bin(img_arr[i][j])[-1] for i in range(pixels) for j in range(0, 3)]
secret_bits = ''.join(secret_bits)
secret_bits = [secret_bits[i:i+8] for i in range(0, len(secret_bits), 8)]

secret_msg = [chr(int(secret_bits[i], 2)) for i in range(len(secret_bits))]
secret_msg = ''.join(secret_msg)

stop_indicator = "$NEURAL$"

if stop_indicator in secret_msg:
    print(secret_msg[:secret_msg.index(stop_indicator)])
else:
    print("Couldn't find secret message")