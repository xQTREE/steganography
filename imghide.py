from PIL import Image
import os.path
from os import path
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome import Random
import base64
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
from rich import print
from rich.console import Console
from rich.table import Table
import getpass
import sys
from time import sleep
import re

DEBUG = False
console = Console()
headerText = "M6nMjy5THr2J"

def encrypt(key, source, encode=True):
    """Encrypt the given message using AES encryption."""
    key = SHA256.new(key).digest()  # Hash the key using SHA-256
    IV = Random.new().read(AES.block_size)  # Initialization vector
    encryptor = AES.new(key, AES.MODE_CBC, IV)  # CBC mode with the generated IV
    padding = AES.block_size - len(source) % AES.block_size  # Padding for block size
    source += bytes([padding]) * padding  # Add padding to the message
    data = IV + encryptor.encrypt(source)  # Prepend the IV to the encrypted data
    return base64.b64encode(data).decode() if encode else data

def decrypt(key, source, decode=True):
    """Decrypt the given AES-encrypted message."""
    if decode:
        source = base64.b64decode(source)  # Decode the base64 string
    key = SHA256.new(key).digest()  # Hash the key
    IV = source[:AES.block_size]  # Extract the initialization vector
    decryptor = AES.new(key, AES.MODE_CBC, IV)  # CBC mode decryption
    data = decryptor.decrypt(source[AES.block_size:])  # Decrypt the data
    padding = data[-1]  # The last byte is the padding value
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")
    return data[:-padding]  # Remove the padding

def convertToRGB(img):
    """Convert an RGBA image to RGB."""
    try:
        rgba_image = img
        rgba_image.load()
        background = Image.new("RGB", rgba_image.size, (255, 255, 255))
        background.paste(rgba_image, mask=rgba_image.split()[3])
        print("[yellow]Converted image to RGB [/yellow]")
        return background
    except Exception as e:
        print(f"[red]Couldn't convert image to RGB[/red] - {e}")

def getPixelCount(img):
    """Return the number of pixels in the image."""
    width, height = Image.open(img).size
    return width * height

def encodeImage(image, message, filename):
    """Encode the message into the image."""
    with console.status("[green]Encoding image...", spinner="dots"):
        try:
            width, height = image.size
            pix = image.getdata()

            current_pixel = 0
            x = 0
            y = 0
            tmp = 0
            for ch in message:
                binary_value = format(ord(ch), '08b')

                p1 = pix[current_pixel]
                p2 = pix[current_pixel+1]
                p3 = pix[current_pixel+2]

                three_pixels = [val for val in p1 + p2 + p3]

                for i in range(0, 8):
                    current_bit = binary_value[i]
                    if current_bit == '0' and three_pixels[i] % 2 != 0:
                        three_pixels[i] -= 1 if three_pixels[i] == 255 else 1
                    elif current_bit == '1' and three_pixels[i] % 2 == 0:
                        three_pixels[i] += 1 if three_pixels[i] == 255 else 1

                current_pixel += 3
                tmp += 1

                if tmp == len(message):
                    if three_pixels[-1] % 2 == 0:
                        three_pixels[-1] += 1 if three_pixels[-1] == 255 else 1
                else:
                    if three_pixels[-1] % 2 != 0:
                        three_pixels[-1] -= 1 if three_pixels[-1] == 255 else 1

                three_pixels = tuple(three_pixels)
                st, end = 0, 3
                for i in range(3):
                    image.putpixel((x, y), three_pixels[st:end])
                    st += 3
                    end += 3
                    if x == width - 1:
                        x = 0
                        y += 1
                    else:
                        x += 1

            encoded_filename = filename.split('.')[0] + "-enc.png"
            image.save(encoded_filename)
            print(f"\n[yellow]Original File: {filename}[/yellow]")
            print(f"[green]Image encoded and saved as [u][bold]{encoded_filename}[/u][/bold][/green]")

        except Exception as e:
            print(f"[red]An error occurred - {e}[/red]")
            sys.exit(0)

def decodeImage(image):
    """Decode the message from the image."""
    with console.status("[green]Decoding image...", spinner="dots"):
        try:
            pix = image.getdata()
            current_pixel = 0
            decoded = ""
            while True:
                binary_value = ""
                p1 = pix[current_pixel]
                p2 = pix[current_pixel+1]
                p3 = pix[current_pixel+2]
                three_pixels = [val for val in p1 + p2 + p3]

                for i in range(0, 8):
                    binary_value += '0' if three_pixels[i] % 2 == 0 else '1'

                ascii_value = int(binary_value, 2)
                decoded += chr(ascii_value)
                current_pixel += 3

                if three_pixels[-1] % 2 != 0:
                    break

            return decoded
        except Exception as e:
            print(f"[red]An error occurred - {e}[/red]")
            sys.exit()

def main():
    """Main function to handle user interaction."""
    while True:
        print("[cyan]Select the option (number): [/cyan]")
        op = int(input("1. Encode\n2. Decode\n0. Exit\n>>"))

        if op == 1:
            print("[cyan]Image path (with extension): [/cyan]")
            img = input(">>")
            if not path.exists(img):
                raise Exception("Image not found!")

            print("[cyan]Message to be hidden: [/cyan]")
            message = input(">>")
            message = headerText + message
            if (len(message) + len(headerText)) * 3 > getPixelCount(img):
                raise Exception("Given message is too long to be encoded in the image.")

            password = ""
            while True:
                print("[cyan]Password to encrypt (leave empty if you want no password): [/cyan]")
                password = getpass.getpass(">>")
                if password == "":
                    break
                print("[cyan]Re-enter Password: [/cyan]")
                confirm_password = getpass.getpass(">>")
                if password != confirm_password:
                    print("[red]Passwords don't match, try again[/red]")
                else:
                    break

            cipher = ""
            if password != "":
                cipher = encrypt(key=password.encode(), source=message.encode())
                cipher = headerText + cipher  # Add header to cipher
            else:
                cipher = message

            image = Image.open(img)
            if image.mode != 'RGB':
                image = convertToRGB(image)
            encodeImage(image=image.copy(), message=cipher, filename=img)

        elif op == 2:
            print("[cyan]Image path (with extension): [/cyan]")
            img = input(">>")
            if not path.exists(img):
                raise Exception("Image not found!")

            print("[cyan]Enter password (leave empty if no password): [/cyan]")
            password = getpass.getpass(">>")

            image = Image.open(img)
            cipher = decodeImage(image)

            #if cipher.startswith(headerText):
            cipher = cipher.removeprefix(headerText)
            #cipher = cipher[len(headerText):]  # Strip header before decryption

            if password != "":
                try:
                    decrypted = decrypt(key=password.encode(), source=cipher)
                except Exception:
                    print("[red]Wrong password![/red]")
                    sys.exit(0)
            else:
                decrypted = cipher

            # Ensure that decrypted text is shown correctly
            if isinstance(decrypted, bytes):
                decrypted = decrypted.decode('utf-8')

            if headerText in decrypted:
                decrypted = re.sub(headerText,"",decrypted,1)
            print(f"[green]Decoded Text: \n[bold]{decrypted}[/bold][/green]")

        elif op == 0:
            print("[yellow]Exiting...[/yellow]")
            break

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    cprint(figlet_format('STEGANO', font='starwars'), 'green', attrs=['bold'])
    print()
    print("[bold]STEGANO[/bold] [yellow]allows you to embed payload inside an image. You can also protect these payloads with a password using AES-256.[/yellow]")
    print()
    main()