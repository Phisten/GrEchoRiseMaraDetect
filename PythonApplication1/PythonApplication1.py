
import cv2
import numpy as np

from os import listdir
from os.path import isfile, isdir, join


ImgPath = "C:\STEN\\"

def GaussianBlur(Img):
    return cv2.GaussianBlur(Img,(3,3),0)
def PathImg(ImgName):
    return cv2.imread(ImgPath + ImgName)


tpImg_Star = GaussianBlur(PathImg('star.png'))
colorCount , tmpStar_w, tmpStar_h = tpImg_Star.shape[::-1]

stars_x = (179,321,463,605,747,889,1031,179,321,463,605)
stars_y = (304,304,304,304,304,304,304,479,479,479,479)
star_w = 17
star_h = 18

method = cv2.TM_SQDIFF_NORMED
font = cv2.FONT_HERSHEY_SIMPLEX 

def CountStar(gImg):
    starCount = [0,0,0,0,0,0,0,0,0,0,0]
    star4 = 0
    star3 = 0
    for j in range(11):
        for i in range(0,4):
            x = stars_x[j]
            y = stars_y[j]
            tmpXshift = star_w * i
            res = cv2.matchTemplate(gImg[y:y+star_h,x+tmpXshift:x+tmpXshift+star_w],tpImg_Star,cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc[0]+x+tmpXshift,min_loc[1]+y
                matchVal = 1 - min_val
            else:
                top_left = max_loc[0]+x+tmpXshift,max_loc[1]+y
                matchVal = min_val

            bottom_right = (top_left[0] + tmpStar_w, top_left[1] + tmpStar_h)

            if matchVal >= 0.9:
                starCount[j]+=1
                cv2.rectangle(srcImg,top_left, bottom_right, (0,0,255), 1)
                #cv2.putText(srcImg,str(round(matchVal,2)),(bottom_right[0],bottom_right[1]+i*15+20),font,0.4,(0,255,255))
        if starCount[j] == 4:
            star4+=1
        elif starCount[j] == 3:
            star3+=1
    return (star4,star3)


# 指定要列出所有檔案的目錄
mypath = "\\Mac\Home\Downloads\Phisten"

# 取得所有檔案與子目錄名稱
files = listdir(mypath)

# 以迴圈處理
for f in files:
  # 產生檔案的絕對路徑
  fullpath = join(mypath, f)
  # 判斷 fullpath 是檔案還是目錄
  if isfile(fullpath):
    print("檔案：", f)
  elif isdir(fullpath):
    print("目錄：", f)


srcImg = PathImg("heroList.png")
gImg = GaussianBlur(srcImg)

#resS4,resS3 = CountStar(gImg)
#cv2.imshow(str(resS4) + str(resS3),srcImg)

cv2.waitKey(0)
cv2.destroyAllWindows()
    