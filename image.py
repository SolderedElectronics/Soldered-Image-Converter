# The class file for the image which will get converted
import os
import re

# Import Pillow
from PIL import Image, ImageOps
import numpy as np
from dither import *

# The class of the image being converted with all it's attributes
class ImageForConversion:
    def __init__(self, num, path="", format=""):
        self.number = num
        self.file_path = path
        self.file_format = format
        self.processed_image_name = "image_"+str(num)
        # Conversion mode 0 is 1-bit
        # Conversion mode 1 is 3-bit
        # Conversion mode 2 is 4-bit
        self.conversion_mode = 0
        self.width = 0
        self.height = 0
        self.original_ratio = 0
        self.bw_tresh = 50
        self.invert = False
        self.resize = False
        self.constrain = False
        self.ditherKernel = 0 # See dither function for what each of the values mean
        self.resultString = "" # The resulting string

    def getPath(self):
        return self.file_path

    def initial_process(self):
        self.process_image_name()
        self.set_conversion_mode(0)
        self.set_default_width_height()
        self.process_image() # Process it right away

    def process_image_name(self):
        # Extract the file name without the extension
        base_name = os.path.basename(self.file_path)
        file_name, _ = os.path.splitext(base_name)

        # Cut the file name at 30 characters and remove spaces or special characters
        file_name = re.sub(r'[^a-zA-Z0-9]', '_', file_name[:30])

        # Update processed_image_name with the cleaned file name
        self.processed_image_name = file_name

    def set_conversion_mode(self, conversion_mode):
        self.conversion_mode = conversion_mode

    def set_default_width_height(self):
        try:
            with Image.open(self.file_path) as img:
                self.width = img.width
                self.height = img.height
                self.original_ratio = float(img.width / img.height)
        except Exception as e:
            print(f"Error: {e}")

    def convert_to_4bit_grayscale(self, img):
        # Convert the image to a numpy array
        img_array = np.array(img)

        # Normalize the pixel values to 0-15 range
        img_array = (img_array // 16) * 16

        # Convert back to an image
        img_4bit = Image.fromarray(img_array)

        return img_4bit

    def convert_to_3bit_grayscale(self, img):
        # Convert the image to a numpy array
        img_array = np.array(img)

        # Normalize the pixel values to 0-7 range
        img_array = (img_array // 32) * 32

        # Convert back to an image
        img_3bit = Image.fromarray(img_array)

        return img_3bit

    # This function processes the image
    def process_image(self):
        try:
            with Image.open(self.file_path) as img:
                # Resize the image if needed
                if self.resize:
                    img = img.resize((self.width, self.height))

                # 1 bit processing
                if self.conversion_mode == 0:
                    # Convert to grayscale
                    img = img.convert("L")
                    # Dithering
                    if self.ditherKernel == 0:
                        # No dithering
                        # Apply threshold to convert to black and white
                        threshold = int(self.bw_tresh * 255 / 100)  # Map threshold from 0 to 100 to 0 to 255
                        img = img.point(lambda p: 255 if p > threshold else 0, '1')  # Apply threshold
                    else:
                        # Dithering
                        img.save("preview.png")  # Save to file
                        img_dither_input = cv2.imread("preview.png", 0)
                        dither_module = ditherModule()
                        img_dither_output = dither_module.dither(img_dither_input, method=self.ditherKernel,
                                                                 resize=False)
                        cv2.imwrite("preview.png", img_dither_output)
                        img = Image.open("preview.png")  # Re-open the image
                        # TODO why does treshold 0 give the desired result here?
                        threshold = 0  # Map threshold from 0 to 100 to 0 to 255
                        img = img.point(lambda p: 255 if p > threshold else 0, '1')  # Apply threshold

                # 3 bit processing
                elif self.conversion_mode == 1:
                    img = img.convert("L")
                    if self.ditherKernel == 0:
                        # No dithering
                        img = self.convert_to_3bit_grayscale(img)
                    else:
                        # dithering
                        img.save("preview.png")  # Save to file
                        img_dither_input = cv2.imread("preview.png", 0)
                        dither_module = ditherModule3bit()
                        img_dither_output = dither_module.dither(img_dither_input, 3,
                                                                 resize=False)
                        cv2.imwrite("preview.png", img_dither_output)
                        img = Image.open("preview.png")  # Re-open the image
                        img = img.convert("L")

                # 4 bit processing
                elif self.conversion_mode == 1 or self.conversion_mode == 2:
                    img = img.convert("L")
                    if self.ditherKernel == 0:
                        # No dithering
                        img = self.convert_to_4bit_grayscale(img)
                    else:
                        # dithering
                        img.save("preview.png")  # Save to file
                        img_dither_input = cv2.imread("preview.png", 0)
                        dither_module = ditherModule4bit()
                        img_dither_output = dither_module.dither(img_dither_input, 3,
                                                                 resize=False)
                        cv2.imwrite("preview.png", img_dither_output)
                        img = Image.open("preview.png")  # Re-open the image
                        img = img.convert("L")
                # If invert is on, invert the image
                if self.invert:
                    img = ImageOps.invert(img.convert("RGB")).convert(img.mode)

                # Save or process the image further as needed
                img.save("preview.png")
                # Convert it to code also!
                # Depending on the different mode the conversion mode is different
                if self.conversion_mode == 0:
                    self.bw_image_to_c_array(img)
                elif self.conversion_mode == 1:
                    self.grayscale_to_c_array_3_bit(img)
                else:
                    self.grayscale_to_c_array_4_bit(img)

        except Exception as e:
            print(f"An error occurred while processing the image: {e}")

    def change_name(self, new_name):
        # Define the regex pattern to find the parts to replace
        pattern = r'const uint8_t\s+\w+\[\] PROGMEM ='
        width_pattern = r'const uint16_t\s+\w+_w ='
        height_pattern = r'const uint16_t\s+\w+_h ='

        # Replace the names in the string
        self.resultString = re.sub(pattern, f'const uint8_t {new_name}[] PROGMEM =', self.resultString)
        self.resultString = re.sub(width_pattern, f'const uint16_t {new_name}_w =', self.resultString)
        self.resultString = re.sub(height_pattern, f'const uint16_t {new_name}_h =', self.resultString)
        self.processed_image_name = new_name


    def bw_image_to_c_array(self, image):
        # Ensure image is in 'L' mode (grayscale) and convert to 1-bit
        image = image.convert('1')

        # Get image dimensions
        width, height = image.size

        # Get pixel data
        pixel_data = image.getdata()

        # Create byte array
        byte_array = []
        for y in range(height):
            for x in range(0, width, 8):
                byte = 0
                for bit in range(8):
                    if x + bit < width:
                        byte = (byte << 1) | (1 if pixel_data[y * width + x + bit] == 0 else 0)
                    else:
                        byte = (byte << 1)
                byte_array.append(byte)

        # Convert byte array to hex string
        hex_array = ','.join(f'0x{byte:02X}' for byte in byte_array)

        # Generate the C-style array string
        result = (
            f"const uint8_t {self.processed_image_name}[] PROGMEM = {{ {hex_array} }};\n"
            f"const uint16_t {self.processed_image_name}_w = {str(self.width)};\n"
            f"const uint16_t {self.processed_image_name}_h = {str(self.height)};"
        )

        # Lastly, save it
        self.resultString = result

    def grayscale_to_c_array_4_bit(self, image):
        # Ensure image is in 'L' mode (grayscale)
        image = image.convert('L')

        # Get image dimensions
        width, height = image.size

        # Get pixel data
        pixel_data = image.getdata()

        # Create byte array
        byte_array = []
        for y in range(height):
            for x in range(0, width, 2):
                byte = 0
                # Pack two 4-bit grayscale values into one byte
                for nibble in range(2):
                    if x + nibble < width:
                        grayscale_value = pixel_data[y * width + x + nibble]
                        # Convert 8-bit grayscale to 4-bit by dividing by 16
                        four_bit_value = grayscale_value // 16
                        byte = (byte << 4) | four_bit_value
                    else:
                        byte = (byte << 4)
                byte_array.append(byte)

        # Convert byte array to hex string
        hex_array = ','.join(f'0x{byte:02X}' for byte in byte_array)

        # Generate the C-style array string
        result = (
            f"const uint8_t {self.processed_image_name}[] PROGMEM = {{ {hex_array} }};\n"
            f"const uint16_t {self.processed_image_name}_w = {str(self.width)};\n"
            f"const uint16_t {self.processed_image_name}_h = {str(self.height)};"
        )

        # Lastly, save it
        self.resultString = result

    def grayscale_to_c_array_3_bit(self, image):
        # Ensure image is in 'L' mode (grayscale)
        image = image.convert('L')

        # Get image dimensions
        width, height = image.size
        self.width, self.height = width, height  # Save dimensions if needed elsewhere

        # Get pixel data as a list
        pixel_data = list(image.getdata())

        # Create byte array
        byte_array = []
        for y in range(height):
            for x in range(0, width, 2):
                byte = 0
                # Pack two 3-bit grayscale values into one byte
                for pixel_index in range(2):
                    if x + pixel_index < width:
                        grayscale_value = pixel_data[y * width + x + pixel_index]
                        # Convert 8-bit grayscale to 3-bit by dividing by 32
                        three_bit_value = grayscale_value // 32  # Values from 0 to 7
                        if pixel_index == 0:
                            # First pixel, shift left by 5 (bits 7-5)
                            byte |= (three_bit_value & 0x07) << 5
                        elif pixel_index == 1:
                            # Second pixel, shift left by 1 (bits 3-1)
                            byte |= (three_bit_value & 0x07) << 1
                        # Unused bits (bit 4 and bit 0) remain as is (zero)
                byte_array.append(byte)

        # Convert byte array to hex string
        hex_array = ','.join(f'0x{byte:02X}' for byte in byte_array)

        # Generate the C-style array string
        result = (
            f"const uint8_t {self.processed_image_name}[] PROGMEM = {{ {hex_array} }};\n"
            f"const uint16_t {self.processed_image_name}_w = {self.width};\n"
            f"const uint16_t {self.processed_image_name}_h = {self.height};"
        )

        # Save the result
        self.resultString = result