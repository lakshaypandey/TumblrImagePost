# TumblrImagePost
Script to post images to photo posts to tumblr with Exif data.

#### Dependencies
```python
pip install -r --upgrade requirements.txt
```
You would need python pip for this.

####Images
Put all of the images in the Images folder.
Then add the filenames, captions and tags to the Captions.csv file.

Filename|Caption|Tags

All of them need to be added but can be left blank.

####API Oauth
Create a file named Tumblr_Keys
Add your tumblr consumer key and consumer secret and blog path to Tumblr_Keys
```shell
{'consumer_secret': 'Enter Consumer Secret Key here', 'consumer_key': 'Enter Consumer Key Here' , 'blogname' : 'blogname here'}
```
Blog path is the url or your blog or the custom url if you have one

####Running the script

```shell
    python tumblr_post.py sort batch draft
```
3 optional parameters here
sort, batch and state

* **sort** :  sorts the images based on their Time
* **batch** :  process all the images without it asks for key press for every Images
* **state** : defines the state of the post when posted
* should be on of **published private draft** default is set to draft
