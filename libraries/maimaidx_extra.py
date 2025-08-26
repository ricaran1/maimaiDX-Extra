import json
from ..config import *
from loguru import logger

combo_to_fc = ["", "fc", "fcp", "ap", "app", "sync"]
sync_to_fs =  ["", "fs", "fsp", "fsd", "fsdp", "sync"]
level_index_to_label = ["Basic", "Advanced", "Expert", "Master", "Re:MASTER"]
score_rank_to_rate = [
    "d", "c", "b", "bb", "bbb", "a", "aa", "aaa", "s",
    "sp", "ss", "ssp", "sss", "sssp",
]

with open(f"{music_extra_file}", "r", encoding="utf-8") as music_file:
    music_data = json.load(music_file)

##ap50的数据处理
async def ap50(user_data):
    if not isinstance(user_data, dict):
        user_data = user_data.dict()
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
    if not isinstance(user_data, dict):
        user_data = user_data.dict()
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
    if not isinstance(user_data, dict):
        user_data = user_data.dict()
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
            song_id = str(record["song_id"])
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

def load_json(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def load_music_data(nhcode: int = 0):
    if nhcode == 1:
        return load_json(nh_mai_music_file)
    return load_json(music_extra_file)

def cal_ra(achievements, ds):
    coefficient = 0.0
    if achievements >= 100.5:
        achievements = 100.5
        coefficient = 22.4
    elif achievements >= 100:
        coefficient = 21.6
    elif achievements >= 99.5:
        coefficient = 21.1
    elif achievements >= 99:
        coefficient = 20.8
    elif achievements >= 98:
        coefficient = 20.3
    elif achievements >= 97:
        coefficient = 20.0
    elif achievements >= 94:
        coefficient = 16.8
    elif achievements >= 90:
        coefficient = 15.2
    elif achievements >= 80:
        coefficient = 13.6
    elif achievements >= 75:
        coefficient = 12.0
    elif achievements >= 70:
        coefficient = 11.2
    elif achievements >= 60:
        coefficient = 9.6
    elif achievements >= 50:
        coefficient = 8.0
    elif achievements >= 40:
        coefficient = 6.4
    elif achievements >= 30:
        coefficient = 4.8
    elif achievements >= 20:
        coefficient = 3.2
    elif achievements >= 10:
        coefficient = 1.6
    return int(achievements / 100.0 * ds * coefficient)

def music_data_to_records(data, countscode=0, nhcode=0):
    user_music_data = json.loads(data)
    mai_music_data = load_music_data(nhcode)
    records = []

    for user_music in user_music_data:
        song_id = user_music.get("musicId")
        level_index = user_music.get("level")

        if song_id is None or level_index is None:
            continue

        mai_music = mai_music_data.get(str(song_id))
        if not mai_music:
            continue

        achievements = user_music["achievement"] / 10000.0
        if "ds" not in mai_music or not isinstance(mai_music["ds"], list):
            continue
        if level_index >= len(mai_music["ds"]):
            continue

        ds = mai_music["ds"][level_index]
        ra = cal_ra(achievements, ds)

        record = {
            "achievements": achievements,
            "ds": ds,
            "dxScore": user_music["deluxscoreMax"],
            "fc": combo_to_fc[user_music["comboStatus"]],
            "fs": sync_to_fs[user_music["syncStatus"]],
            "level": mai_music["level"][level_index],
            "level_index": level_index,
            "level_label": level_index_to_label[level_index],
            "ra": ra,
            "rate": score_rank_to_rate[user_music["scoreRank"]],
            "song_id": song_id,
            "title": mai_music["title"],
            "type": mai_music["type"],
        }

        # pc50 额外加 playCount
        if countscode == 1:
            record["playCount"] = user_music.get("playCount")

        records.append(record)

    return records

# 转 b50 数据
def data_to_b50data(user_id, nickname, nhcode=0):
    music_data2 = ...  # 这里传入来自服务器的所有乐曲成绩
    music_data1 = json.dumps(music_data2)

    df_data = music_data_to_records(music_data1, nhcode=nhcode)

    sd_song_ids = {song["id"] for song in music_data if song["category"].lower() == "sd"}
    dx_song_ids = {song["id"] for song in music_data if song["category"].lower() == "dx"}

    sd_songs = [song for song in df_data if str(song["song_id"]) in sd_song_ids]
    dx_songs = [song for song in df_data if str(song["song_id"]) in dx_song_ids]

    sd_songs.sort(key=lambda x: x["ra"], reverse=True)
    dx_songs.sort(key=lambda x: x["ra"], reverse=True)

    selected_sd = sd_songs[:35]
    selected_dx = dx_songs[:15]

    result = {
        "additional_rating": 1,
        "charts": {"dx": selected_dx, "sd": selected_sd},
        "nickname": nickname,
        "plate": "",
        "rating": sum(song["ra"] for song in selected_sd + selected_dx),
        "user_general_data": None,
        "username": "测试"
    }
    return result

# 转 pc50 数据
def data_to_pc50data(user_id, nickname):
    music_data2 = ...  # 这里传入来自服务器的所有乐曲成绩
    music_data1 = json.dumps(music_data2)

    df_data = music_data_to_records(music_data1, countscode=1)

    sd_song_ids = {song["id"] for song in music_data if song["category"].lower() == "sd"}
    dx_song_ids = {song["id"] for song in music_data if song["category"].lower() == "dx"}

    sd_songs = [song for song in df_data if str(song["song_id"]) in sd_song_ids]
    dx_songs = [song for song in df_data if str(song["song_id"]) in dx_song_ids]

    sd_songs.sort(key=lambda x: (x["playCount"], x["ra"]), reverse=True)
    dx_songs.sort(key=lambda x: (x["playCount"], x["ra"]), reverse=True)

    selected_sd = sd_songs[:35]
    selected_dx = dx_songs[:15]

    result = {
        "additional_rating": 1,
        "charts": {"dx": selected_dx, "sd": selected_sd},
        "nickname": nickname,
        "plate": "",
        "rating": sum(song["ra"] for song in selected_sd + selected_dx),
        "user_general_data": None,
        "username": "测试"
    }
    return result
