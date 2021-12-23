import numpy as np
import struct

a = np.random.randint(0,10,size=[3,3])
print(a)

a.astype('float32').tofile('test.bin')

data = np.fromfile('test.bin','f4')
print('data--->', data)

# unpack_result = struct.unpack('ii', data)
# print('111', unpack_result)
