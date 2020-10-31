import json
import os

imagesToCleanPath = 'C:\\Users\\omarl\\Desktop\\FourthYearProject\\trainImages\\'
annotationsJsonPath = 'C:\\Users\\omarl\\Desktop\\FourthYearProject\\trainAnnotations\\trainCOCO.json'

entries = os.listdir(imagesToCleanPath)
entries.sort()

annotatedPictures = {'placeholder'} # So python treats this as a set

file = open(annotationsJsonPath)
file = json.load(file)
    
for i in range(len(file['images'])):
    annotatedPictures.add(file['images'][i]['file_name'])

for entry in entries:
    if entry not in annotatedPictures:
        os.remove(imagesToCleanPath+entry)

