import segmentimg as simg

# Example use if segmentimg
def with_sito():
    img.hist_equal_all(on='rescaled_dict')
    img.save_hist_equal_all(r"\backup2\histeq")

    img.bilateral_all(on='hist_equal_dict')
    img.save_bilateral_all(r"\backup2\bilateral")

    img.thresh_green_chan_all(on='bilateral_dict')
    img.save_thresh_green_chan_all(r"\backup2\thresh green")

    img.masked_all(on='thresh_inv_green')
    img.save_masked_all(r"\backup2\masked with sito")

def with_no_sito():
    img.bilateral_all(on='rescaled_dict')
    img.save_bilateral_all(r"\backup2\bilateral no sito")
    
    img.thresh_gray_all(on='bilateral_dict')
    img.save_thresh_gray(r"\backup2\thresh gray")

    img.masked_all(on='thresh_inv_gray')
    img.save_masked_all(r"\backup2\masked with no sito")

img = simg.segmentImg(r"C:\Users\Mahatma Ageng Wisesa\Desktop\OpenCV", "test")
img.read_all_img()

img.rescale_all()
img.save_rescaled_all(r"\backup2\rescale")

with_sito()
with_no_sito()