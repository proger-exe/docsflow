import json
from AtlantSDK.type.model import Model
from AtlantSDK.errors.model import PriorityModelError


class ModelParser:
    def __init__(self):
        self.models = {}

    def get_models_from_file(self, file_path: str) -> dict[str, Model]:
        """Model parser from *.json file

        Args:
            file_path (str): path to *.json file

        Raises:
            PriorityModelError: if more than 1 model with priority 0

        Returns:
            dict[str, Model]: a dict with models and CORE-model.
        """        
        with open(file_path, encoding="utf-8") as raw_models_data_content:
            raw_models_data = raw_models_data_content.read()

        models_data = json.loads(raw_models_data)
        start_model = ""

        for model_data in models_data:
            if model_data.get("Priority", -1) == 0:
                if start_model:
                    raise PriorityModelError(f"The {model_data['Name']} model with priority 0 conflicts with {start_model}, maybe you forgot to change the priority? ")

                model_object = Model(model_data)
                self.models.update({"CORE": model_object, model_data["Name"]: model_object})
                continue

            model_object = Model(model_data)
            self.models.update({model_data["Name"]: model_object})

        return self.models