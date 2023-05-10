import toml
import os
import logging
import sys

logger = logging.getLogger('HatchPatternLog')
logging.basicConfig(filename = "Log.txt",                                        # ログファイル名 
                    filemode = "a",                                              # ファイル書込
                    level    = logging.DEBUG,                                    # ログレベル
                    format   = " %(asctime)s - %(levelname)s - %(module)s - line:%(lineno)s - %(message)s "     # ログ出力フォーマット
                    )
#logger.setLevel(10)
#fh = logging.FileHandler('Log.log')
#logger.addHandler(fh)
#formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcname)s - %(message)s')	
#fh.setFormatter(formatter)


# 設定ファイル読込
if not os.path.isfile('settings.toml'):
    logger.error('設定ファイル(settings.toml)がありません')
    sys.exit(0)
else:
    try:
        obj = toml.load('settings.toml')
    except Exception as e:
        logger.error('設定ファイル(settings.toml)の読込エラー')
        sys.exit(0)