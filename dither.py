import cv2
import numpy as np
class ditherModule(object):
    def dither(self, img, method=1, resize = False):
        if(resize):
            img = cv2.resize(img, (int(0.5*(np.shape(img)[1])), int(0.5*(np.shape(img)[0]))))

        # Simple2D
        if(method == 3):
            img = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
            rows, cols = np.shape(img)
            out = cv2.normalize(img.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
            for i in range(1, rows-1):
                for j in range(1, cols-1):
                    # threshold step
                    if(out[i][j] > 0.5):
                        err = out[i][j] - 1
                        out[i][j] = 1
                    else:
                        err = out[i][j]
                        out[i][j] = 0

                    # error diffusion step
                    out[i][j + 1] = out[i][j + 1] + (0.5 * err)
                    out[i + 1][j] = out[i + 1][j] + (0.5 * err)

            return(out[1:rows-1, 1:cols-1])

        # Floyd-steinberg
        elif(method == 1):
            img = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
            rows, cols = np.shape(img)
            out = cv2.normalize(img.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
            for i in range(1, rows - 1):
                for j in range(1, cols - 1):
                    # threshold step
                    if (out[i][j] > 0.5):
                        err = out[i][j] - 1
                        out[i][j] = 1
                    else:
                        err = out[i][j]
                        out[i][j] = 0

                    # error diffusion step
                    out[i][j + 1] = out[i][j + 1] + ((7/16) * err)
                    out[i + 1][j - 1] = out[i + 1][j - 1] + ((3/16) * err)
                    out[i + 1][j] = out[i + 1][j] + ((5/16) * err)
                    out[i + 1][j + 1] = out[i + 1][j + 1] + ((1/16) * err)

            return (out[1:rows - 1, 1:cols - 1])

        # Jarvis
        elif (method == 2):
            img = cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_REPLICATE)
            rows, cols = np.shape(img)
            out = cv2.normalize(img.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
            for i in range(2, rows - 2):
                for j in range(2, cols - 2):
                    # threshold step
                    if (out[i][j] > 0.5):
                        err = out[i][j] - 1
                        out[i][j] = 1
                    else:
                        err = out[i][j]
                        out[i][j] = 0

                    # error diffusion step
                    out[i][j + 1] = out[i][j + 1] + ((7 / 48) * err)
                    out[i][j + 2] = out[i][j + 2] + ((5 / 48) * err)

                    out[i + 1][j - 2] = out[i + 1][j - 2] + ((3 / 48) * err)
                    out[i + 1][j - 1] = out[i + 1][j - 1] + ((5 / 48) * err)
                    out[i + 1][j] = out[i + 1][j] + ((7 / 48) * err)
                    out[i + 1][j + 1] = out[i + 1][j + 1] + ((5 / 48) * err)
                    out[i + 1][j + 2] = out[i + 1][j + 2] + ((3 / 48) * err)

                    out[i + 2][j - 2] = out[i + 2][j - 2] + ((1 / 48) * err)
                    out[i + 2][j - 1] = out[i + 2][j - 1] + ((3 / 48) * err)
                    out[i + 2][j] = out[i + 2][j] + ((5 / 48) * err)
                    out[i + 2][j + 1] = out[i + 2][j + 1] + ((3 / 48) * err)
                    out[i + 2][j + 2] = out[i + 2][j + 2] + ((1 / 48) * err)

            return (out[2:rows - 2, 2:cols - 2])

        else:
            raise TypeError('specified method does not exist. available methods = "simple2D", "floyd-steinberg(default)", "jarvis-judice-ninke"')

class ditherModule4bit(object):
    def dither(self, img, method=1, resize = False):
        if(resize):
            img = cv2.resize(img, (int(0.5*(np.shape(img)[1])), int(0.5*(np.shape(img)[0]))))

        if method == 3:
            img = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
            rows, cols = np.shape(img)
            out = cv2.normalize(img.astype('float'), None, 0.0, 15.0, cv2.NORM_MINMAX)  # Normalize to 0-15 range
            for i in range(1, rows - 1):
                for j in range(1, cols - 1):
                    # Quantize to 4-bit (16 levels)
                    old_pixel = out[i][j]
                    new_pixel = round(old_pixel)
                    out[i][j] = new_pixel
                    quant_error = old_pixel - new_pixel

                    # Distribute the quantization error to neighboring pixels
                    out[i][j + 1] = out[i][j + 1] + (7 / 16.0 * quant_error)
                    out[i + 1][j - 1] = out[i + 1][j - 1] + (3 / 16.0 * quant_error)
                    out[i + 1][j] = out[i + 1][j] + (5 / 16.0 * quant_error)
                    out[i + 1][j + 1] = out[i + 1][j + 1] + (1 / 16.0 * quant_error)

            out = np.clip(out, 0, 15)  # Ensure values are within the 4-bit range
            out = (out * 16).astype(np.uint8)  # Convert back to 8-bit range (0-255)
            return out[1:rows - 1, 1:cols - 1]

class ditherModule3bit(object):
    def dither(self, img, method=1, resize=False):
        if resize:
            img = cv2.resize(img, (int(0.5 * img.shape[1]), int(0.5 * img.shape[0])))

        if method == 3:
            # Add a border to handle edge cases during error diffusion
            img = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
            rows, cols = img.shape
            # Normalize pixel values to the 0-7 range (3 bits)
            out = cv2.normalize(img.astype('float'), None, 0.0, 7.0, cv2.NORM_MINMAX)
            for i in range(1, rows - 1):
                for j in range(1, cols - 1):
                    # Quantize to 3-bit (8 levels)
                    old_pixel = out[i][j]
                    new_pixel = round(old_pixel)
                    out[i][j] = new_pixel
                    quant_error = old_pixel - new_pixel

                    # Distribute the quantization error to neighboring pixels
                    out[i][j + 1] += (7 / 16.0) * quant_error
                    out[i + 1][j - 1] += (3 / 16.0) * quant_error
                    out[i + 1][j] += (5 / 16.0) * quant_error
                    out[i + 1][j + 1] += (1 / 16.0) * quant_error

            # Clip the values to ensure they are within the 0-7 range
            out = np.clip(out, 0, 7)
            # Scale back to the 0-255 range for display or saving
            out = (out * 32).astype(np.uint8)  # 32 = 256 / 8 levels
            # Remove the border before returning the image
            return out[1:rows - 1, 1:cols - 1]

def dither(img, method='floyd-steinberg', resize = False):
    dither_object = ditherModule()
    out = dither_object.dither(img, method, resize)
    return(out)

def dither4bit(img, method='floyd-steinberg', resize = False):
    dither_object = ditherModule4bit()
    out = dither_object.dither(img, 3, resize)
    return(out)