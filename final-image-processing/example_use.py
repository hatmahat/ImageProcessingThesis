import segmentimg as simg

# Example use of segmentimg
def with_sito():
    print("---- WITH SITO RUNNING ----")
    img.hist_equal_all(on='org_dict')
    img.save_hist_equal_all(r"\backup2\histeq", "(Histogram Equal WS)")

    img.bilateral_all(on='hist_equal_dict')
    img.save_bilateral_all(r"\backup2\bilateral", "(Bilateral Blur WS)")

    img.thresh_green_chan_all(on='bilateral_dict')
    img.save_thresh_green_chan_all(r"\backup2\thresh green", "(Threshold Green WS)")

    img.masked_all(on='thresh_inv_green', mask='org_dict') # ukuran harus sesuai dari thresh
    img.save_masked_all(r"\backup2\masked with sito", "(Masked WS)")
    print("---- WITH SITO DONE ----")

def with_no_sito(use_rescale=False):
    print("---- WITH NO SITO RUNNING ----")
    img.bilateral_all(on='org_dict')
    img.save_bilateral_all(r"\backup2\bilateral no sito", "(Bilateral Blur WNS)")
    
    img.thresh_gray_all(on='bilateral_dict')
    img.save_thresh_gray(r"\backup2\thresh gray", "(Threshold Gray WNS)")

    img.masked_all(on='thresh_inv_gray', mask='org_dict')
    img.save_masked_all(r"\backup2\masked with no sito", "(Masked WNS)")
    print("---- WITH NO SITO DONE ----")

img = simg.segmentImg(r"C:\Users\Mahatma Ageng Wisesa\Desktop\OpenCV", "test3")
img.read_all_img()

img.rescale_all()
img.save_rescaled_all(r"\backup2\rescale")

with_sito()
with_no_sito()