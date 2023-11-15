# -*- coding: utf-8 -*-
import requests
from requests import exceptions

import json
from loguru import logger

from dataModel import GroupMessageData

class getGroupInfo:
    def __init__(self,ssid) -> None:
        self.ssid=ssid

class getGroupList:
    def __init__(self,ssid:str) -> None:
        self.ssid=ssid
        self.url=f"http://127.0.0.1:7895/groupList?sessionKey={ssid}"

class sendMessage:
    def __init__(self,ssid:str, a: GroupMessageData) -> None:
        self.verifyKey = "1793159"
        self.url = "http://127.0.0.1:7895/sendGroupMessage"
        self.data=a
        self.sessionKey = ssid
        self.groupid=a.group
        # self.sendGroupMessage([
        #     {"type": "Plain", "text": "hello "},
        #     {"type": "Plain", "text": "world"}
        # ])
    @logger.catch
    async def _makeAtList(self)->list[dict]: 
        # temp={"type": "At","target": 123456,"display": "@Mirai"}
        '''
        构建AT列表的消息链 
        '''
        ans=[]
        for i in self.data.atList:
            temp={"type": "At","target": i}
            ans.append(temp)
        return ans
    @logger.catch
    async def send(self):
        '''
        发送群组消息
        '''
        data = {
            "sessionKey": self.sessionKey,
            "target": self.groupid,
            "messageChain": []
        }
        if self.data.atList != [] and self.data.atList!=None:
            if self.data.atList[0]=="all":
                data["messageChain"]=[{"type": "AtAll"}]
            else:
                data["messageChain"]=await self._makeAtList()
        data["messageChain"].append({"type": "Plain", "text": f"{self.data.msg}"})
        try:
            return requests.post(self.url, data=json.dumps(data)).json()
        except exceptions.RequestException as re:
            return {"code":500,"msg":f"{re}"}

    # def main(self):
    #     ssessionkey=get_ssid().json()
    #     print(ssessionkey)
    #     pass


class botManger:
    def __init__(self,qq:int) -> None:
        self.verifyKey = "1793159"
        self.url = "http://127.0.0.1:7895"
        self.sessionKey = ""
        self.qq=qq
        self.get_ssid()
        self.bind()
    @logger.catch
    def get_ssid(self):
        verifyKey = self.verifyKey
        url = self.url
        data = {
            "verifyKey": verifyKey
        }
        x = requests.post(
            url+"/verify", data=json.dumps(data)).json()['session']
        self.sessionKey = x
    @logger.catch
    def bind(self):
        '''
        绑定ssid
        '''
        url = self.url+"/bind"
        data = {
            "sessionKey": f"{self.sessionKey}",
            "qq": self.qq
        }
        print(requests.post(url, data=json.dumps(data)).json())
    # def getBotList(self)->list:
    #     url=self.url+"/botList"
    #     return requests.get(url).json()["data"]
    @logger.catch
    async def sendGroupMessage(self,a: GroupMessageData)->dict:
        return await sendMessage(ssid=self.sessionKey,a=a).send()
    def __del__(self):
        url = self.url+"/release"
        data = {
            "sessionKey": f"{self.sessionKey}",
            "qq": self.qq
        }
        x = requests.post(url, data=json.dumps(data)).json()


# if __name__ == "__main__":
#     A = sendMessage(737919624)

# if __name__ == '__main__':
#     server = HTTPServer(host, My_Server)
#     print("server启动@ : %s:%s" % host)
#     server.serve_forever()
