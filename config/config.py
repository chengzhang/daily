# coding = utf8
# author: donyzhang
# date: 2023.03.28


import os

from dynaconf import Dynaconf

current_dir = os.path.dirname(os.path.realpath(__file__))
settings = Dynaconf(
    settings_files=os.path.join(current_dir, 'settings.json'),
    environments=True,  # 为 True 则可在一个文件里声明多个环境。环境名任意，除 default 和 global 之外。运行程序前，声明
                        # export ENV_FOR_DYNACONF=<env_name> 来指明环境
)
