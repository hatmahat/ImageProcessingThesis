import cv2 as cv
import os

class segmentImg:
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
        self.img_dict_rescaled = {} # rescaled img
        self.img_hist_eq_dict = {} # histogram equalization img
        self.img_bilateral_dict = {}

    def get_img_dict(self):
        """
        Returns
        ------------
        self.img_names : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                         Dictionary of images with their names.
        """
        return self.img_dict

    def get_img_dict_rescaled(self):
        return self.img_dict_rescaled

    def get_img_hist_eq_dict(self):
        return self.img_hist_eq_dict

    def get_bilateral_dict(self):
        return self.img_bilateral_dict

    def read_all_img(self):
        """Create dictionary of images.
        """
        for img_name in os.listdir(self.child):
            self.img_names.append(img_name)
        for img_name in self.img_names:
            self.img_dict[img_name] = cv.imread(self.child+f"\\{img_name}")
            
    def rescale_all(self, scale=0.2):
        """Rescale all images in self.img_dict

        Parameters
        ------------
        scale : float 
                Rescale image from 0 to 1 times.
        """
        def rescale(frame, scale):
            width = int(frame.shape[1]*scale)
            height = int(frame.shape[0]*scale)
            dimensions = (width, height)
            return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

        for img_name, img in self.img_dict.items(): # karena ada ".jpg" di nama makannya -4
            self.img_dict_rescaled[img_name[:-4]] = rescale(img, scale)

    def save_rescaled_all(self, saved_folder):
        """Save images from img_dict_rescaled to the "saved_folder" folder.

        Parameters
        ------------
        saved_folder : str
                       Name of the new folder where images will be saved.
        """
        os.chdir(self.ROOT_DIR+f"\\{saved_folder}")
        for img_name, img in self.img_dict_rescaled.items():
            cv.imwrite(f"{img_name} (rescaled).jpg", img)
        print("Image saved.")
        os.chdir(self.ROOT_DIR)
        print("Back to ROOT_DIR")

    def hist_equal_all(self, where='rescaled_dict'):
        """Histogram equalization.
        
        Parameters
        ------------
        rescale : bool
                  If true use self.img_dict_rescaled, else use self.img_dict 
                  original image stil need update.
        """
        def hist_equal():
            self.img_hist_eq_dict[img_name] = cv.cvtColor(img, cv.COLOR_BGR2YUV)
            self.img_hist_eq_dict[img_name][:,:,0] = cv.equalizeHist(self.img_hist_eq_dict[img_name][:,:,0])
            self.img_hist_eq_dict[img_name] = cv.cvtColor(self.img_hist_eq_dict[img_name], cv.COLOR_YUV2BGR)

        if where == 'rescaled_dict':
            # make rescaled
            for img_name, img in self.img_dict_rescaled.items():
                hist_equal()
        else:
            # make original (masih perlu perbaikan)
            for img_name, img in self.img_dict.items():
                hist_equal()

    def save_hist_equal(self, saved_folder):
        """Save images from img_hist_eq_dict to the "saved_folder" folder.

        Parameters
        ------------
        saved_folder : str
                       Name of the new folder where images will be saved.
        """
        os.chdir(self.ROOT_DIR+f"\\{saved_folder}")
        for img_name, img in self.img_hist_eq_dict.items():
            cv.imwrite(f"{img_name} (Hist Equal).jpg", img)
        print("Image saved.")
        os.chdir(self.ROOT_DIR)
        print("Back to ROOT_DIR")

    def bilateral(self, where='org_dict'):
        """Histogram equalization.
        
        Parameters
        ------------
        where : str
                'hist_equal_dict' iterate over self.img_hist_eq_dict
                'rescaled_dict' iterate over self.img_dict_rescaled
                'org_dict' iterate over self.img_dict
        """
        def bilateralFilter():
            self.img_bilateral_dict[img_name] = cv.bilateralFilter(img, 10, 50, 50)

        count = 1
        if where == 'hist_equal_dict':
            for img_name, img in self.img_hist_eq_dict.items():
                bilateralFilter()
                print(f'{count}/{len(self.img_hist_eq_dict.items())}')
                count += 1
        elif where == 'rescaled_dict':
            for img_name, img in self.img_dict_rescaled.items():
                bilateralFilter()
                print(f'{count}/{len(self.img_dict_rescaled.items())}')
                count += 1
        elif where == 'org_dict':
            for img_name, img in self.img_dict.times():
                bilateralFilter()
                print(f'{count}/{len(self.img_dict.items())}')
                count += 1

    def save_bilateral(self, saved_folder):
        """Save images from img_bilateral_dict to the "saved_folder" folder.

        Parameters
        ------------
        saved_folder : str
                       Name of the new folder where images will be saved.
        """
        os.chdir(self.ROOT_DIR+f"\\{saved_folder}")
        for img_name, img in self.img_bilateral_dict.items():
            cv.imwrite(f"{img_name} (bilateral blur).jpg", img)
        print("Image saved.")
        os.chdir(self.ROOT_DIR)
        print("Back to ROOT_DIR")

img = segmentImg(r"C:\Users\Mahatma Ageng Wisesa\Desktop\OpenCV", "test")
img.read_all_img()
img.rescale_all()
#img.save_rescaled_all("saved")
img.hist_equal_all(where='rescaled_dict')
# img.save_hist_equal("saved")
img.bilateral(where='hist_equal_dict')
img.save_bilateral('bilateral')
print(img.img_hist_eq_dict.keys())