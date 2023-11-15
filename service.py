from fastapi import FastAPI
# import logging

import random

from dataModel import GroupMessageData

from qqManger import botManger

app = FastAPI(docs_url=None, redoc_url=None)
# app = FastAPI()
token = "VWPjl0p8jpvX661OYylqbiN-ne1waljF%w"

botIdPoll = [3135775769]


@app.get("/")
async def heartbeat():
    return {"code": 0, "msg": "alive"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {}


@app.get("/sendGroupMessage/")
async def getGroupMessage():
    return {"code": 400, "msg": "Bad access method"}


@app.post("/sendGroupMessage/")
async def postGroupMessage(message: GroupMessageData):
    # logging.debug()
    if message.token != token:  # 权限检查
        return {"code": 400, "msg": "No interface access permission"}
    result = ""
    if message.isAt == True:  # 是否at全体成员，尚未支持
        # result.join("[info] The atMember function is not yet supported\n")
        message.atList=["all"]
    elif message.atList!=None and message.atList != []:
        try:
            for e,v in enumerate(message.atList):
                message.atList[e]=int(v)
        except ValueError as ve:
            result.join("[error] Wrong information at atList")
            return {"code": 400, "msg": f"{result}"}
    if message.isCutting == True:  # 将长消息切片后发送
        result.join("[info] The Cutting function is not yet supported\n")
    if message.botId == None:  # 不填写就自动选择
        message.botId = random.choice(botIdPoll)
        result.join("[info] No bot ID, random ID will be used\n")
    else:
        try:
            message.botId = int(message.botId)
        except ValueError as ve:
            result.join("[warning] Wrong bot ID, random ID will be used\n")
            message.botId = random.choice(botIdPoll)
    if (x := len(message.msg.encode("utf-8"))) > 2000:
        result.join("[error] Message length exceeds the limit")
        return {"code": 500, "msg": f"{result}"}
    if message.msg == "":
        result.join("[error] Message is empty")
        return {"code": 500, "msg": f"{result}"}
    if not (await check_group(message)):
        result.join("[error] Haven't joined this group yet")
        return {"code": 400, "msg": f"{result}"}

    try:
        x = botManger(message.botId)
        status = await x.sendGroupMessage(message)
    except BaseException as be:
        return {"code": 500, "msg": f"Unknown error:{be}"}
    
    if int(status["code"]) == 0:
        result.join("[info] "+status["msg"])
        return {"code": 0, "msg": f"{result}"}
    else:
        fcode = int(status["code"])
        result.join("[error] "+status["msg"])
        return {"code": fcode, "msg": f"{result}"}
    # except BaseException as be:
    #     return {"code": 500, "msg": f"[serious] Unknown error, details: {be}"}


async def check_group(msg: GroupMessageData):  # 检查群组是否存在

    return True
