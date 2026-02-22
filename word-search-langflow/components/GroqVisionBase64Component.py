from langflow.custom import Component
from langflow.inputs import SecretStrInput, MessageTextInput, DropdownInput
from langflow.io import Output
from langflow.schema import Message
from groq import Groq

class GroqVisionBase64Component(Component):
    display_name = "Groq Vision (Base64)"
    description = "Send base64 image data to Groq's vision-capable model"
    icon = "Groq"

    inputs = [
        SecretStrInput(
            name="groq_api_key",
            display_name="Groq API Key",
            required=True,
            info="Your Groq API key from https://console.groq.com"
        ),
        MessageTextInput(
            name="base64_image",
            display_name="Base64 Image Data",
            required=True,
            info="Base64 encoded image string"
        ),
        MessageTextInput(
            name="prompt",
            display_name="Prompt",
            required=True,
            info="Instructions for the model (e.g. extract JSON grid)"
        ),
        DropdownInput(
            name="model",
            display_name="Model",
            options=[
                "meta-llama/llama-4-scout-17b-16e-instruct",
                "meta-llama/llama-4-maverick-17b-128e-instruct"
            ],
            value="meta-llama/llama-4-scout-17b-16e-instruct",
            info="Vision-capable Groq model"
        ),
        DropdownInput(
            name="image_type",
            display_name="Image Type",
            options=["image/jpeg", "image/png", "image/webp"],
            value="image/jpeg",
            info="MIME type of the image"
        )
    ]

    outputs = [
        Output(type=Message, display_name="Response", name="response", method="process_image"),
    ]

    def process_image(self) -> Message:
        try:
            # Initialize Groq client
            client = Groq(api_key=self.groq_api_key)

            # Clean base64
            base64_data = self.base64_image.strip()
            if base64_data.startswith("data:"):
                base64_data = base64_data.split(",", 1)[1]

            # Build data-url
            image_url = f"data:{self.image_type};base64,{base64_data}"

            # Prepare payload
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]

            # Call Groq API
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=self.model
            )

            # Return text result
            return Message(text=chat_completion.choices[0].message.content)

        except Exception as e:
            return Message(text=f"Error processing image with Groq: {str(e)}")