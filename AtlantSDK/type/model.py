import os 

from google.genai import Client, types
from AtlantSDK.errors.model import ErrorInitializationModel
from AtlantSDK.type.conversation import Conversation
from AtlantSDK.type.generation_config import DefaultModelConfigurationSettings, ModelConfigurationSettings


class Model:
    "Class of neural network model operation"

    def __init__(self, settings: dict):
        """Model Initialization Function

        Args:
            settings (dict): Generation parameters and framework configuration 
            upload_from_file (bool): Parameter determining whether a system instruction should be loaded from AtlantSDK.a file or whether the given parameter is already an instruction
        """
        self.name = settings.get("Name", "")
        self.system_instruction = settings.get("SystemInstruction", str())
        self.priority = settings.get("Priority")
        self.model = settings.get("Model", "gemini-2.0-flash")
        self.base_tune_model = settings.get("TuneModel", "models/gemini-1.5-flash-001-tuning")
        upload_from_file = settings.get("FromFile", True)
        self.can_tune = settings.get("CanTune", False)
        self.tune_data = settings.get("TuneData", [])
        self.tuned = False 

        # A generation subparameters
        generation_settings = settings.get("Generation", DefaultModelConfigurationSettings.generation_config)
        self.generation_setting = ModelConfigurationSettings(**generation_settings)
        

        if not self.name or not self.system_instruction:
            raise ErrorInitializationModel("Model.name or Model.system_instruction was not specified in the model configuration.")

        # Framework settings
        if upload_from_file:
            self.system_instruction = self._read_description_from_file(self.system_instruction)

        # Add API usage variables

    def set_client(self, client: Client):
        self.client = client

    def init_conversation(self):
        self.chat = Conversation(self, self.client)
        return self.chat


    def _read_description_from_file(self, path: str):
        """Read description from model.file method

        Args:
            path (str): A path to file

        Raises:
            ErrorInitializationModel: if there is not file

        Returns:
            str: Return a content of file
        """
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, "r+", encoding="utf-8") as description:
                return description.read()
        else:
            raise ErrorInitializationModel("The Model.system_instruction path does not exist (maybe you forgot to turn off upload_from_file?)")

    def tune_model(self):
        self.tuned = True
        
        training_dataset=types.TuningDataset(
            examples=[
                types.TuningExample(
                    text_input=i,
                    output=o,
                )
                for i,o in self.tune_data
            ],
        )

        tuning = self.client.tunings.tune(
            base_model=self.base_tune_model,  # type: ignore
            training_dataset=training_dataset,
            config=types.CreateTuningJobConfig(
                epoch_count= 5,
                batch_size=4,
                learning_rate=0.001,
                tuned_model_display_name=f"{self.model}_TUNED"
            )
        )
        
        self.model = tuning.tuned_model.model