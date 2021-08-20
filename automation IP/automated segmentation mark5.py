import cv2 as cv
import os

class segmentImg:
    """Image segmentation for Acute Lymphoblastic Leukemia L1
       Credits: Mahatma Wisesa

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
        self.img_names = [] # nama file yg ada di folder
        
        self.img_dict = {} # masih ada ".jpg" --> gambar original
        self.img_dict_rescaled = {} # rescaled img
        self.img_hist_eq_dict = {} # histogram equalization img
        self.img_bilateral_dict = {}
        self.thresh_inv_hist = {}
        self.img_masked = {}

    def get_img_dict(self):
        """
        Returns
        ------------
        self.img_dict : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                        Dictionary of images with their original names.
        """
        return self.img_dict

    def get_img_dict_rescaled(self):
        """
        Returns
        ------------
        self.img_dict_rescaled : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                                 Dictionary of rescaled images with their original names.
        """
        return self.img_dict_rescaled

    def get_img_hist_eq_dict(self):
        """
        Returns
        ------------
        self.img_hist_eq_dict : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                                Dictionary of hist equalization images with their original names.
        """
        return self.img_hist_eq_dict

    def get_bilateral_dict(self):
        """
        Returns
        ------------
        self.img_bilateral_dict : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                                  Dictionary of bilateral blur images with their original names.
        """
        return self.img_bilateral_dict

    def read_all_img(self):
        """Create dictionary of images.
        """
        self.img_names = [img_name for img_name in os.listdir(self.child)]
        self.img_dict = {
            img_name:cv.imread(self.child+f"\\{img_name}") for img_name in self.img_names
            }
            
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
            img_name = img_name.replace(".jpg", "")
            self.img_dict_rescaled[img_name] = rescale(img, scale)

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
        print("Everything is OK.")

    def hist_equal_all(self, where='rescaled_dict'):
        """Histogram equalization.
        
        Parameters
        ------------
        rescale : bool
                  If true use self.img_dict_rescaled, else use self.img_dict 
                  original image stil need update.
        """
        def hist_equal(read_dict):
            count = 1
            for img_name, img in read_dict.items():
                img_name = img_name.replace(".jpg", "")
                self.img_hist_eq_dict[img_name] = cv.cvtColor(img, cv.COLOR_BGR2YUV)
                self.img_hist_eq_dict[img_name][:,:,0] = cv.equalizeHist(self.img_hist_eq_dict[img_name][:,:,0])
                self.img_hist_eq_dict[img_name] = cv.cvtColor(self.img_hist_eq_dict[img_name], cv.COLOR_YUV2BGR)
                print(f'Hist Equal Processed: {count}/{len(read_dict.items())}')
                count += 1

        if where == 'rescaled_dict':
            # make rescaled
            hist_equal(self.img_dict_rescaled)
        elif where == 'org_dict':
            # make gambar ori
            hist_equal(self.img_dict)

    def save_hist_equal_all(self, saved_folder):
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
        print("Everything is OK.")

    def bilateral_all(self, where='org_dict'):
        """Histogram equalization.
        
        Parameters
        ------------
        where : str
                'hist_equal_dict' iterate over self.img_hist_eq_dict
                'rescaled_dict' iterate over self.img_dict_rescaled
                'org_dict' iterate over self.img_dict
        """
        def bilateralFilter(read_dict):
            count = 1
            for img_name, img in read_dict.items():
                self.img_bilateral_dict[img_name] = cv.bilateralFilter(img, 25, 75, 75) #cv.bilateralFilter(img, 10, 50, 50)
                print(f'Bilateral Filter Processed: {count}/{len(read_dict.items())}')
                count += 1

        if where == 'hist_equal_dict':
            bilateralFilter(self.img_hist_eq_dict)
        elif where == 'rescaled_dict':
            bilateralFilter(self.img_dict_rescaled)
        elif where == 'org_dict':
            bilateralFilter(self.img_dict)

    def save_bilateral_all(self, saved_folder):
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
        print("Everything is OK.")

    def thresh_green_chan_all(self, where='org_dict'):

        def thresh_green_chan(read_dict):
            count = 1
            for img_name, img in read_dict.items():
                b, g, r = cv.split(img)
                ret, thresh_inv_hist = cv.threshold(g, 100, 255, cv.THRESH_BINARY_INV)
                self.thresh_inv_hist[img_name] = thresh_inv_hist
                print(f'Green Thresh Processed: {count}/{len(read_dict.items())}')
                count += 1

        if where == 'hist_equal_dict':
            thresh_green_chan(self.img_hist_eq_dict)
        elif where == 'rescaled_dict':
            thresh_green_chan(self.img_dict_rescaled)
        elif where == 'org_dict':
            thresh_green_chan(self.img_dict)
        elif where == 'bilateral_dict':
            thresh_green_chan(self.img_bilateral_dict)

    def save_thresh_green_chan_all(self, saved_folder):
        os.chdir(self.ROOT_DIR+f"\\{saved_folder}")
        for img_name, img in self.thresh_inv_hist.items():
            cv.imwrite(f"{img_name} (thresh).jpg", img)
        print("Image saved.")
        os.chdir(self.ROOT_DIR)
        print("Back to ROOT_DIR")
        print("Everything is OK.")

    def masked_all(self, where='org_dict'):
        def masked(read_dict):
            count = 1
            for img_name, img in read_dict.items():
                masked_hist = cv.bitwise_and(
                    self.img_dict_rescaled[img_name], self.img_dict_rescaled[img_name], mask=img
                    )
                self.img_masked[img_name] = masked_hist
                print(f'Masked Processed: {count}/{len(read_dict.items())}')
                count += 1

        if where == 'hist_equal_dict':
            masked(self.img_hist_eq_dict)
        elif where == 'rescaled_dict':
            masked(self.img_dict_rescaled)
        elif where == 'org_dict':
            masked(self.img_dict)
        elif where == 'bilateral_dict':
            masked(self.img_bilateral_dict)
        elif where == 'thresh_dict':
            masked(self.thresh_inv_hist)
            # masked(self.img_masked)

    def save_masked(self, saved_folder):
        os.chdir(self.ROOT_DIR+f"\\{saved_folder}")
        for img_name, img in self.img_masked.items():
            cv.imwrite(f"{img_name} (masked).jpg", img)
        print("Image saved.")
        os.chdir(self.ROOT_DIR)
        print("Back to ROOT_DIR")
        print("Everything is OK.")


img = segmentImg(r"C:\Users\Mahatma Ageng Wisesa\Desktop\OpenCV", "test")
img.read_all_img()

img.rescale_all()
img.save_rescaled_all("rescale")

img.hist_equal_all(where='rescaled_dict')
img.save_hist_equal_all("histeq")

img.bilateral_all(where='hist_equal_dict')
img.save_bilateral_all('bilateral')

img.thresh_green_chan_all(where='bilateral_dict')
img.save_thresh_green_chan_all("thresh")

img.masked_all(where='thresh_dict')
img.save_masked("masked")
# print("thresh_inv_hist", img.thresh_inv_hist.keys())
# print("img_dict_rescaled", img.img_dict_rescaled.keys())