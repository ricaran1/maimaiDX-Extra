from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

from ..libraries.image import to_bytes_io
from ..libraries.maimaidx_music_info import *
from ..libraries.maimaidx_player_score import *
from ..libraries.maimaidx_update_plate import *
from ..libraries.maimaidx_extra import ap50
def get_at_qq(message: Message) -> Optional[int]:
    for item in message:
        if isinstance(item, MessageSegment) and item.type == 'at' and item.data['qq'] != 'all':
            return int(item.data['qq'])
        
Ap50  = on_command('ap50', aliases={'AP50','aP50','Ap50'}, priority=5)

@Ap50.handle()
async def _(event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()):
    qqid = get_at_qq(arg) or event.user_id
    username = arg.extract_plain_text().split()
    if _q := get_at_qq(arg):
        qqid = _q
    obj = await maiApi.query_user_dev(qqid=qqid, username=username)
    userdata=await ap50(obj)
    await matcher.finish(await generate_other50(userdata,qqid, username), reply_message=True)