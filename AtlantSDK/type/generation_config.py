from dataclasses import dataclass


class DefaultModelConfigurationSettings:
    "Standard model generation configuration"
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }


@dataclass
class ModelConfigurationSettings:
    "Model generation configuration"
    default = DefaultModelConfigurationSettings.generation_config

    temperature: int = default["temperature"]
    top_p: float = default["top_p"]
    top_k: int = default["top_k"]
    max_output_tokens: int = default["max_output_tokens"]
    response_mime_type: str = default["response_mime_type"]

