# Simple-DES

An implementation of the Simple DES specification for encryption and decryption.
It uses a 10 bit key to encrypt any file.

Disclaimer: This tool shouldn't be used for anything that requires any degree of real security and was created purely for educational purposes.

More details here:  
https://www.brainkart.com/article/Simplified-Data-Encryption-Standard-(S-DES)_8343/

Usage:  
Encryption: python3 sdes.py -e <key> <plaintext file name> <ciphertext file name>  
Decryption: python3 sdes.py –d <key> <ciphertext file name> <plaintext file name>  

Example:  
python3 sdes.py -e 1011010100 file1.jpg cipher.txt

