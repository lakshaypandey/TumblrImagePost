
import exifread
import time
from PIL import Image
from fractions import Fraction
from PIL.ExifTags import TAGS

#Parameters Being read declared here for ease of reference
LensModel=''
Flash=0
Time=''
FNumber=''
ApertureValue=''
FocalLength=''
ISOSpeedRatings=''
CameraModel=''
ExposureTime=''
EffFocalLength=''


def read_image(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


#Reading the File from exifread to read LensModel from exifread
def read_lensmodel(filename):
    f = open(filename, 'rb')
    tags=exifread.process_file(f)
    try:
        lensModel =tags['EXIF LensModel']
    except Exception as e:
        lensModel=None
    try:
        efec_Focal_Length=tags['EXIF FocalLengthIn35mmFilm']
    except Exception as e:
        efec_Focal_Length=None
    return lensModel,efec_Focal_Length

def get_exif_string(filename,time_flag=False):
    exif_string = ''
    exif_values= read_image(filename)
    LensModel,EffFocalLength = read_lensmodel(filename)
    if 'DateTimeOriginal' in exif_values:
        Time = time.strptime( exif_values['DateTimeOriginal'],"%Y:%m:%d %H:%M:%S")
        Frmt_Time= time.strftime("%d-%m-%Y %H:%M", Time)
        exif_string = 'Taken on %s'%(str(Frmt_Time))
    else:
        exif_string = 'Taken'
    if 'Model' in exif_values:
        CameraModel = exif_values['Model']
        exif_string = '%s using a %s'% (exif_string,str(CameraModel))
        if not LensModel==None:
            exif_string = '%s with a %s lens'% (exif_string,str(LensModel))

    if 'FocalLength' in exif_values.keys():
        FocalLength = str(exif_values['FocalLength'][0]/exif_values['FocalLength'][1])
        exif_string = '%s at %smm'% (exif_string,FocalLength)
        if not EffFocalLength==None:
            exif_string = '%s equivalent to %smm for 35mm film'% (exif_string,EffFocalLength)


    if 'FNumber' in exif_values.keys():
        FNumber = 'f/' + str('{0:g}'.format(exif_values['FNumber'][0]/float(exif_values['FNumber'][1])))
        Flag=True
        exif_string = '%s with settings at %s'% (exif_string,FNumber)
    else:
        Flag=False
        exif_string = '%s with settings at'% (exif_string)
    if 'ISOSpeedRatings' in exif_values.keys():
        ISOSpeedRatings = str(exif_values['ISOSpeedRatings'])
        exif_string = '%s ISO %s'% (exif_string,ISOSpeedRatings)
        Flag=True
    if 'ExposureTime' in exif_values.keys():
        ExposureTime = str(Fraction(exif_values['ExposureTime'][0],exif_values['ExposureTime'][1]))
        exif_string = '%s %s sec'% (exif_string,ExposureTime)
        Flag=True
    if 'Flash' in exif_values.keys():
        if not Flag:
            exif_string=exif_string[:-17]
            Flag=True
        Flash = '' if exif_values['Flash']==0 else 'with Flash'
        exif_string = '%s %s'% (exif_string,Flash)
    if not Flag:
        exif_string=exif_string[:-17]
        Flag=True

    if 'ApertureValue' in exif_values.keys():
        ApertureValue = exif_values['ApertureValue']
    if 'MaxApertureValue' in exif_values.keys():
        MaxApertureValue = exif_values['MaxApertureValue']

    ##Formatting the exif string here
    if time_flag:
        return exif_string,exif_values['DateTimeOriginal']
    else:
        return exif_string
