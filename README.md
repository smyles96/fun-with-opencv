## Fun with OpenCV

#### Motivation

I wanted to learn the basics of OpenCV, so I created a script to dynamically apply filters to a webcam stream.

Filters/Recognition include:
* Grayscale
* Subtractors
* Canny
* Gaussian Blur
* Facial Recognition
* Image pasting over faces (pastes the GITS laughing man logo)

#### Installing & Usage

1) Clone this repo
2) Run `pip install -r requirements.txt`
3) Plug in a webcam
4) Run `python main.py`
5) Apply filters or quit by pressing the following keys:
    > Pressing `q` : Quits the program
    > Pressing `s` : Activate/Deactivate the Subtractor filter
    > Pressing `c` : Activate/Deactivate the Canny filter
    > Pressing `g` : Activate/Deactivate the Gaussian Blur filter
    > Pressing `z` : Activate/Deactivate the Grayscale filter
    > Pressing `r` : Activate/Deactivate facial recognition
    > Pressing `l` : Activate/Deactivate the Laughing Man face paste

**Note: To use the laughing man filter, the recognizer filter must be active**