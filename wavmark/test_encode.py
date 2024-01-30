# string to a binary of capped length
n = "test test"
l = 7
#print(bin(n))[2:].zfill(l))


# string to binary full
word = "test test"
# convert string to bytearray
byte_arr = bytearray(word, 'utf-8')
res = []
for byte in byte_arr:
    binary_rep = bin(byte)  # convert to binary representation
    res.append(binary_rep[2:])  # remove prefix "0b" and add to list
out_binary = ' '.join(res)
length_max = 16
st = "hello world"
#test_bin= map(bin,bytearray(st))
#print(test_bin)
#truncate_binary = bin(test_bin)[2:].zfill(length_max)
print(out_binary)  # join all the binaries of res list
#print(truncate_binary)
def truncate_bin_shift(n, k):
    return n & -15 >> k
n = 4
k =int(out_binary)
print(k)
#print(truncate_bin_shift(n,k))

