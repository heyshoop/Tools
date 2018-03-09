#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/26
# @File    : GreenHat.py
# @Des     : 码如其名

from PIL import Image
import face_recognition

img_path = './someOne.JPG'

image = face_recognition.load_image_file(img_path)
face_locations = face_recognition.face_locations(image)
print("图片中共发现{}张脸.".format(len(face_locations)))

human_img = Image.open(img_path)
human_img = human_img.convert("RGBA")

hat_img = Image.open("./hat.png")
hat_img = hat_img.convert("RGBA")

for face_location in face_locations:
    top, right, bottom, left = face_location
    print("面部位于图片位置 顶: {}, 左: {}, 底: {}, 右: {}".format(top, left, bottom, right))
    head_h = bottom - top
    head_l = right - left

    hat_img = hat_img.resize((head_l, head_h))
    hat_region = hat_img
    human_region = (left, top - head_h, right, top)
    human_img.paste(hat_region, human_region, mask=hat_img)

human_img.show()

