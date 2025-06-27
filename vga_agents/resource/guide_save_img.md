# Python Image Processing Tutorial: Saving Base64 and Showing Images
In this tutorial, we will learn how to save base64 image data to file using Python and perform basic image
operations such as showing image using the Pillow library.

## Prerequisites
Before we begin, make sure you have the following libraries installed in your Python environment:
- `requests`: for downloading images
- `Pillow`: for image processing
If you haven't installed these libraries yet, you can install them using pip:
```bash
pip install requests Pillow
```
## Step 1: Opening and Displaying the Image
First, we will use the `Pillow` library to open and display the image we just saved.
```
from PIL import Image
def open_and_show_image(filename):
image = Image.open(filename)
image.show()
# Example usage
open_and_show_image(filename)
```
By now, you have learned how to download images using Python and perform basic image
operations using the Pillow library. You can extend these basics to implement more complex image
processing functions as needed.