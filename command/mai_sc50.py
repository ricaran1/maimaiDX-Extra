from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

from ..libraries.image import to_bytes_io
from ..libraries.maimaidx_music_info import *
from ..libraries.maimaidx_player_score import *
from ..libraries.maimaidx_update_plate import *
from ..libraries.maimaidx_extra import sc50
def get_at_qq(message: Message) -> Optional[int]:
    for item in message:
        if isinstance(item, MessageSegment) and item.type == 'at' and item.data['qq'] != 'all':
            return int(item.data['qq'])
        
suo50     = on_command('锁50', aliases={}, priority=5)
sss_suo50 = on_command('鸟锁50', aliases={'sss锁50','SSS锁50'}, priority=5)
sssp_suo50= on_command('鸟+锁50', aliases={'sss+锁50','SSS+锁50'}, priority=5)
cun50     = on_command('寸50', aliases={}, priority=5)
sss_cun50 = on_command('鸟寸50', aliases={'sss寸50','SSS+寸50'}, priority=5)
sssp_cun50= on_command('鸟+寸50', aliases={'sss+寸50','SSS+寸50'}, priority=5)

@suo50.handle()
async def _(event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()):
    qqid = get_at_qq(arg) or event.user_id
    username = arg.extract_plain_text().split()
    if _q := get_at_qq(arg):
        qqid = _q
    obj = await maiApi.query_user_dev(qqid=qqid, username=username)
    userdata=await sc50(obj,type=1,music=0)
    await matcher.finish(await generate_other50(userdata,qqid, username), reply_message=True)

@sss_suo50.handle()
async def _(event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()):
    qqid = get_at_qq(arg) or event.user_id
    username = arg.extract_plain_text().split()
    if _q := get_at_qq(arg):
        qqid = _q
    obj = await maiApi.query_user_dev(qqid=qqid, username=username)
    userdata=await sc50(obj,type=1,music=1)
    await matcher.finish(await generate_other50(userdata,qqid, username), reply_message=True)

@sssp_suo50.handle()
async def _(event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()):
    qqid = get_at_qq(arg) or event.user_id
    username = arg.extract_plain_text().split()
    if _q := get_at_qq(arg):
        qqid = _q
    obj = await maiApi.query_user_dev(qqid=qqid, username=username)
    userdata=await sc50(obj,type=1,music=2)
    await matcher.finish(await generate_other50(userdata,qqid, username), reply_message=True)

@cun50.handle()
async def _(event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()):
    qqid = get_at_qq(arg) or event.user_id
    username = arg.extract_plain_text().split()
    if _q := get_at_qq(arg):
        qqid = _q
    obj = await maiApi.query_user_dev(qqid=qqid, username=username)
    userdata=await sc50(obj,type=2,music=0)
    await matcher.finish(await generate_other50(userdata,qqid, username), reply_message=True)

@sss_cun50.handle()
async def _(event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()):
    qqid = get_at_qq(arg) or event.user_id
    username = arg.extract_plain_text().split()
    if _q := get_at_qq(arg):
        qqid = _q
    obj = await maiApi.query_user_dev(qqid=qqid, username=username)
    userdata=await sc50(obj,type=2,music=1)
    await matcher.finish(await generate_other50(userdata,qqid, username), reply_message=True)

@sssp_cun50.handle()
async def _(event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()):
    qqid = get_at_qq(arg) or event.user_id
    username = arg.extract_plain_text().split()
    if _q := get_at_qq(arg):
        qqid = _q
    obj = await maiApi.query_user_dev(qqid=qqid, username=username)
    userdata=await sc50(obj,type=2,music=2)
    await matcher.finish(await generate_other50(userdata,qqid, username), reply_message=True)