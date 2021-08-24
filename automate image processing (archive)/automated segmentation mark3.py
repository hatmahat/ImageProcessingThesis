import cv2 as cv
import os

class segmentIMG:
    """Image segmentation.

    Parameters
    ------------
    ROOT_DIR : str
               Root directory.
    child : str
            Raw images folder directory.
    """
    def __init__(self, ROOT_DIR, child):
        self.ROOT_DIR = ROOT_DIR
        self.child = self.ROOT_DIR+f"\\{child}"
        self.img_names = []
        self.img_dict = {}
        self.img_dict_rescaled = {}

    def read_img(self):
        """Create dictionary of images.

        Returns
        ------------
        self.img_names : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                         Dictionary of images with their names.
        """
        for img_name in os.listdir(self.child):
            self.img_names.append(img_name)

        for img_name in self.img_names:
            self.img_dict[img_name] = cv.imread(self.child+f"\\{img_name}")
        return self.img_dict

    def rescale(self, frame, scale=0.2):
        """Rescale images (inner use only).

        Parameters
        ------------
        frame : <class 'numpy.ndarray'> 
                Image in cv.imread
        scale : float 
                Rescale image from 0 to 1 times.

        Returns
        ------------
        cv.resize() : <class 'numpy.ndarray'>
        """
        width = int(frame.shape[1]*scale)
        height = int(frame.shape[0]*scale)
        dimensions = (width, height)
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    def rescale_all(self, scale=0.2):
        """Rescale all images in self.img_dict

        Parameters
        ------------
        scale : float 
                Rescale image from 0 to 1 times.
        """
        for img_name, img in self.img_dict.items(): # karena ada ".jpg" di nama makannya -4
            self.img_dict_rescaled[img_name[:-4]+" (rescaled)"] = self.rescale(img, scale)

    def save_rescaled_imges(self, saved_folder):
        """Save images from img_dict_rescaled to the "saved_folder" folder.

        Parameters
        ------------
        saved_folder : str
                       Name of the new folder where images will be saved.
        """
        os.chdir(self.ROOT_DIR+f"\\{saved_folder}")
        for img_name, img in self.img_dict_rescaled.items():
            cv.imwrite(f"{img_name}.jpg", img)
        print("Image saved.")
        os.chdir(self.ROOT_DIR)
        print("Back to ROOT_DIR")

img = segmentIMG(r"C:\Users\Mahatma Ageng Wisesa\Desktop\OpenCV", "test")
img.read_img()
img.rescale_all()
img.save_rescaled_imges("saved")
print(img.img_dict.keys())