import json
import os

path = 'C:\\Users\\omarl\\Desktop\\FourthYearProject\\trainAnnotations\\COCO\\5th-set-COCO.json'

file = open(path)
file = json.load(file)

mapping = {2:1, 1:2, 3:3, 4:4, 5:5}
    
for i in range(len(file['annotations'])):
    currentId = file['annotations'][i]['category_id']
    file['annotations'][i]['category_id'] = mapping[currentId]

with open('C:\\Users\\omarl\\Desktop\\FourthYearProject\\trainAnnotations\\COCO\\5th-set-COCO-Mapped.json', 'w') as outfile:
    json.dump(file, outfile)
