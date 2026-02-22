from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Data, Message
import requests
import base64
import os

class ImageURLToBase64(Component):
    display_name = "Image URL to Base64"
    description = "Fetches an image from a URL and converts it to base64 format"
    icon = "image"

    inputs = [
        MessageTextInput(
            name="image_url",
            display_name="Image URL",
            info="URL or local file path of the image (PNG, JPG, etc.)",
            required=True,
        ),
    ]

    outputs = [
        Output(display_name="Base64 Message", name="base64_message", method="get_base64_message")
    ]

    def convert_image(self) -> Data:
        try:
            image_url = self.image_url

            # If URL
            if image_url.startswith("http"):
                headers = {"User-Agent": "Mozilla/5.0"}  # Avoid 403 errors
                response = requests.get(image_url, headers=headers)
                response.raise_for_status()
                image_data = response.content
                content_type = response.headers.get("Content-Type", "image/jpeg")
            # If local file
            else:
                if not os.path.exists(image_url):
                    raise FileNotFoundError(image_url)
                with open(image_url, "rb") as f:
                    image_data = f.read()
                content_type = "image/jpeg"

            # Convert to base64
            base64_string = base64.b64encode(image_data).decode('utf-8')

            # Create data object
            result = Data(
                data={
                    "base64": base64_string,
                    "content_type": content_type,
                    "data_url": f"data:{content_type};base64,{base64_string}"
                }
            )

            self.status = f"Successfully converted image from {image_url}"
            return result

        except Exception as e:
            self.status = f"Error: {str(e)}"
            raise Exception(f"Failed to convert image: {str(e)}")

    def get_base64_message(self) -> Message:
        result = self.convert_image()
        base64_str = result.data.get("base64", "")
        return Message(text=base64_str)