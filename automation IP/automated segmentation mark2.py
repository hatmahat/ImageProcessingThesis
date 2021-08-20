import cv2 as cv
import os

class segmentIMG:
    def __init__(self, ROOT_DIR):
        self.ROOT_DIR = ROOT_DIR
        self.img_names = []
        self.img_dict = {}
        self.img_dict_rescaled = {}

    def to_child(self, child):
        """String to child dir of ROOT_DIR
        Parameters
        ------------
        child : {string}, "name child dir of ROOT_DIR"

        Returns
        ------------
        {string}
        """
        return self.ROOT_DIR+f"\\{child}"
        
    # def img_list(self, child):
    #     """Read file names in child folder.
    #     Parameters
    #     ------------
    #     child : {string}, "sample folder"
    #             the name of the folder containing the images

    #     Returns
    #     ------------
    #     self.img_names : {list}
    #                      list of image file names.
    #     """
    #     for img_name in os.listdir(self.to_child(child)):
    #         self.img_names.append(img_name)
    #     return self.img_names

    def read_img(self, child):
        """Create dictionary of images.
        Parameters
        ------------
        child : {string}, "sample folder"

        Returns
        ------------
        self.img_names : {dict}, {"IMG_NAME": <class 'numpy.ndarray'>}
                         dictionary of images.
        """
        for img_name in os.listdir(self.to_child(child)):
            self.img_names.append(img_name)

        for img_name in self.img_names:
            self.img_dict[img_name] = cv.imread(self.to_child(child)+f"\\{img_name}")
        return self.img_dict

    def rescale(self, frame, scale=0.2):
        """Rescale images.
        Parameters
        ------------
        frame : {<class 'numpy.ndarray'>}, image in cv.imread

        Returns
        ------------
        cv.resize() : {<class 'numpy.ndarray'>}
                      numpy.ndarray object
        """
        width = int(frame.shape[1]*scale)
        height = int(frame.shape[0]*scale)
        dimensions = (width, height)
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    def rescale_all(self):
        """Rescale all images in self.img_dict
        Returns
        ------------
        self.img_dict_rescaled : {dictionary}, {"IMG_NAME (rescaled)": <class 'numpy.ndarray'>}
        """
        for img_name, img in self.img_dict.items():
            self.img_dict_rescaled[img_name+" (rescaled)"] = self.rescale(img)
        return self.img_dict_rescaled

    def save_rescaled_imges(self, child):
        """Save images from img_dict_rescaled to the "child" folder.
        Parameters
        ------------
        child : {string}, name of the new folder
        """
        os.chdir(self.to_child(child))
        for img_name, img in self.img_dict_rescaled.items():
            cv.imwrite(f"{img_name}.jpg", img)
        print("Image saved.")
        os.chdir(self.ROOT_DIR)
        print("Back to ROOT_DIR")

img = segmentIMG(r"C:\Users\Mahatma Ageng Wisesa\Desktop\OpenCV")
# img_names = img.img_list("test")
img.read_img("test") 
img_rescale = img.rescale_all()
img.save_rescaled_imges("saved")