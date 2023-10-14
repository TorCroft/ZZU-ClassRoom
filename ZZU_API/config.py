import json, os
from .utils import update_secret

CONFIG_TEMPLATE = {
    "Account": "",
    "Password": "",
    "UserToken": "",
    "Token": "",
    "JsessionId": "",
    "Tid": "",
    "RefreshToken": "",
    "ECardAccessToken": "",
}

# fmt: off
class Config:
    def __init__(self) -> None:
        if "ZZU_CONFIG" in os.environ:
            data: dict = json.loads(os.environ["ZZU_CONFIG"])
        else:
            self.path = "config.json"
            data = None
            if not os.path.exists(self.path):
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(CONFIG_TEMPLATE, f, ensure_ascii=False)
        self.load_config(data)

    def load_config(self, data=None):
        if data is None:
            with open(self.path, "r", encoding="utf-8") as f:
                data: dict = json.load(f)
        for k, v in data.items():
            self.__dict__[k] = v

    def save_config(self, **kwargs):
        data = {}
        for key in CONFIG_TEMPLATE:
            data[key] = self.__dict__[key]
        data.update(**kwargs)
        if "ZZU_CONFIG" in os.environ:
            update_secret(secret_name="ZZU_CONFIG", value=json.dumps(data), owner=os.environ["GH_USERNAME"], repo="ZZU-ClassRoom", token=os.environ["GH_ACCESS_TOKEN"])
        else:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f)
# fmt: on

config = Config()
