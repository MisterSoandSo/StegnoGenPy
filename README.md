# StegnoGenPy

![App Result](media/top0.png)

 StegnoGenPy is a proof-of-concept app for embedding text in randomly generated images (color/greyscale) using steganography. It obfuscates text with base64 and hashing for added security. The tool supports encoding and decoding, offering a basic, secure way to hide and retrieve information in images.

## Usage
* read_image(): Accepts an input image file to initialize the StegnoGen image object.
* generate_random_image(width, height, layers): Generates a random image based on specified dimensions. Set layers to 0 for a greyscale image or 3 for an RGB image.
* embed_string_to_image(input_str, password, output_filepath="output/default.png"): Embeds a string into an image using a password. If output_filepath is not provided, it defaults to "output/default.png".
* extract_text_from_image(password): Uses a password to extract and decode the hidden string from the image.

## Limitations
Avoid compressing images, as this may lead to data loss.

## Requirements
To get started, ensure you have all the necessary dependencies. You can install them using the following command:
```
pip install -r requirements.txt
```

## Setup Virtual Environment
In the console or terminal, type `python -m venv venv` to initialize the python virtual environment. In linux, you might have to run `sudo apt update && apt update -y` to install pip for later uses.
```
# Windows Users
.\venv\Scripts\activate

# Unix/ Mac Users
source venv/bin/activate

# Exit venv Command
deactivate

```-