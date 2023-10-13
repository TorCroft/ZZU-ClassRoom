from ZZU_API.utils import find_available_classroom
import json
from datetime import datetime, UTC


def utc_time_string():
    utc_time = datetime.now(UTC)
    return datetime.strftime(utc_time, "%Y-%m-%d %H:%M:%S %Z")


def write_data_into_json(data, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


# fmt: off
def parse_data_by_periods(room_data, target_periods):
    total_floor = int(room_data[-1]["floor"])
    result = []
    for floor in range(1, total_floor + 1):
        EmptyRooms = find_available_classroom(room_data, floor, target_periods)
        if EmptyRooms:
            temp = {"floor": floor, "EmptyRooms": EmptyRooms}
            result.append(temp)
    result.reverse()
    return result
# fmt: on

