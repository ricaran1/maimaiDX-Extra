class UserNotFoundError(Exception):
    
    def __str__(self) -> str:
        return '''未找到您的QQ对应的水鱼查分器数据！请点击水鱼查分器的编辑个人资料按钮并在绑定QQ号中填写你的QQ号。
水鱼官网：https://www.diving-fish.com/maimaidx/prober/'''


class UserDisabledQueryError(Exception):
    
    def __str__(self) -> str:
        return '该用户禁止了其他人获取数据。'
    

class ServerError(Exception):
    
    def __str__(self) -> str:
        return '别名服务器错误，请联系插件开发者'


class EnterError(Exception):
    
    def __str__(self) -> str:
        return '参数输入错误'


class CoverError(Exception):
    """图片错误"""


class UnknownError(Exception):
    """未知错误"""