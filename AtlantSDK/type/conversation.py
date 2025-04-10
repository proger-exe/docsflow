from google import genai
from AtlantSDK.utils.clear_md import clean_text
from google.genai.chats import Chat
from google.genai import types


class Conversation:
    def __init__(self, model, client: genai.Client):
        self.model = model
        self.history = {}
        self.client = client
        self.chat = self._get_chat()

    def _get_chat(self) -> Chat:
        """
        Get chat method

        Returns:
            genai.Chat
        """
        generate_content_config = types.GenerateContentConfig(
            temperature=self.model.generation_setting.temperature,
            top_p=self.model.generation_setting.top_p,
            top_k=self.model.generation_setting.top_k,
            max_output_tokens=self.model.generation_setting.max_output_tokens,
            system_instruction=[
                types.Part.from_text(
                    text=self.model.system_instruction
                ),
            ],
        )
        return self.client.chats.create(
            model=self.model.model,
            config=generate_content_config 
        )

    def send_command(self, command: str):
        result = self.chat.send_message(
            command
        )
        if not result:
            self.send_command(command)

        res = clean_text(result.text).strip()  # type: ignore
        return res

    def send_file(self, file, message: str):

        a_file = self.client.files.upload(file=file),


        generate_content_config = types.GenerateContentConfig(
            temperature=self.model.generation_setting.temperature,
            top_p=self.model.generation_setting.top_p,
            top_k=self.model.generation_setting.top_k,
            max_output_tokens=self.model.generation_setting.max_output_tokens,
            system_instruction=[
                types.Part.from_text(
                    text=self.model.system_instruction
                ),
            ],
        )   

        return self.client.models.generate_content(
            model=self.model.model,
            contents=[message, a_file],
            config=generate_content_config,
        ).text