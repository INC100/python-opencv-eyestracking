from detect import *
import pyautogui
import datetime
video=cv2.VideoCapture('face_up.mp4')
base_right_x=base_right_y=base_left_x=base_left_y=0
base_symbol=True
right=left=base_number=500
time_rr=time_rl=time_lr=time_ll=time_rs=time_ls=time_rru=time_rrd=time_llu=time_lld=time_rlu=time_rld=time_lru=time_lrd=0
number_img=0;eye_symbol=False
#[time_rs, time_rr, time_rru, time_rrd, time_rlu, time_rld, time_rl]
stage = ['静止', '右移', '右上','右下','左上','左下','左移']
h=6;width=20;
re=le=face=photo=0;
while True:
    start_time=datetime.datetime.now()
    #grabbed验证视频是否读取成功
    (grabbed,raw_frame)=video.read()
    if not grabbed:
        break
    (height,widths)=raw_frame.shape[:2]
    # ratio=300/width
    dim=(widths,height)
    # frame=cv2.resize(raw_frame,dim,interpolation=cv2.INTER_AREA)
    photo=photo+1;
    #彩色图像转换为灰度图像
    gray=cv2.cvtColor(raw_frame,cv2.COLOR_BGR2GRAY)
    faces_gray,faces_color,faces_x,faces_y=detect_face(raw_frame,gray)
    face_time=datetime.datetime.now()
    for i in range(len(faces_gray)):
        face_gray=faces_gray[i]
        face_color=faces_color[i]
        face_x=faces_x[i]
        face_y=faces_y[i]
        cv2.imshow("face",face_color)
        eyes=detect_eye(face_gray,face_color)
        eyes_time=datetime.datetime.now()
        face=face+1
        if len(eyes)==5:
            eye_gray,eye_color,k,eye_x,eye_y=eyes
            if k==1:
                #右眼
                re=re+1;
                #cv2.imshow("right_eye",eye_color)
                right_x,right_y=detect_pupil(eye_gray, eye_color,"right")
                right_x=face_x+eye_x+right_x
                right_y=face_y+eye_y+right_y
                eye_symbol, time_rr, time_rl, time_rs, time_rru, time_rrd, time_rlu, time_rld=\
                    analysis(eye_symbol,base_symbol,right_x,base_right_x,width,right_y,base_right_y,h,time_rru,time_rrd,time_rr,number_img,time_rlu,time_rld,time_rl,time_rs)
                if right != 0 and base_symbol:
                    try:
                        base_right_x = right_x + base_right_x
                        base_right_y = base_right_y + right_y
                        right = right - 1
                        print('第', abs(right - base_number), '次检测到右眼')
                    except NameError:
                        pass
            else:
                #cv2.imshow("left_eye",eye_color)
                le=le+1;
                left_x,left_y=detect_pupil(eye_gray, eye_color,"left")
                left_x=left_x+eye_x+face_x
                left_y=left_y+eye_y+face_y
                eye_symbol, time_lr, time_ll, time_ls, time_lru, time_lrd, time_llu, time_lld = \
                    analysis(eye_symbol,base_symbol, left_x, base_left_x, width, left_y, base_left_y, h, time_lru, time_lrd,
                             time_rr, number_img, time_rlu, time_rld, time_rl, time_rs)
                if left != 0 and base_symbol:
                    try:
                        base_left_x = base_left_x + left_x
                        base_left_y = base_left_y + left_y
                        left = left - 1
                        print('第', abs(left - base_number), '次检测到左眼')
                    except NameError:
                        pass
            pupil_time=datetime.datetime.now()
        elif len(eyes)==8:
            right_gray, right_color, left_gray, left_color,right_eye_x,right_eye_y,left_eye_x,left_eye_y=eyes
            le=le+1;re=re+1;
            right_x,right_y=detect_pupil(right_gray,right_color,"right")
            left_x,left_y=detect_pupil(left_gray,left_color,"left")
            right_x = face_x + right_eye_x + right_x
            right_y = face_y + right_eye_y + right_y
            left_x = left_x + left_eye_x + face_x
            left_y = left_y + left_eye_y + face_y
            eye_symbol, time_rr, time_rl, time_rs, time_rru, time_rrd, time_rlu, time_rld = \
                analysis(eye_symbol,base_symbol, right_x, base_right_x, width, right_y, base_right_y, h, time_rru, time_rrd,
                         time_rr, number_img, time_rlu, time_rld, time_rl, time_rs)

            eye_symbol, time_lr, time_ll, time_ls, time_lru, time_lrd, time_llu, time_lld = \
                analysis(eye_symbol,base_symbol, left_x, base_left_x, width, left_y, base_left_y, h, time_lru, time_lrd,
                         time_rr, number_img, time_rlu, time_rld, time_rl, time_rs)
            if right != 0 and base_symbol:
                try:
                    base_right_x = right_x + base_right_x
                    base_right_y = base_right_y + right_y
                    right = right - 1
                    print('第', abs(right - base_number), '次检测到右眼')
                except NameError:
                    pass
            if left != 0 and base_symbol:
                try:
                    base_left_x = base_left_x + left_x
                    base_left_y = base_left_y + left_y
                    left = left - 1
                    print('第', abs(left - base_number), '次检测到左眼')
                except NameError:
                    pass
            pupil_time=datetime.datetime.now()


    if right == 0 and left == 0 and base_symbol:
        base_left_x = int(base_left_x / base_number)
        base_right_x = int(base_right_x / base_number)
        base_left_y = int(base_left_y / base_number)
        base_right_y = int(base_right_y / base_number)
        # base_left_x=1225
        # base_left_y=352
        # base_right_x=973
        # base_right_y=368
        print('左眼基准坐标为', str((base_left_x, base_left_y)))
        print('右眼基准坐标为', str((base_right_x, base_right_y)))
        base_symbol = False


    if (number_img%5==0) and eye_symbol and not base_symbol:
        right_array=[time_rs,time_rr,time_rru,time_rrd,time_rlu,time_rld,time_rl]
        left_array=[time_ls,time_lr,time_lru,time_lrd,time_llu,time_lld,time_ll]
        real_right=max(right_array)
        real_left=max(left_array)
        right_idx=right_array.index(max(right_array))
        left_idx=left_array.index(max(left_array))
        if real_right>real_left:
            print("经比较，右眼置信度较高，判定眼睛动作为",stage[right_idx])
            right=right_idx
        elif real_right<real_left:
            print("经比较，左眼置信度较高，判定眼睛动作为",stage[left_idx])
            right=left_idx
        else:
            right=right_idx
            print("经比较，两眼置信度相等，左眼判定眼睛动作为",stage[left_idx],"右眼判定眼睛动作为",stage[right_idx])
        # [time_rs, time_rr, time_rru, time_rrd, time_rlu, time_rld, time_rl]
        currentMouseX, currentMouseY = pyautogui.position()
        if 1380>currentMouseX>541 and 801<currentMouseY<1060:
            if right==0:
                #点击
                pyautogui.click()
            elif right==1:
                #右移
                pyautogui.moveRel(60,0,0.25)
            elif right==2:
                pyautogui.moveRel(60,-56,0.25)
            elif right==3:
                pyautogui.moveRel(60,56,0.25)
            elif right==4:
                pyautogui.moveRel(-60,-56,0.25)
            elif right==5:
                pyautogui.moveRel(-60,56,0.25)
            elif right==6:
                pyautogui.moveRel(-60,0,0.25)
        else:
            pass


        eye_symbol=False
        time_rr = time_rl = time_lr = time_ll = time_rs = time_ls = time_rru = time_rrd = time_llu = time_lld = time_rlu = time_rld = time_lru = time_lrd = 0

    cv2.imshow("original",raw_frame)

    end_time=datetime.datetime.now()

    with open('program_records.txt','a')as f:
        content='对一张图片执行完所有操作共需'+str((end_time-start_time).microseconds/1000000)+'秒\n'\
        +'从图像中检测人脸需'+str((face_time-start_time).microseconds/1000000)+'秒\n'\
        +'从人脸中检测人眼需'+str((eyes_time-face_time).microseconds/1000000)+'秒\n'\
        +'从人眼中检测眼球需'+str((pupil_time-eyes_time).microseconds/1000000)+'秒\n\n'
        f.write(content)
    # 等待1ms
    cv2.waitKey(1)
#
    if cv2.waitKey(1)& 0xFF == ord("q"):
        break
# 释放资源和窗口
video.release()

with open('program_records.txt', 'a')as f:
    content = "视频共有%d帧图像\n从视频中共检测到%d张人脸\n从视频中共检测出%d次左眼，%d次右眼\n"%(photo,face,le,re)
    f.write(content)

















