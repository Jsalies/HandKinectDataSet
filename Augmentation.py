# -*- coding: utf-8 -*-
import os
from lxml import etree
import cv2
import time
from natsort import natsorted
import writexml

Xml_file="Xml"
Image_file="Images"

xml_list=natsorted(os.listdir(Xml_file), key=lambda y: y.lower())
img_list=natsorted(os.listdir(Image_file), key=lambda y: y.lower())

valueH=int(img_list[-1].split(".")[0].split("_")[1])
valueV=int(img_list[-1].split(".")[0].split("_")[1])+len(img_list)
valueR=int(img_list[-1].split(".")[0].split("_")[1])+2*len(img_list)

for image in img_list:
    valueH+=1
    valueV+=1
    valueR+=1
    picture=cv2.imread(Image_file+"/"+image)
    reversedH=cv2.flip(picture,1)
    reversedV=cv2.flip(picture,0)
    rows,cols,dim=picture.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 180, 1)
    pictureR = cv2.warpAffine(picture, M, (cols, rows))

    cv2.imwrite(Image_file+"/Hand_"+str(valueH)+".jpg",reversedH)
    cv2.imwrite(Image_file+"/Hand_"+str(valueV)+".jpg",reversedV)
    cv2.imwrite(Image_file+"/Hand_"+str(valueR)+".jpg",pictureR)

    tree = etree.parse(Xml_file+"/"+image.split(".")[0]+".xml")
    objects=[]
    objectsV=[]
    objectsH=[]
    objectsR=[]
    for object in tree.xpath("/annotation/object"):
        objects.append(object.xpath("name")[0].text)
        objectsH.append(object.xpath("name")[0].text)
        objectsV.append(object.xpath("name")[0].text)
        objectsR.append(object.xpath("name")[0].text)

        for coords in object.xpath("bndbox"):
            objects.append(int(coords[0].text))
            objects.append(int(coords[1].text))
            objects.append(int(coords[2].text))
            objects.append(int(coords[3].text))

            objectsH.append(cols-int(coords[0].text))
            objectsH.append(int(coords[1].text))
            objectsH.append(cols-int(coords[2].text))
            objectsH.append(int(coords[3].text))

            objectsV.append(int(coords[0].text))
            objectsV.append(rows-int(coords[1].text))
            objectsV.append(int(coords[2].text))
            objectsV.append(rows-int(coords[3].text))

            objectsR.append(cols-int(coords[0].text))
            objectsR.append(rows-int(coords[1].text))
            objectsR.append(cols-int(coords[2].text))
            objectsR.append(rows-int(coords[3].text))

    pathH = os.path.abspath(Image_file + "/" + "Hand_"+str(valueH)+".jpg")
    pathV = os.path.abspath(Image_file + "/" + "Hand_"+str(valueV)+".jpg")
    pathR = os.path.abspath(Image_file + "/" + "Hand_"+str(valueR)+".jpg")

    xmlH = writexml.writeXML(Image_file, "Hand_"+str(valueH)+".jpg", pathH, 512, 424, 3, objectsH)
    xmlV = writexml.writeXML(Image_file, "Hand_"+str(valueV)+".jpg", pathV, 512, 424, 3, objectsV)
    xmlR = writexml.writeXML(Image_file, "Hand_"+str(valueR)+".jpg", pathR, 512, 424, 3, objectsR)

    with open(Xml_file + "/" + "Hand_"+str(valueH) + ".xml", "w") as file:
        file.write(xmlH)
    with open(Xml_file + "/" + "Hand_"+str(valueV) + ".xml", "w") as file:
        file.write(xmlV)
    with open(Xml_file + "/" + "Hand_"+str(valueR) + ".xml", "w") as file:
        file.write(xmlR)

    for i in range(len(objects) // 5):
        if objects[i * 5] == 'hand':
            cv2.rectangle(picture,(int(objects[i * 5 + 1]), int(objects[i * 5 + 2])), (int(objects[i * 5 + 3]), int(objects[i * 5 + 4])),(0,255,0))
        elif objects[i * 5] == 'fist':
            cv2.rectangle(picture,(int(objects[i * 5 + 1]), int(objects[i * 5 + 2])), (int(objects[i * 5 + 3]), int(objects[i * 5 + 4])),(0,0,255))
        else:
            cv2.rectangle(picture,(int(objects[i * 5 + 1]), int(objects[i * 5 + 2])), (int(objects[i * 5 + 3]), int(objects[i * 5 + 4])),(255,0,0))

    for i in range(len(objectsH) // 5):
        if objectsH[i * 5] == 'hand':
            cv2.rectangle(reversedH,(int(objectsH[i * 5 + 1]), int(objectsH[i * 5 + 2])), (int(objectsH[i * 5 + 3]), int(objectsH[i * 5 + 4])),(0,255,0))
        elif objectsH[i * 5] == 'fist':
            cv2.rectangle(reversedH,(int(objectsH[i * 5 + 1]), int(objectsH[i * 5 + 2])), (int(objectsH[i * 5 + 3]), int(objectsH[i * 5 + 4])),(0,0,255))
        else:
            cv2.rectangle(reversedH,(int(objectsH[i * 5 + 1]), int(objectsH[i * 5 + 2])), (int(objectsH[i * 5 + 3]), int(objectsH[i * 5 + 4])),(255,0,0))

    for i in range(len(objectsV) // 5):
        if objectsV[i * 5] == 'hand':
            cv2.rectangle(reversedV,(int(objectsV[i * 5 + 1]), int(objectsV[i * 5 + 2])), (int(objectsV[i * 5 + 3]), int(objectsV[i * 5 + 4])),(0,255,0))
        elif objectsV[i * 5] == 'fist':
            cv2.rectangle(reversedV,(int(objectsV[i * 5 + 1]), int(objectsV[i * 5 + 2])), (int(objectsV[i * 5 + 3]), int(objectsV[i * 5 + 4])),(0,0,255))
        else:
            cv2.rectangle(reversedV,(int(objectsV[i * 5 + 1]), int(objectsV[i * 5 + 2])), (int(objectsV[i * 5 + 3]), int(objectsV[i * 5 + 4])),(255,0,0))

    for i in range(len(objectsR) // 5):
        if objectsR[i * 5] == 'hand':
            cv2.rectangle(pictureR,(int(objectsR[i * 5 + 1]), int(objectsR[i * 5 + 2])), (int(objectsR[i * 5 + 3]), int(objectsR[i * 5 + 4])),(0,255,0))
        elif objectsR[i * 5] == 'fist':
            cv2.rectangle(pictureR,(int(objectsR[i * 5 + 1]), int(objectsR[i * 5 + 2])), (int(objectsR[i * 5 + 3]), int(objectsR[i * 5 + 4])),(0,0,255))
        else:
            cv2.rectangle(pictureR,(int(objectsR[i * 5 + 1]), int(objectsR[i * 5 + 2])), (int(objectsR[i * 5 + 3]), int(objectsR[i * 5 + 4])),(255,0,0))

    cv2.imshow("original",picture)
    cv2.imshow("H_flip",reversedH)
    cv2.imshow("V_flip",reversedV)
    cv2.imshow("rotated",pictureR)

    time.sleep(1/25)
    if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
        break
