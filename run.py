from service import app

from loguru import logger
logger.add("./log/file_{time}.log", rotation="12:00",backtrace=True, diagnose=True) # 每天12:00会创建一个新的文件
logger.debug("service start")




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1141)