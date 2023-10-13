from ZZU_API.core import ZZU_Class_Room
from src.utils import parse_data_by_periods, utc_time_string, write_data_into_json

JSON_PATH = "./page/data.json"

PERIODS = [
    [1, 2],
    [3, 4],
    [5, 6],
    [7, 8],
    [9, 10],
    [1, 2, 3, 4],
    [5, 6, 7, 8],
]

BUILDING_ID_LIST = [5, 6, 7, 8, 9]  # 北1到北5

building = ZZU_Class_Room()

# fmt: off
def process_data():
    result = {}
    for i in BUILDING_ID_LIST:
        temp_result = {}
        data = building.get_room_data_by_building_id(building_id=i)[0]
        rooms = data.get("rooms")
        for target in PERIODS:
            temp_result[f"time_split_{PERIODS.index(target)+1}"] = parse_data_by_periods(rooms, target)
        result[f"building_{i}"] = temp_result
    return result
# fmt: on

def main():
    data = {"last_update_time": utc_time_string(), "data": process_data()}
    write_data_into_json(data=data, json_path=JSON_PATH)

if __name__ == "__main__":
    main()
