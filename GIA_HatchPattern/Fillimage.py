import cv2
import numpy as np
import Setting_Hatchpattern as set

def Fillimg(img):
    
    mask = np.all(img[:,:,:] == [0, 0, 0], axis=-1)
    # 元画像をBGR形式からBGRA形式に変換
    dst = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA) 
    # マスク画像をもとに、透明部分を白色化
    dst[mask,0] = 255
    dst[mask,1] = 255
    dst[mask,2] = 255
    dst[mask,3] = 255
    #cv2.imwrite('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\dst.png', dst)
    #cv2.imshow('dst', dst)

    # グレースケール変換
    img_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('img_gray', img_gray)
    #cv2.imwrite('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\img_gray.png', img_gray)

    # 画像の白黒2値化
    ret, thresh = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY)
    #cv2.imwrite('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\threshold.png', thresh)

    # 輪郭抽出
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #for i, cnt in enumerate(contours):
        # 輪郭の面積を計算する。
    #    area = cv2.contourArea(cnt)
    #    print(f"contour: {i}, area: {area}")
    # 円面積(129)以下の輪郭のみ取得、大きい輪郭は排除
    contours_del = list(filter(lambda x: cv2.contourArea(x) < set.obj["pic"]["threshold_area"], contours))
    # 塗りつぶし
    # まっさらな画像に塗りつぶしを行う、塗りつぶされた箇所の透過値を変更する
    img_tmpfill = np.zeros((img.shape[0],img.shape[1],3), np.uint8) 
    for i in range(len(contours_del)):
        cv2.drawContours(img_tmpfill, contours_del, -1, color=(set.obj["fill"]["color_g"], set.obj["fill"]["color_b"], set.obj["fill"]["color_r"]), thickness=-1)
        
    dst_tmpfill = cv2.cvtColor(img_tmpfill, cv2.COLOR_BGR2BGRA) 
    fill_mask = np.all(dst_tmpfill[:,:,:] == [set.obj["fill"]["color_g"], set.obj["fill"]["color_b"], set.obj["fill"]["color_r"], 255], axis=-1)
    dst_tmpfill[fill_mask, 3] = set.obj["fill"]["color_alpha"]
    
    #cv2.imwrite('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\img_tmpfill.png', dst_tmpfill)

    # 元画像imgに塗りつぶし画像dst_tmpfillを合成する
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA) 
    img2gray = cv2.cvtColor(dst_tmpfill, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(img1, img1, mask = mask_inv)
    img2_fg = cv2.bitwise_and(dst_tmpfill, dst_tmpfill, mask = mask)
    dst = cv2.add(img1_bg,img2_fg)

    #cv2.imwrite('C:\\Users\\501796\\Desktop\\HatchPattern\\test\\fillimg.png', dst)

    return dst