from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot,Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
import re
from ..libraries.image import text_to_bytes_io
from ..libraries.maimaidx_music_info import *
from ..libraries.maimaidx_player_score import *
from ..libraries.maimaidx_update_plate import *
from ..libraries.maimaidx_extra import data_to_b50data,data_to_pc50data

def get_at_qq(message: Message) -> Optional[int]:
    for item in message:
        if isinstance(item, MessageSegment) and item.type == 'at' and item.data['qq'] != 'all':
            return int(item.data['qq'])
        
pc50  = on_command('pc50', aliases={'Pc50','pc58','Pc58','PC50'}, priority=5)
nh50  = on_command('拟合50', aliases={'拟合b50','拟合b58','拟合B50','拟合B58'}, priority=5)

@pc50.handle()
async def _(bot: Bot,event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()):
    group_id = event.group_id if hasattr(event, 'group_id') else 0
    qqid = get_at_qq(arg) or event.user_id
    username = arg.extract_plain_text().split()
    if group_id!=0:
        match = re.search(r"card='([^']*)'", str(event.sender))
        nickname=match.group(1)
    else:
        nickname=(await bot.get_stranger_info(user_id=qqid)).get("nick")
    if _q := get_at_qq(arg):
        qqid = _q
    user_id = 1 #请自行传入userid
    userdata= data_to_pc50data(user_id,nickname)
    await matcher.finish(await generate_pc50(userdata,qqid, username), reply_message=True)

@nh50.handle()
async def _(bot: Bot,event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()):
    group_id = event.group_id if hasattr(event, 'group_id') else 0
    qqid = get_at_qq(arg) or event.user_id
    username = arg.extract_plain_text().split()
    if group_id!=0:
        match = re.search(r"card='([^']*)'", str(event.sender))
        nickname=match.group(1)
    else:
        nickname=(await bot.get_stranger_info(user_id=qqid)).get("nick")
    if _q := get_at_qq(arg):
        qqid = _q
    user_id = 1 #请自行传入userid
    userdata=data_to_b50data(user_id,nickname,nhcode=1)
    await matcher.finish(await generate_other50(userdata,qqid, username), reply_message=True)