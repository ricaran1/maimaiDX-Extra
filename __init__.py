import nonebot
from nonebot.plugin import PluginMetadata, require
from .command import *

scheduler = require('nonebot_plugin_apscheduler')

from nonebot_plugin_apscheduler import scheduler

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-maimaidx-extra",
    description="基于nonebot-plugin-maimaidx开发的额外插件",
    usage="使用 ap50帮助 来查看帮助列表（还没写）",
    type="application",
    homepage="https://github.com/ricaran1/maimaiDX-Extra",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath('plugins').resolve())
)


@driver.on_startup
async def get_music():
    """
    bot启动时开始获取所有数据
    """
    if maiconfig.maimaidxproberproxy:
        log.info('正在使用代理服务器访问查分器')
    if maiconfig.maimaidxaliasproxy:
        log.info('正在使用代理服务器访问别名服务器')
    await mai.get_music()
    maiApi.load_token_proxy()

