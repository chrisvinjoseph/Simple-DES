# Simple-DES

An implementation of the Simple DES specification for encryption and decryption.
More details here:  
https://www.brainkart.com/article/Simplified-Data-Encryption-Standard-(S-DES)_8343/

Usage:  
Encryption: sdes -e <key> <plaintext file name> <ciphertext file name>  
Decryption: sdes –d <key> <ciphertext file name> <plaintext file name>  

Example:  
sdes -e 1011010100 file1.jpg cipher.txt
