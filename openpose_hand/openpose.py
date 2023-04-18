# fashion_pose.py : MPII를 사용한 신체부위 검출
import cv2
import random
HAND_PAIR = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], [0, 9],
             [9, 10], [10, 11], [11, 12], [0, 13], [13, 14], [14, 15], [15, 16],
             [0, 17], [17, 18], [18, 19], [19, 20]
             ]
    
# 각 파일 path
protoFile = "..//openpose//models//hand//pose_deploy.prototxt"
weightsFile = "..//openpose//models//hand//pose_iter_102000.caffemodel"
 
# 위의 path에 있는 network 불러오기
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

# 이미지 읽어오기
image = cv2.imread("image//hand1.jpg")
# image = cv2.resize(image,(640,600))
# image = cv2.resize(image, (0,0), fx = 0.2, fy=0.2)


# frame.shape = 불러온 이미지에서 height, width, color 받아옴
imageHeight, imageWidth, _ = image.shape
 
# network에 넣기위해 전처리
inpBlob = cv2.dnn.blobFromImage(image, 1.0 / 255, (imageWidth, imageHeight), (0, 0, 0), swapRB=False, crop=False)
 
# network에 넣어주기
net.setInput(inpBlob)

# 결과 받아오기
output = net.forward()

print(output.shape)

# output.shape[0] = 이미지 ID, [1] = 출력 맵의 높이, [2] = 너비
H = output.shape[2]
W = output.shape[3]
print("이미지 ID : ", len(output[0]), ", H : ", output.shape[2], ", W : ",output.shape[3]) # 이미지 ID

# 키포인트 검출시 이미지에 그려줌
points = []
for i in range(0,22):
    # 해당 신체부위 신뢰도 얻음.
    probMap = output[0, i, :, :]
 
    # global 최대값 찾기
    minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

    # 원래 이미지에 맞게 점 위치 변경
    x = (imageWidth * point[0]) / W
    y = (imageHeight * point[1]) / H

    # 키포인트 검출한 결과가 0.1보다 크면(검출한곳이 위 BODY_PARTS랑 맞는 부위면) points에 추가, 검출했는데 부위가 없으면 None으로    
    if prob > 0.1 :    
        cv2.circle(image, (int(x), int(y)), 3, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)       # circle(그릴곳, 원의 중심, 반지름, 색)
        cv2.putText(image, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
        points.append((int(x), int(y)))
    else :
        points.append(None)
        print(f"errorpoint {i}")

cv2.imshow("Output-Keypoints",image)
cv2.waitKey(0)

# 이미지 복사
imageCopy = image

#각 POSE_PAIRS별로 선 그어줌 (머리 - 목, 목 - 왼쪽어깨, ...)
for pair in HAND_PAIR:
    partA = pair[0]             # Head
    # partA = BODY_PARTS[partA]   # 0
    partB = pair[1]             # Neck
    # partB = BODY_PARTS[partB]   # 1
    
    red = random.randrange(0, 255)
    green = random.randrange(0, 255)
    blue = random.randrange(0, 255)

    #print(partA," 와 ", partB, " 연결\n")
    if points[partA] and points[partB]:
        cv2.line(imageCopy, points[partA], points[partB], (red, green, blue), 2)

#cv2.imwrite("C:\\opencv test\\human\\save.jpg",imageCopy)
cv2.imshow("Output-Keypoints",imageCopy)
cv2.waitKey(0)
cv2.destroyAllWindows()