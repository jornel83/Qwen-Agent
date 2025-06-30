# Python Image Processing Tutorial: Downloading Images and Performing Show Operations
In this tutorial, we will learn how to download images using Python and perform basic image
operations such as flipping and rotating using the Pillow library.
## Prerequisites
Before we begin, make sure you have the following libraries installed in your Python environment:
- `requests`: for downloading images
- `Pillow`: for image processing
If you haven't installed these libraries yet, you can install them using pip:
```bash
pip install requests Pillow
```
## Step 1: Downloading an Image
First, we need to download an image. We will use the `requests` library to accomplish this task.
```
import requests
from PIL import Image
from io import BytesIO

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Error: Failed to download image from {url}")

# Example usage
image_url = "https://example.com/image.jpg" # Replace with the URL of the image you want to download
filename = "downloaded_image.jpg"
download_image(image_url, filename)

url = 'http://10.240.243.203:31457/images/flux-1751284108.png'
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img.show()
```
## Step 2: Opening and Displaying the Image
Next, we will use the `Pillow` library to open and display the image we just downloaded.
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
