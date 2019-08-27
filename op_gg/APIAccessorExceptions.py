from op_gg.routes import render_template



class APIAccessorException(Exception):
    pass

class InvalidAPiKeyException(APIAccessorException):
    def __init__(self,message):
        self.message = message

class InvalidSummonerNameException(APIAccessorException):
    def __init__(self,message):
        self.message = message





