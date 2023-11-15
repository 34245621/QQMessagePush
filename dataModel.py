from pydantic import BaseModel

class GroupMessageData(BaseModel):# 发送群信息时需要的模型
    token:str
    msg:str=""
    isAt:bool|None = None
    group:str|int|None=None
    isCutting:bool|None = None# 多次发送，暂未支持
    botId:str|int|None # 选择发送消息的机器人ID 
    atList:list[int]|None = None# at列表