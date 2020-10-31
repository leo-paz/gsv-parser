import json
import os
from shutil import copy

imagesToCopyFrom = 'C:\\Users\\omarl\\Desktop\\FourthYearProject\\train\\trainImages\\'
directoryToPasteImages = 'C:\\Users\\omarl\\Desktop\\FourthYearProject\\validationImages'
annotationsJsonPath = 'C:\\Users\\omarl\\Desktop\\FourthYearProject\\train\\trainAnnotations\\trainCOCO.json'
validationAnnotationsPath = 'C:\\Users\\omarl\\Desktop\\FourthYearProject\\validationAnnotations\\trainCOCO.json'

main = open(validationAnnotationsPath)
main = json.load(main)

file = open(annotationsJsonPath)
file = json.load(file)

annotatedPictures = [] # So python treats this as a set

main['images'] = []
main['annotations'] = []

for i in range(400):

    main['images'].append(file['images'][i])
    main['annotations'].append(file['annotations'][i])

    annotatedPictures.append(file['images'][i]['file_name'])

for i in range(len(annotatedPictures)):
    copy(imagesToCopyFrom+annotatedPictures[i], directoryToPasteImages)

with open('C:\\Users\\omarl\\Desktop\\FourthYearProject\\validationAnnotations\\valCOCO.json', 'w') as outfile:
    json.dump(main, outfile)