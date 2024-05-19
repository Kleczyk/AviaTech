import base64
import struct
import numpy as np

float_array =  [0.0] * 512

byte_data = struct.pack('f' * 512, *float_array)
base64_encoded_data = base64.b64encode(byte_data).decode('utf-8')

print(base64_encoded_data)
