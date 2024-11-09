import base64
import cv2
import hashlib
import numpy as np
import os
import sys

# Hashing and encryption
def string_to_binary(text: str) -> str:
    """Convert a string into its binary representation."""
    return ''.join(format(ord(char), '08b') for char in text)

def xor_encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    """XOR-based encryption/decryption."""
    return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))

def encode_pw64(input_text: str, password: str) -> str:
    """Encrypt a string with a password and encode it in base64."""
    key = hashlib.sha256(password.encode()).digest()
    encrypted_data = xor_encrypt_decrypt(input_text.encode(), key)
    return base64.b64encode(encrypted_data).decode('utf-8')

def decode_pw64(encoded_text: str, password: str) -> str:
    """Decode base64 string and decrypt it with the password."""
    key = hashlib.sha256(password.encode()).digest()
    encrypted_data = base64.b64decode(encoded_text)
    decrypted_data = xor_encrypt_decrypt(encrypted_data, key)
    return decrypted_data.decode('utf-8')

# Custom exception
class StegoGenException(Exception):
    pass

class StegnoGen:
    def __init__(self):
        self.image = None
        self.height, self.width, self.nbchannels = None, None, None

    def check_filepath(self, f_path: str) -> bool:
        """Check if file exists at specified path."""
        if os.path.exists(f_path):
            return True
        print(f"File: {f_path} does not exist")
        sys.exit()

    def generate_random_image(self, width=1, height=1, layers=0, output_path="output/default.png"):
        """Generate a random noise image and save it."""
        channels = 1 if layers == 0 else 3
        noise = np.random.randint(128, 256, (height, width, channels), dtype=np.uint8)
        cv2.imwrite(output_path, noise)
        self.image = noise
        self.height, self.width, self.nbchannels = noise.shape

    def read_image(self, f_path: str):
        """Read an image from a file."""
        if self.check_filepath(f_path):
            self.image = cv2.imread(f_path)
            self.height, self.width, self.nbchannels = self.image.shape

    def read_text_file(self, f_path: str) -> str:
        """Read text from a file."""
        if self.check_filepath(f_path):
            with open(f_path, "r") as f:
                return f.read()

    def embed_string_to_image(self, input_text: str, password: str, output_path: str):
        """Embed a string into the image's LSBs after encrypting it."""
        encoded_str64 = encode_pw64(input_text, password)
        binary_text = string_to_binary(encoded_str64) + '00000000'  # Null byte termination

        flat_image = self.image.flatten()
        if len(binary_text) > len(flat_image):
            raise StegoGenException("Text is too long to embed in the provided image.")

        for i, bit in enumerate(binary_text):
            flat_image[i] = (flat_image[i] & 0xFE) | int(bit)  # Set LSB to bit

        modified_image = flat_image.reshape(self.image.shape)
        cv2.imwrite(output_path, modified_image)
        print(f"Text embedded in image saved as {output_path}")

    def extract_text_from_image(self, password: str) -> str:
        """Extract text embedded in the image's LSBs and decrypt it."""
        flat_image = self.image.flatten()
        bits = ''.join(str(pixel & 1) for pixel in flat_image)

        binary_text = [bits[i:i + 8] for i in range(0, len(bits), 8)]
        characters = ''.join(chr(int(char, 2)) for char in binary_text)
        end_marker = characters.find('\x00')
        extracted_text = characters[:end_marker] if end_marker != -1 else characters

        return decode_pw64(extracted_text, password)
