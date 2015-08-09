import os
import sys
import yaml

import read_exif as exif
from get_oauth import new_oauth
from operator import itemgetter
from pytumblr import TumblrRestClient


if __name__ == '__main__':
    BatchProcess=False
    SortByTime=False
    State='draft'
    FileColumnSeparator= '|'
    FileTagsSeparator= ','
    BlogName = 'photoblog.lakshaypandey.com'
    if len(sys.argv)>1:
        if 'batch' in sys.argv:
            BatchProcess=True
        if 'sort' in sys.argv:
            SortByTime=True
        if 'published' in sys.argv:
            State='published'
        elif 'private' in sys.argv:
            State='private'
        elif 'draft' in sys.argv:
            State='draft'

    print State

    Image_Folder =os.path.join(os.getcwd(),'Images')

    #Get Consumer key and secret from Tumblr_Keys
    Keys = eval(open('Tumblr_Keys','r').read())


    #Generate Oauth tokens. Taken from interactive_console.py in pytumblr
    yaml_path = os.path.expanduser('~') + '/.tumblr'

    if not os.path.exists(yaml_path):
        tokens = new_oauth(yaml_path,Keys['consumer_key'],Keys['consumer_secret'],)
    else:
        yaml_file = open(yaml_path, "r")
        tokens = yaml.safe_load(yaml_file)
        yaml_file.close()

    client = TumblrRestClient(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )


    #print client.info()


    #Read Captions, List of Files
    fout  = open ('Captions.csv','r')
    data = fout.readlines()
    fout.close()

    ImageList=[]
    if not SortByTime:
        for i in data[1:]:
            ImagePath=os.path.join(Image_Folder,i.split(FileColumnSeparator)[0])
            Caption = i.split(FileColumnSeparator)[1] + '\n' + exif.get_exif_string(ImagePath)
            Tags=i.split(FileColumnSeparator)[2].split(FileTagsSeparator)
            #Image_Block =
            ImageList.append({'Path' : ImagePath, 'Caption' : Caption ,'Tags' : Tags})
    else:
        for i in data[1:]:
            ImagePath=os.path.join(Image_Folder,i.split(FileColumnSeparator)[0])
            Exif = exif.get_exif_string(ImagePath,True)
            Caption = i.split(FileColumnSeparator)[1] + '\n' + Exif[0]
            Tags=i.split(FileColumnSeparator)[2].split(FileTagsSeparator)
            #Image_Block =
            ImageList.append([Exif[1],{'Path' : ImagePath, 'Caption' :Caption,'Tags' : Tags }])
        ImageList = sorted(ImageList, key=itemgetter(0))
        temp=[]
        for i in ImageList:
            temp.append(i[1])
        ImageList=temp
    #print client.blog_info('photoblog.lakshaypandey.com')
    for i in ImageList:
        print 'Posting : ', i['Path']
        print 'Caption : ', i['Caption']
        print 'Tags : ' , i['Tags']
        if not BatchProcess:
            raw_input("Press Enter to Continue")
        #client.create_photo(Keys['blogname'], state="draft", tags=i['Tags'],  data=i['Path'],caption =i['Caption'])
        print 'Done for ',i['Path']
        print '-'*30
