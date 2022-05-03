import cv2
import numpy as np
import math
import json

#test/c1.jpg


def delet_contours(contours, delete_list):
    delta = 0
    for i in range(len(delete_list)):
        # print("i= ", i)
        del contours[delete_list[i] - delta]
        delta = delta + 1
    return contours



def drawMyContours(winName, image, contours, draw_on_blank):
    if (draw_on_blank): # 在白底上绘制轮廓
        temp = np.ones(image.shape, dtype=np.uint8) * 255
        cv2.drawContours(temp, contours, -1, (0, 0, 0), 2)
    else:
        temp = image.copy()
        cv2.drawContours(temp, contours, -1, (0, 0, 255), 2)
    cv2.imshow(winName, temp)

def main(path):
    image = cv2.imread(path)

    height, width, channel = image.shape
    image = cv2.resize(image, (int(0.25 * width), int(0.25 * height)), interpolation=cv2.INTER_CUBIC)


    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_hsv = np.array([0, 43, 46])
    high_hsv = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    # cv2.imshow("find_red", mask)
    # cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.erode(mask, kernel, 15)
    cv2.imshow("morphology", mask)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print("find", len(contours), "contours")

    #contours = np.array(cont)
    drawMyContours("find contours", image, contours, True)

    lengths = list()
    for i in range(len(contours)):
        length = cv2.arcLength(contours[i], True)
        lengths.append(length)
        print("轮廓%d 的周长: %d" % (i, length))

    min_size = 20
    max_size = 200
    delete_list = []
    for i in range(len(contours)):
        if (cv2.arcLength(contours[i], True) < min_size) or (cv2.arcLength(contours[i], True) > max_size):
            delete_list.append(i)

    # 根据列表序号删除不符合要求的轮廓
    contours = delet_contours(contours, delete_list)  # 筛选后的轮廓
    print("find", len(contours), "contours left after length filter")  # 打印筛选后的轮廓
    drawMyContours("contours after length filtering", image, contours, False)
    result = image.copy()
    all_information = []
    for i in range(len(contours)):
        rect = cv2.minAreaRect(contours[i])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        draw_rect = cv2.drawContours(image.copy(), [box], -1, (0, 0, 255), 2)
        a = cv2.contourArea(contours[i]) * 4 * math.pi
        b = math.pow(cv2.arcLength(contours[i], True), 2)
        # 中心坐标值
        pt = ((int)((box[1][0] + box[2][0] + box[3][0] + box[0][0]) / 4),
              (int)((box[1][1] + + box[2][1] + box[3][1] + box[0][1]) / 4))

        # 画红点
        cv2.circle(result, pt, 2, (0, 0, 255), 2)

        text = "(" + str(pt[0]) + ", " + str(pt[1]) + ")"
        text1 = [int(box[1][0]), int(box[1][1])]
        text2 = [int(box[2][0]), int(box[2][1])]
        text3 = [int(box[3][0]), int(box[3][1])]
        text4 = [int(box[0][0]), int(box[0][1])]

        textall = text1, text2, text3, text4
        cv2.putText(result, text, (pt[0] + 10, pt[1] + 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1, 8, 0)
        #cv2.putText(result, text1, i, cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1, 8, 0)
        print("box_{}:{},中心坐标为{}, 种类为seed, 圆度为{}\n".format(i, box, text,a / b))
        image = draw_rect
        control = {"ID": i, "Type": "Seed", "Center Coordinate":pt, "Rectangular Coordinate": textall, "Circular Degree": a/b}
        all_information.append(control)
    json.dump(all_information,open('SeedInformation.json','w'),indent=6)
    #cv2.imshow("draw_rect", draw_rect)
    #cv2.imshow("only_res", result)


    for i in range(len(contours)):
        rect = cv2.minAreaRect(contours[i])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        draw_rect = cv2.drawContours(image.copy(), [box], -1, (0, 0, 255), 2)
        # 左上角坐标值
        pt = ((int)((box[1][0] + box[2][0] + box[3][0] + box[0][0]) / 4),
              (int)((box[1][1] + + box[2][1] + box[3][1] + box[0][1]) / 4))
        # 画绿点
        circle = cv2.circle(draw_rect.copy(), pt, 2, (0, 255, 0), 2)
        text = "(" + str(pt[0]) + ", " + str(pt[1]) + ")" + "box_" + str(i)
        all = cv2.putText(circle.copy(), text, (pt[0] + 10, pt[1] + 10), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), 1, 8, 0)
        image = all
    cv2.imshow("all_res", all)
    cv2.waitKey(0)

