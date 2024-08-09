# This is just a test file not used in the main code, get all unique colors in an image
# Used to check the app's output

from PIL import Image

def get_unique_colors(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert image to RGB if it's not already in that mode
        img = img.convert("RGB")

        # Get the colors in the image
        colors = img.getdata()

        # Convert to a set to get unique colors
        unique_colors = set(colors)

        return unique_colors

# Example usage
image_path = 'preview.png'
unique_colors = get_unique_colors(image_path)
print(f"Number of unique colors: {len(unique_colors)}")
print(unique_colors)
