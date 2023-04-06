# Image Search

This project is a Python implementation of an image search engine that allows users to search for images containing a given search term and display all related images in a contact sheet. The project relies on several techniques such as image processing, optical character recognition (OCR), and object detection. The main objective of the project was to develop an image search engine that could find images containing a given search term and display all related images in a contact sheet. Additionally, the project was able to detect faces in the related images and generate a contact sheet of all faces found in the images. Finally, the project was able to serialize and deserialize Python objects in and out of files using the pickle library.

## Getting Started

To run this project, you will need to have Python 3.x and the following Python modules installed:

-   pytesseract
-   OpenCv
-   PIL

Once you have the required modules installed, you can download or clone the project code to your local machine.

## Usage

To search for images containing a given keyword, run the `main.py` script and enter the keyword.

The program will search for matching images in the `small_img.zip` file and display any detected faces in the matching images. If no faces are detected, the program will print a message indicating this.

Note that if you have already searched for a keyword before, the program will retrieve the results from a cached dictionary to save time.

## Important Files

-   `main.py`: contains the `search()` function that accepts a user input and searches for matching images, and calls the `detectfaces()` function to detect faces in any matching images.
-   `image_searcher.py`: contains the `detectfaces()` function that takes an image and uses OpenCV to detect any faces in it.
-   `readonly/`: contains the image data and the `haarcascade_frontalface_default.xml` file used by OpenCV for face detection.
