import nonebot
from nonebot.plugin import PluginMetadata, require

from .command import *

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-maimaidx-extra",
    description="基于nonebot-plugin-maimaidx开发的额外插件",
    usage="使用 ap50帮助 来查看帮助列表（还没写）",
    type="application",
    homepage="暂无",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

@driver.on_startup
async def get_music():
    """bot启动时获取本地存储的乐曲数据和token"""
    maiApi.load_token()
    await mai.get_music()