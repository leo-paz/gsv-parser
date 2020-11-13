import os
from coco_assistant import COCO_Assistant

annotationDir = "C:\\Users\\omarl\\Desktop\\FourthYearProject\\data\\train\\trainAnnotations\\COCO\\Final"
imageDir = "C:\\Users\\omarl\\Desktop\\FourthYearProject\\data\\train\\trainAnnotations\\COCO\\Images"

ann_dir = os.path.join(os.getcwd(), annotationDir)
img_dir = os.path.join(os.getcwd(), imageDir)
cas = COCO_Assistant(img_dir, ann_dir)

cas.merge(merge_images=False)