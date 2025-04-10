import logging
from typing import Dict
from google import genai

from AtlantSDK.handling.router import Router
from AtlantSDK.misc.states import StateSystem
from AtlantSDK.utils.model_parser import ModelParser
from AtlantSDK.utils.return_to import return_to


class Dispatcher:
    def __init__(self, token: str, models_path: str = "models.json"):
        self.models_path = models_path
        self.routers: Dict[str, Router] = {}
        self.logger = logging.getLogger("AtlantSDK.dispatcher")
        self.state = StateSystem()
        self.client = genai.Client(api_key=token)

    def __getattr__(self, model: str):
        return self.routers[model]


    def init_routers(self):
        """Initialization a Routers to Models"""
        parser = ModelParser()

        models = parser.get_models_from_file(self.models_path)
        for model_id in models:
            model = models[model_id]
            router = Router(model=model, dp=self, state=self.state, client=self.client)
            abs_router = self.routers.get(model_id)

            if abs_router:
                router.sync(abs_router.handlers)
            
            self.routers.update({model.name: router})


    def proccess_update(self, command: dict, to: str):
        # Uses format CMD => WHO
        if not command:
            return

        self.routers[to].handle_update(command)


    def include_routers(self, routers: list):
        for router in routers:
            self.routers.update({router.model_name: router})


    def start_polling(self, start_command: str = "START", to_model: str = "CORE", no_update=False, args: tuple = ()):
        """Method Start of polling

        Args:
            start_command (str, optional): The command that will be sent to start working with CORE model. Defaults to "START".
            to_model (str, Optional): The model which get a update
            no_update (bool, Optional): Need send update or system called by yourself?
        """
        self.init_routers()
        
        self.logger.info("Running...")

        if not no_update:
            self.proccess_update({"command": start_command, "args": ' '.join(args)}, to_model)

