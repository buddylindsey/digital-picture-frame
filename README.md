# digital-picture-frame
digital-picture-frame is a PyQt5 application meant to be multi-platform specifically to turn your monitor into a picture frame of images. Either on a raspberry-pi and 5 inch monitor in your house, or on a big 4k monitor in your photography studio.

![Screenshot](https://raw.githubusercontent.com/buddylindsey/digital-picture-frame/gh-pages/images/digital-picture-frame1.png)

## Running and Development

Since this project is still under fairly heavy development you will need to treat running as such. Here are the steps on my Mac and Linux machine.

### Project Requirements

    * Python - 3.4+
    * PyQt5 - 5.7+

### Setup
```
$ virtualenv ~/.virtualenv/digital-frame
$ source ~/.virtualenv/digital-frame/bin/activate
$ git clone https://github.com/buddylindsey/digital-picture-frame.git
$ cd digital-picture-frame
$ pip install -r requirements.txt
$ python image.py
```

### How it Works
Biggest thing to note is once you are running the project you will need to set settings of where your images are. Then you can hit `ctrl+r` to start your slide show, or use the menu.

## Contributing
If you would like to contribute that would be AMAZING. Please fork the repo and follow the steps above. Then submit a PR here.
