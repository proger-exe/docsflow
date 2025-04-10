from AtlantSDK import Dispatcher, AbstactRouter, Conversation
from AtlantSDK.utils.return_to import return_to
from app.core.config import config
from app.api.deps import buffer
import json


router = AbstactRouter("CORE")


@router.handler(command="START")
def analyze_data(cmd: str):
    return return_to("UPLOAD", cmd.replace("START", ""), to_model="CORE")


@router.handler(command="UPLOAD")
def upload_and_analyze_data(cmd: str, chat: Conversation):
    data = cmd.split(" ")
    filename = data[1]
    task_id = data[2]

    print(filename)
    res = chat.send_file(file=filename, message="make this")

    buffer.update({task_id: res})
    return return_to("EXIT", to_model="CORE")  # it's not defined command, we need to exit.


dp = Dispatcher(config.backend.GEMINI_API_TOKEN, "app/models/models.json")
dp.include_routers([router])
dp.start_polling(no_update=True)