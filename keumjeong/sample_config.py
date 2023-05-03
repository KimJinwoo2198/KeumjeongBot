'''
Sample Config
'''

class Config(object):
    '''Config'''
    TOKEN = ''  # 봇 토큰
    OWNERS = []  # 관리자의 아이디
    DebugServer = []  # 채널 id
    BOT_NAME = ""  # 봇 이름
    BOT_TAG = ""  # 태그
    BOT_ID =      # 봇 아이디
    AboutBot = ""  # 봇 정보
    color_code = 0x2f3136  # 색상코드
    error_cc = 0xf12101 # 에러 색상코드

    email_id = '' # 이메일 아이디
    email_password = '' # 비밀번호

class Production(Config):
    '''Production Logger'''
    LOGGER = False


class Development(Config):
    '''Production Logger'''
    LOGGER = True
