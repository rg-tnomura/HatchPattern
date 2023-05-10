import cv2
import numpy as np
import GetFile
import Fillimage
import os
#import skimage.io
import skimage.util
import Setting_Hatchpattern as set
import PySimpleGUI as psg
import argparse
import sys

#### test ####
#img = cv2.imread('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\test_pattern.png')
#retimg = Fillimage.Fillimg(img)
#### test ####

parser = argparse.ArgumentParser()

parser.add_argument('-inpath', type=str, default="")
parser.add_argument('-outpath', type=str, default="")
args = parser.parse_args()
#infolderpath = set.obj["path"]["in_path"]

if not os.path.isdir(args.inpath):
    set.logger.error('-inpath 引数の入力フォルダが存在しません')
    sys.exit(0)
else:
    infolderpath = args.inpath
if not os.path.isdir(args.outpath):
    set.logger.error('-outpath 引数の出力フォルダが存在しません')
    sys.exit(0)
else:
    outfolderpath = args.outpath

# 画像の読み込み
Xpathlist, Xnamelist = GetFile.GetXFoldersList(infolderpath)

# プログレスバー準備
# ファイル数カウント
filecount = 0
for current_dir, sub_dirs, files_list in os.walk(os.path.join(infolderpath, str(set.obj["pic"]["zoomlevel"]))): 
  for file_name in files_list: 
      if os.path.isfile(os.path.join(current_dir, file_name)) == True:
          filecount += 1

if 0 == filecount:
    set.logger.warning('入力フォルダ(%s)にファイルがありません', os.path.join(infolderpath, str(set.obj["pic"]["zoomlevel"])))

# プログレスバーレイアウト
layout = [[psg.Text('処理中')], [psg.Text('ファイル：', key="txt_in")], [psg.ProgressBar(filecount, orientation='h', size=(60,20), key="prog")]]
window = psg.Window("進捗状況", layout)
psgevent, psgvalues = window.read(timeout=1)    #read待機時間を1msにする

progcount = 0   #処理完了した数

# 各X座標フォルダ下にあるY座標画像リストを取得
for xpath in Xpathlist:
    yfilelist = GetFile.GetYFileList(xpath)

    # 塗りつぶし対象画像の周り8方向の画像と連結してから塗りつぶし処理を行い、処理後に対象画像個所を切り取って保存
    for targetimgpath in yfilelist:
        targetimg = cv2.imread(targetimgpath)
        window["txt_in"].update('ファイル：' + targetimgpath)
        #cv2.imwrite('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\_inimage.png', targetimg)
        # Y方向(列方向)隣に画像があるか調べる
        name = os.path.basename(targetimgpath)
        targetYval = int(os.path.splitext(name)[0])
        upYpath = [s for s in yfilelist if str(targetYval - 1) in s] # Y方向上
        img_upY = GetFile.GetImagefromPathList(upYpath)
        plusYpath = [s for s in yfilelist if str(targetYval + 1) in s] # Y方向下
        img_downY = GetFile.GetImagefromPathList(plusYpath)

        img_center = skimage.util.montage([img_upY, targetimg, img_downY], grid_shape=(3, 1), channel_axis=3) # 中央の画像3×1
        #cv2.imwrite('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\img_center.png', img_center)
        
        targetXval = int(os.path.splitext(os.path.basename(xpath))[0])
        leftXlist = [s for s in Xpathlist if str(targetXval - 1) in s]
        if leftXlist:
            tempyfilelist = GetFile.GetYFileList(leftXlist[0])
            leftXY = [s for s in tempyfilelist if str(targetYval) in s] # X方向左 Y
            img_leftXY = GetFile.GetImagefromPathList(leftXY)
            leftXupY = [s for s in tempyfilelist if str(targetYval - 1) in s] # X方向左 Y方向上
            img_leftXupY = GetFile.GetImagefromPathList(leftXupY)
            leftXdownY = [s for s in tempyfilelist if str(targetYval + 1) in s] # X方向左 Y方向下
            img_leftXdownY = GetFile.GetImagefromPathList(leftXdownY)
            img_left = skimage.util.montage([img_leftXupY, img_leftXY, img_leftXdownY], grid_shape=(3, 1), channel_axis=3) # 左の画像3×1
        else:
            img_left = np.zeros((768,256,3), np.uint8) # 左の画像3×1
        #cv2.imwrite('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\img_left.png', img_left)

        rightXlist = [s for s in Xpathlist if str(targetXval + 1) in s]
        if rightXlist:
            tempyfilelist = GetFile.GetYFileList(rightXlist[0])
            rightXY = [s for s in tempyfilelist if str(targetYval) in s] # X方向左 Y
            img_rightXY = GetFile.GetImagefromPathList(rightXY)
            rightXupY = [s for s in tempyfilelist if str(targetYval - 1) in s] # X方向左 Y方向上
            img_rightXupY = GetFile.GetImagefromPathList(rightXupY)
            rightXdownY = [s for s in tempyfilelist if str(targetYval + 1) in s] # X方向左 Y方向下
            img_rightXdownY = GetFile.GetImagefromPathList(rightXdownY)
            img_right = skimage.util.montage([img_rightXupY, img_rightXY, img_rightXdownY], grid_shape=(3, 1), channel_axis=3) # 右の画像3×1
        else:
            img_right = np.zeros((768,256,3), np.uint8) # 右の画像3×1
        #cv2.imwrite('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\img_right.png', img_right)

        img_concat = cv2.hconcat([img_left, img_center, img_right])
        #cv2.imwrite('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\img_concat.png', img_concat)

        # 塗りつぶし
        try:
            img_fill = Fillimage.Fillimg(img_concat)
        except Exception as e:
            logger.error('塗りつぶし処理中エラー')
            sys.exit(0)

        # 対象画像だけ切り取り
        img_cut = img_fill[256:512, 256:512]
        
        # 黒色部分を透明化
        img_alphaglay = cv2.cvtColor(img_cut, cv2.COLOR_BGR2GRAY)
        ret_alp, threshold_alp = cv2.threshold(img_alphaglay, 1, 255, cv2.THRESH_BINARY)
        dst_alpha = cv2.cvtColor(threshold_alp, cv2.COLOR_GRAY2BGR) 
        mask_alpha = np.all(dst_alpha[:,:,:] == [0, 0, 0], axis=-1)
        img_save = cv2.cvtColor(img_cut, cv2.COLOR_BGR2BGRA) 
        img_save[mask_alpha,3] = 0
        
        # 保存
        #savepath = os.path.join(set.obj["path"]["out_path"], str(set.obj["pic"]["zoomlevel"]), str(targetXval))
        #if not os.path.exits(savepath):
        savepath = os.path.join(outfolderpath, str(set.obj["pic"]["zoomlevel"]), str(targetXval))
        os.makedirs(savepath, exist_ok = True)
        cv2.imwrite(os.path.join(savepath, str(targetYval) + '.png'), img_save)

        progcount += 1
        window["prog"].update(progcount)

window.close()
cv2.destroyAllWindows()