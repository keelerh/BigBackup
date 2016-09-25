#!/usr/bin/env python

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

"""AES CFB Stream Cipher Tool"""

from Crypto.Cipher import AES
from Crypto import Random
from argparse import ArgumentParser
import base64, sys

def main():
    # Set-up a command-line argument parser
    parser = ArgumentParser(description=__doc__, epilog="""Input is read from
        stdin and output is written to stdout. Use the stream redirection
        features of your shell to pass data through this program. If a key is
        not specified, it is generated and written to stderr.""")
    parser.add_argument('-d', '--decrypt', action='store_true')
    parser.add_argument('-k', '--key', metavar='key')
    args = parser.parse_args()

    # Decode the key if it was supplied
    key = base64.b64decode(args.key) if args.key else None

    # -- DECRYPT --

    if args.decrypt:
        # Check to see if a key was supplied
        if key is None:
            sys.stderr.write('Error: Please supply a decryption key.\n')
            exit(1)

        # Read in the initialization vector
        iv = sys.stdin.read(AES.block_size)

        # Create the cipher object and process the input stream
        cipher = AES.AESCipher(key, AES.MODE_CFB, iv)
        method = cipher.decrypt

        # Stream is processed below...

    # -- ENCRYPT --

    else:
        # Create a file object that produces random data when read from
        random = Random.new()

        # Generate a key if one was not supplied
        if key is None:
            key = random.read(AES.key_size[0])
            sys.stderr.write('Encryption Key: %s\n' % base64.b64encode(key))

        # Create the initialization vector
        iv = random.read(AES.block_size)
        sys.stdout.write(iv)

        # Create the cipher object and process the input stream
        cipher = AES.AESCipher(key, AES.MODE_CFB, iv)
        method = cipher.encrypt

        # Stream is processed below...

    # Process the input stream
    while True:
        data = sys.stdin.read(AES.block_size)
        if data == '': break # Check for EOF
        sys.stdout.write(method(data))

if __name__ == '__main__':
    main()
