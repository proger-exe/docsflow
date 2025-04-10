import logging
import inspect

from AtlantSDK.misc.states import StateSystem
from AtlantSDK.type.conversation import Conversation
from AtlantSDK.type.model import Model
from AtlantSDK.misc.filter import check_handlers
from AtlantSDK.utils.make_update import make_an_update


class Router:
    def __init__(self, model: Model, dp, state: StateSystem, client) -> None:
        """A Routing of model-chat class.

        Args:
            model (atlant.types.Model): The model to which the router will be bound

        """
        self.model: Model = model
        self.model.set_client(client)
        if self.model.can_tune and self.model.tune_data:
            self.model.tune_model()

        self.chat: Conversation = model.init_conversation()
        self.logger = logging.getLogger(f"AtlantSDK.router.{model.name}")
        self.handlers = {}
        self.dp = dp
        self.state = state


    def send_command(self, text: str):
        self.logger.info(f"TO\t=>\t{text}")
        answer = self.chat.send_command(
            text
        )

        self.logger.info(f"FROM\t=>\t{answer}")

        return answer

    def register_a_handler(self, function):
        def wrapper(*args, **kwargs):

            sig = inspect.signature(function)
            bound_args = sig.bind_partial()

            for param_name in sig.parameters:
                if param_name == "chat":
                    bound_args.arguments[param_name] = self.chat
                elif param_name == "model":
                    bound_args.arguments[param_name] = self.model
                elif param_name == "state":
                    bound_args.arguments[param_name] = self.state

            for kw in kwargs:
                print(kw)
                bound_args.arguments[kw] = kwargs[kw]
            
            state = self.state.get_state()
            res = function(*bound_args.args, **bound_args.kwargs)

            self.dp.proccess_update(*make_an_update(res, state))

        return wrapper



    def handle_update(self, command: dict):
        self.logger.info(f"TO => {command}")

        for handler in self.handlers:
            correct = check_handlers(dict(handler), command)
            if correct:
                func = self.handlers.get(handler)

                if func:
                    cmd = command["command"]
                    cmd_args = command.get("args")
                    cmd = f"{cmd} {cmd_args}" if cmd_args else cmd
                    func(cmd=cmd)


    def sync(self, handlers: dict):
        for handler in handlers:
            self.handlers[handler] = self.register_a_handler(handlers[handler])


class AbstactRouter:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.handlers = {}

    def handler(self, **filters):
        def register_a_handler(func):
            
            params = tuple(filters.items())
            self.handlers.update({params: func})

            def wrapper(*args, **kwargs):
                return func

            return wrapper
        return register_a_handler
