#!-*- coding:utf-8 -*-
# python3.7
# CreateTime: 2023/9/21 16:32
# FileName:

import os

# 飞书机器人
FeiShuErrorRobot = ''

# 阿里云盘登录扫码端口
AliLoginPort = 80

# ---------------------------覆盖配置----------------------------------

# 从系统环境中重载变量
for var, var_value in locals().copy().items():
    # 变量命名要求大写开头
    if not var[0].isupper() or callable(var_value):
        continue

    locals()[var] = os.getenv(var, var_value)

# 本地测试时，可增加local_config.py来覆盖配置
try:
    from local_config import *
except:
    pass
# ----------------------------------------------------------------
