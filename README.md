# STEGANO

![enter image description here](https://i.ibb.co/4f0RD03/stegano.png)

Hide secret texts/messages inside an image. You can optionally encrypt your texts with a password using AES-256 before encoding into the image.


## Installation
You can install the all requirements from **requirements.txt** by using pip.

    pip install -r requirements.txt


## Usage

    python imghide.py

**Encode**

 - Choose *Encode* in the options menu
 - Enter the image path (with extension)
 - Enter the message to be hidden
 - Choose a password to encrypt with AES-256 (optional)

The image is encoded and saved as a ***PNG*** file.

**Decode**

 - Choose *Decode* from the menu
 - Enter the path of the encoded image (with extension) and type in the password to decrypt (leave empty if no password was used)

The decoded text will be displayed on the terminal.
