import sys

def main():
    if len(sys.argv) == 5:
        if len(sys.argv[2]) == 10:
            if sys.argv[1] == '-e' or sys.argv[1] == '-d':
                feistel(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
            else:
                print("Invalid flag: " + sys.argv[1])
                usage()
        else:
            print("Key must be 10 bits in length. Try again...")
    else:
        usage()

def feistel(mode, key, file1, file2):
    sub_keys = keyScheduler(key)
    input_file = open(file1, 'rb')
    # Clearing output file before appending to it
    output_file = open(file2, 'w')
    output_file.close()
    output_file = open(file2, 'ab')

    byte = input_file.read(1)
    while True:
        message = ''.join("{:08b}".format(ord(byte), 'b'))
        ip_permutation = (message[1], message[5], message[2], message[0], message[3], message[7], message[4], message[6])
        ip = ''.join(ip_permutation)
        cipher_r1 = ""
        cipher_r2 = ""
        if mode == '-e':
            cipher_r1 = sDES(sub_keys[0], ip)
            cipher_r1 = transpose(cipher_r1)
            cipher_r2 = sDES(sub_keys[1], cipher_r1)
        elif mode == '-d':
            cipher_r1 = sDES(sub_keys[1], ip)
            cipher_r1 = transpose(cipher_r1)
            cipher_r2 = sDES(sub_keys[0], cipher_r1)
        cipher_final_permutation = (cipher_r2[3], cipher_r2[0], cipher_r2[2], cipher_r2[4], cipher_r2[6], cipher_r2[1], cipher_r2[7], cipher_r2[5])
        cipher_final = ''.join(cipher_final_permutation)

        # Convert string binary representation back to binary representation and write to file
        cipher_final = int(cipher_final, 2)
        output_file.write(cipher_final.to_bytes(1, 'big'))

        byte = input_file.read(1)
        if byte == b'':
            break

def sDES(sub_key, byte):
    H_byte_L = byte[0:4]
    H_byte_R = byte[4:8]

    E_H_byte_R = expand(H_byte_R)
    # XOR
    E_H_byte_R_int = int(E_H_byte_R, 2)
    sub_key_int = int(sub_key, 2)
    XOR_byte_int = E_H_byte_R_int ^ sub_key_int
    XOR_byte = "{:08b}".format(XOR_byte_int, 'b')
    XOR_H_byte_L = XOR_byte[0:4]
    XOR_H_byte_R = XOR_byte[4:8]

    # Substitutions
    Q_byte_L = sub0(XOR_H_byte_L)
    Q_byte_R = sub1(XOR_H_byte_R)
    p4 = "" + Q_byte_L[1] + Q_byte_R[1] + Q_byte_R[0] + Q_byte_L[0]

    # Final XOR
    H_byte_L_int = int(H_byte_L, 2)
    H_byte_P4_int = int(p4, 2)
    H_byte_final_L_int = H_byte_L_int ^ H_byte_P4_int
    H_byte_final_L = "{:04b}".format(H_byte_final_L_int, 'b')

    byte_final = "" + H_byte_final_L + H_byte_R

    return byte_final

def sub0(H_byte):
    row = "" + H_byte[0] + H_byte[3]
    column = "" + H_byte[1] + H_byte[2]
    row = int(row, 2)
    column = int(column, 2)

    s0_table = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
    sub_val = s0_table[row][column]
    Q_byte = "{:02b}".format(sub_val, 'b')

    return Q_byte

def sub1(H_byte):
    row = "" + H_byte[0] + H_byte[3]
    column = "" + H_byte[1] + H_byte[2]
    row = int(row, 2)
    column = int(column, 2)

    s1_table = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
    sub_val = s1_table[row][column]
    Q_byte = "{:02b}".format(sub_val, 'b')

    return Q_byte

def expand(H_byte):
    h_byte_expand = (H_byte[3], H_byte[0], H_byte[1], H_byte[2], H_byte[1], H_byte[2], H_byte[3], H_byte[0])
    byte = ''.join(h_byte_expand)

    return byte

def transpose(byte):
    a = "" + byte[4:8] + byte[0:4]

    return a

def keyScheduler(key):
    sub_keys = []

    # Initial key permutation
    p10_permutation = (key[2], key[4], key[1], key[6], key[3], key[9], key[0], key[8], key[7], key[5])
    p10 = ''.join(p10_permutation)

    # Slice p10 into two halves
    p10_halfA = p10[0:5]
    p10_halfB = p10[5:10]
    # Cyclic shift each half once
    p10_halfA = cyclicLeftShift(p10_halfA)
    p10_halfB = cyclicLeftShift(p10_halfB)
    # Put halves back together
    p10_round_one = p10_halfA + p10_halfB

    # Create first 8-bit round key and add to sub key list
    p8_permutation_r1 = (p10_round_one[5], p10_round_one[2], p10_round_one[6], p10_round_one[3], p10_round_one[7], p10_round_one[4], p10_round_one[9], p10_round_one[8])
    p8_round1 = "".join(p8_permutation_r1)
    sub_keys.append(p8_round1)

    # Slice p10 again into two halves
    p10_halfA = p10_round_one[0:5]
    p10_halfB = p10_round_one[5:10]
    # Cyclic shift each half once
    p10_halfA = cyclicLeftShift(p10_halfA)
    p10_halfA = cyclicLeftShift(p10_halfA)
    p10_halfB = cyclicLeftShift(p10_halfB)
    p10_halfB = cyclicLeftShift(p10_halfB)
    # Put halves back together
    p10_round_two = p10_halfA + p10_halfB

    # Create second 8-bit round key and add to sub key list
    p8_permutation_r2 = (p10_round_two[5], p10_round_two[2], p10_round_two[6], p10_round_two[3], p10_round_two[7], p10_round_two[4], p10_round_two[9], p10_round_two[8])
    p8_round2 = "".join(p8_permutation_r2)
    sub_keys.append(p8_round2)

    return sub_keys

def cyclicLeftShift(bits_to_shift):
    str_end = bits_to_shift[0]
    str_begin = bits_to_shift[1:len(bits_to_shift)]
    outputstr = str_begin + str_end

    return outputstr

def usage():
    print("Usage:\n\tEncryption: sdes -e <key> <plaintext file name> <ciphertext file name>\n\tDecryption: sdes –d <key> <ciphertext file name> <plaintext file name>")

if __name__ == '__main__':
	main()
