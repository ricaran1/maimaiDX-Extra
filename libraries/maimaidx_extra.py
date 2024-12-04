import json
from ..config import *

with open(f"{music_extra_file}", "r", encoding="utf-8") as music_file:
    music_data = json.load(music_file)

##ap50的数据处理
async def ap50(user_data):
    music_category_map = {item["id"]: item["category"] for item in music_data}
    result = {
        "additional_rating": user_data.get("additional_rating", 0),
        "charts": {
            "dx": [],
            "sd": []
        },
        "nickname": user_data.get("nickname", ""),
        "plate": user_data.get("plate", ""),
        "rating": 0,
        "user_general_data": None,
        "username": user_data.get("username", "")
    }

    sd_records = []
    dx_records = []

    for record in user_data.get("records", []):
        song_id = str(record["song_id"])
        category = music_category_map.get(song_id)
        if category == "sd" and record["fc"] in ("ap", "app"):
            sd_records.append(record)
        elif category == "dx" and record["fc"] in ("ap", "app"):
            dx_records.append(record)
    top_sd_records = sorted(sd_records, key=lambda x: x["ra"], reverse=True)[:35]
    top_dx_records = sorted(dx_records, key=lambda x: x["ra"], reverse=True)[:15]
    result["charts"]["sd"].extend(top_sd_records)
    result["charts"]["dx"].extend(top_dx_records)
    combined_records = top_sd_records + top_dx_records
    result["rating"] = sum(record["ra"] for record in combined_records)

    return result

##fc50的数据处理
async def fc50(user_data):
    music_category_map = {item["id"]: item["category"] for item in music_data}
    result = {
        "additional_rating": user_data.get("additional_rating", 0),
        "charts": {
            "dx": [],
            "sd": []
        },
        "nickname": user_data.get("nickname", ""),
        "plate": user_data.get("plate", ""),
        "rating": 0,
        "user_general_data": None,
        "username": user_data.get("username", "")
    }

    sd_records = []
    dx_records = []

    for record in user_data.get("records", []):
        song_id = str(record["song_id"])
        category = music_category_map.get(song_id)
        if category == "sd" and record["fc"] in ("fc", "fcp"):
            sd_records.append(record)
        elif category == "dx" and record["fc"] in ("fc", "fcp"):
            dx_records.append(record)
    top_sd_records = sorted(sd_records, key=lambda x: x["ra"], reverse=True)[:35]
    top_dx_records = sorted(dx_records, key=lambda x: x["ra"], reverse=True)[:15]
    result["charts"]["sd"].extend(top_sd_records)
    result["charts"]["dx"].extend(top_dx_records)
    combined_records = top_sd_records + top_dx_records
    result["rating"] = sum(record["ra"] for record in combined_records)

    return result


##锁/寸50的数据处理
#type=1锁50，#type=2寸50
#music=0不区分鸟/鸟+,取分值最高的前50。music=1为鸟,music=2为鸟+
async def sc50(user_data,type,music=0):
    music_category_map = {item["id"]: item["category"] for item in music_data}
    result = {
        "additional_rating": user_data.get("additional_rating", 0),
        "charts": {
            "dx": [],
            "sd": []
        },
        "nickname": user_data.get("nickname", ""),
        "plate": user_data.get("plate", ""),
        "rating": 0,
        "user_general_data": None,
        "username": user_data.get("username", "")
    }

    sd_records = []
    dx_records = []
    achievement_conditions = {
        (1, 0): lambda a: (100.0000 <= a <= 100.0500) or (100.5000 <= a <= 100.5500),
        (1, 1): lambda a: 100.0000 <= a <= 100.0500,
        (1, 2): lambda a: 100.5000 <= a <= 100.5500,
        (2, 0): lambda a: (99.9000 <= a < 100.0000) or (100.4000 <= a < 100.5000),
        (2, 1): lambda a: 99.9000 <= a < 100.0000,
        (2, 2): lambda a: 100.4000 <= a < 100.5000,
    }
    condition = achievement_conditions.get((type, music))
    if condition:
        for record in user_data.get("records", []):
            song_id = str(record["song_id"])  # 确保与 music_data 中的 id 一致
            category = music_category_map.get(song_id)
            achievements = record["achievements"]
            if category == "sd" and condition(achievements):
                sd_records.append(record)
            elif category == "dx" and condition(achievements):
                dx_records.append(record)
    top_sd_records = sorted(sd_records, key=lambda x: x["ra"], reverse=True)[:35]
    top_dx_records = sorted(dx_records, key=lambda x: x["ra"], reverse=True)[:15]
    result["charts"]["sd"].extend(top_sd_records)
    result["charts"]["dx"].extend(top_dx_records)
    combined_records = top_sd_records + top_dx_records
    result["rating"] = sum(record["ra"] for record in combined_records)

    return result
