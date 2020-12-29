import cv2
def detect_face(raw_frame,img):
    face_detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #使用人脸识别分类器进行人脸识别，返回人脸所在的矩形
    faceRects=face_detector.detectMultiScale(img,scaleFactor=1.2,minNeighbors=7,
                                             minSize=(500,500),flags=cv2.CASCADE_SCALE_IMAGE)
    face_gray=[];face_color=[];
    face_x=[];face_y=[]
    for (x,y,w,h)in faceRects:
        cv2.rectangle(raw_frame,(x,y),(x+w,y+h),(255,255,0),2)
        face=img[y:y+h,x:x+w]
        face_gray.append(face)
        face=raw_frame[y:y+h,x:x+w]
        face_color.append(face)
        face_x.append(x)
        face_y.append(y)
        #print('x--',x,' y--',y,' w--',w,' h--',h)
    return face_gray,face_color,face_x,face_y

def detect_eye(img,frame):
    eye_detector=cv2.CascadeClassifier('haarcascade_eye.xml')
    #使用人眼识别分类器进行人眼识别，返回人眼所在的矩形
    eyeRects=eye_detector.detectMultiScale(img,scaleFactor=1.2,minNeighbors=3,
                                             minSize=(20,20),flags=cv2.CASCADE_SCALE_IMAGE)
    (height,width)=img.shape[:2]

    eyes=[]
    for eye in eyeRects:
        (x,y,w,h)=eye
        if (y<height/3):
            # print('判定为眼睛')
            # print('eye_y--', y, ' eye_h--', height)
            #cv2.imshow("eye",frame[y:y+h,x:x+w])
            # cv2.waitKey(0)
            eyes.append(eye)
        else:
            # print('判定为嘴巴')
            #cv2.imshow("mouth",frame[y:y+h,x:x+w])
            # print('eye_y--', y, ' eye_h--', height)
            # cv2.waitKey(0)
            pass

    if len(eyes)<2:
        for i in range(len(eyes)):
            (x,y,w,h)=eyes[i]
            if (x+w/2)<width/2 :
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                # print('圈出右眼--x--',x,'  w--',width)
                gray=img[y:y+h,x:x+w]
                color=frame[y:y+h,x:x+w]
                return(gray,color,1,x,y)#1代表右眼
            else:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                # print('圈出左眼--x--',x,'  w--',width)

                gray=img[y:y+h,x:x+w]
                color=frame[y:y+h,x:x+w]
                return(gray,color,2,x,y)#2代表左眼
        return [0]
    else:
        minL = 5000;
        minR = 5000;
        for i in range(len(eyes)):
            (x, y, w, h) = eyes[i]
            if x<width/2:
                dist = abs(x + w / 2 - width / 2)
                if dist<minR:
                    minR=dist
                    k1=i
            else:
                dist = abs(x + w / 2 - width / 2)
                if dist < minL:
                    minL=dist
                    k2=i
        try:
            (x1, y1, w1, h1)=eyes[k1]
            # (x2, y2, w2, h2)=eyes[k2]
        except UnboundLocalError:
            k1=k2
            (x1, y1, w1, h1)=eyes[k1]
        try:
            # (x1, y1, w1, h1)=eyes[k1]
            (x2, y2, w2, h2)=eyes[k2]
        except UnboundLocalError:
            k2=k1
            (x2, y2, w2, h2)=eyes[k2]

        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
        cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
        cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
        # print('同时圈出右眼--x--', x1, '  w--', width)
        # print('同时圈出左眼--x--', x2, '  w--', width)
        # print('此时有', len(eyes), '个候选点')
        right_gray = img[y1:y1 + h1, x1:x1 + w1]
        right_color = frame[y1:y1 + h1, x1:x1 + w1]
        left_gray = img[y2:y2 + h2, x2:x2 + w2]
        left_color = frame[y2:y2 + h2, x2:x2 + w2]
        return (right_gray,right_color,left_gray,left_color,x1,y1,x2,y2)

def detect_pupil(gray,color,name):
    #二值化灰度图像
    _,threshold=cv2.threshold(gray,50,255,cv2.THRESH_BINARY_INV)
    (height,width)=gray.shape[:2]
    min=1000
    i=5
    struct1=cv2.getStructuringElement(0,(i,i))
    struct2=cv2.getStructuringElement(0,(4*i,4*i))
    struct3=cv2.getStructuringElement(0,(2*i,2*i))
    open_img=cv2.morphologyEx(threshold,cv2.MORPH_OPEN,struct1)
    dialate_img=cv2.morphologyEx(open_img,cv2.MORPH_DILATE,struct2)
    erod_img=cv2.morphologyEx(dialate_img,cv2.MORPH_ERODE,struct3)
    (number,out,stats,centroids)=cv2.connectedComponentsWithStats(erod_img)
    for i in range(1,number):
        centroid=centroids[i]
        centroid_x=centroid[0]
        # if stats[i][0]==0:
        #     continue
        if abs(centroid_x-width/2)<min:
            min=abs(centroid_x-width/2)
            k=i
    try:
        centroid=centroids[k]
    except UnboundLocalError:
        centroid=centroids[0]

    x=int(centroid[0])
    y=int(centroid[1])
    cv2.line(color,(x-3,y),(x+3,y),(0,255,0),1)
    cv2.line(erod_img,(x-3,y),(x+3,y),(0,255,0),1)
    cv2.line(color,(x,y-3),(x,y+3),(0,255,0),1)
    cv2.line(erod_img,(x,y-3),(x,y+3),(0,255,0),1)
    cv2.imshow(name+'_threshold',erod_img)
    # cv2.waitKey(0)
    #print(name,'眼球横坐标--',x,'纵坐标--',y)
    return x,y


def analysis(eye_symbol,base_symbol,x,base_x,width,y,base_y,h,ru,rd,r,number_img,lu,ld,l,s):
    if not base_symbol and x < base_x - width:
        # print('通过右眼扫描检测到当前眼睛向右移动')
        if y < base_y - int(h/2):
            ru += 1
        elif y > base_y + h:
            rd += 1
        else:
            r += 1
        number_img += 1
        eye_symbol = True
    elif not base_symbol and x > base_x + width:
        # print('通过右眼扫描检测到当前眼睛向左移动')
        if y < base_y - int(h/2):
            lu += 1
        elif y > base_y + h:
            ld += 1
        else:
            l += 1
        number_img += 1
        eye_symbol = True
    elif not base_symbol:
        # print("通过右眼扫描检测到当前眼睛保持不动")
        s += 1
        number_img += 1
        eye_symbol = True
    return eye_symbol,r,l,s,ru,rd,lu,ld