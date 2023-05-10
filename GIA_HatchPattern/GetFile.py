import glob
import os
import cv2
import numpy as np
import Setting_Hatchpattern as set

def GetXFoldersList(dir):
    # zoomレベル17、X座標のフォルダ取得
    joinpath = os.path.join(dir, str(set.obj["pic"]["zoomlevel"]))
    xpathlist = glob.glob(joinpath + '/*')

    xnamelist = []
    for path in xpathlist:
        xnamelist.append(os.path.basename(path))

    return xpathlist, xnamelist


def GetYFileList(dir):
    # Y座標のファイル取得
    return glob.glob(dir + '\*')


def GetImagefromPathList(path):
    if len(path) != 0:
        return cv2.imread(path[0])                 # pathがあれば画像を読み込んで返す
    else:
        return np.zeros((256,256,3), np.uint8)  # path無ければ黒画像を返す