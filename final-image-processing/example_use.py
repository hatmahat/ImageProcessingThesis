import segmentimg as simg

# Example use of segmentation
def use_rescale(func):
    def wrapper(use_rescale):
        global base_dict
        if use_rescale:
            base_dict = 'rescaled_dict'
        else:
            base_dict = 'org_dict'
        print("#########################")
        print("######## RUNNING ########")
        print("#########################")
        func(use_rescale)
        print("##########################")
        print("########## DONE ##########")
        print("##########################")
    return wrapper

@use_rescale
def with_cyto(use_rescale=False):
    img.hist_equal_all(on=base_dict)
    img.save_hist_equal_all(r"\backup2\histeq", "(Histogram Equal WS)")

    img.bilateral_all(on='hist_equal_dict')
    img.save_bilateral_all(r"\backup2\bilateral", "(Bilateral Blur WS)")

    img.thresh_green_chan_all(on='bilateral_dict')
    img.save_thresh_green_chan_all(r"\backup2\thresh green", "(Threshold Green WS)")

    img.masked_all(on='thresh_inv_green', mask=base_dict) # ukuran harus sesuai dari thresh
    img.save_masked_all(r"\backup2\masked with sito", "(Masked WS)")

@use_rescale
def with_no_cyto(use_rescale=False):
    img.bilateral_all(on=base_dict)
    img.save_bilateral_all(r"\backup2\bilateral no sito", "(Bilateral Blur WNS)")
    
    img.thresh_gray_all(on='bilateral_dict')
    img.save_thresh_gray(r"\backup2\thresh gray", "(Threshold Gray WNS)")

    img.masked_all(on='thresh_inv_gray', mask=base_dict)
    img.save_masked_all(r"\backup2\masked with no sito", "(Masked WNS)")

def main():
    img = simg.segmentImg(r"C:\Users\Mahatma Ageng Wisesa\Desktop\OpenCV", "test3")
    img.read_all_img()

    img.rescale_all()
    img.save_rescaled_all(r"\backup2\rescale")

    with_cyto(use_rescale=True) # with cytoplasm
    with_no_cyto(use_rescale=True) # with no cytoplasm, only nucleus

if __name__ == '__main__':
    main()