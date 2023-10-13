from datetime import datetime, timezone, timedelta, UTC
from base64 import b64encode, b64decode
from nacl import encoding, public
from .logger import logger
import requests
import json

# fmt: off
def utc_plus_8() -> datetime:
    return datetime.now(UTC).astimezone(timezone(timedelta(hours=8)))
# fmt: on


def timestamp_13_digit() -> int:
    return int(datetime.timestamp(datetime.now()) * 1000)


def get_today_date_str():
    return datetime.strftime(utc_plus_8(), "%Y-%m-%d")


def decode_str_with_base64(string: str) -> str:
    return b64decode(string.encode("utf-8")).decode("utf-8")


def decode_to_json(string: str):
    return json.loads(decode_str_with_base64(string))


def find_available_classroom(data, floor: str, periods: list[int]):
    """
    `data`: Classroom data\n
    `floor`: target floor\n
    `periods`: target periods, scale from 1~10, such as [1,2,5,6]
    """
    available_classrooms = []
    for classroom in data:
        if int(classroom["floor"]) == int(floor):
            # Check if target period is available, 0 for available, 1 for occupied.
            occupy_units = classroom["occupy_units"]
            is_available = True
            for period in periods:
                if occupy_units[period - 1] == "1":
                    is_available = False
                    break
            if is_available:
                available_classrooms.append(classroom["room_name"])

    return available_classrooms


def encrypt(public_key, secret_value) -> str:
    """
    Encrypt a Unicode string using the public key.

    :param public_key: The public key to use for encryption.
    :param secret_value: The secret value to encrypt.
    :return: The encrypted secret value.
    """
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder)
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def get_pub_key(repos: str, token: str) -> tuple[str, int]:
    url = "https://api.github.com/repos/{}/actions/secrets/public-key".format(repos)
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer {}".format(token),
        "X-GitHub-Api-Version": "2022-11-28",
    }

    r = requests.get(url, headers=headers)
    return r.json()["key"], r.json()["key_id"]


def update_secret(name: str, value: str, repo: str, token: str):
    """
    更新 secret

    :param name: secret 名称
    :param value: secret 值
    :param repo: GITHUB_REPOSITORY 环境变量的值
    :param token: GitHub Personal Access Token with repo permission
    """
    if not token:
        logger.warning("未配置 GitHub Personal Access Token, 更新 refresh_tokens 失败")
        return
    key, key_id = get_pub_key(repo, token)
    url = f"https://api.github.com/repos/{repo}/actions/secrets/{name}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    payload = {"encrypted_value": encrypt(key, value), "key_id": key_id}
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code == 204:
        logger.info(f"Secret {name} 更新成功")
    else:
        logger.error(f"Secret {name} 更新失败，错误信息：{response.content}")
