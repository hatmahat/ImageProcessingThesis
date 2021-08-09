import cv2 as cv 
import matplotlib.pyplot as plt

def rescaleFrame(frame, scale=.2):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

img = cv.imread("BBBB HistEq.jpg")
# img = rescaleFrame(img)
cv.imshow("IMG", img)

# Averaging
average = cv.blur(img, (7,7))
cv.imshow("Average Blur", average)

# Gaussian Blur
gaussian = cv.GaussianBlur(img, (7,7), 0)
cv.imshow("Gaussian Blur", gaussian)

# Median Blur
median = cv.medianBlur(img, 7)
cv.imshow("Median Blur", median)

# Bilateral 
bilateral = cv.bilateralFilter(img, 25, 75, 75)
cv.imshow("Bilateral HistEq", bilateral)

gray = cv.cvtColor(bilateral, cv.COLOR_BGR2GRAY)
cv.imshow("gray HistEq", gray)

ret, thresh_inv_hist = cv.threshold(gray, 110, 255, cv.THRESH_BINARY_INV)
cv.imshow("Threshold", thresh_inv_hist)

# di thresholding per RGB? karena beda di green cukup tinggi sama sel darah merah
# COBA THRESHOLDING PER RGB

# bitwise_and = cv.bitwise_and(thresh, bilateral)
# cv.imshow("Bitwise AND", bitwise_and)

# masked = cv.bitwise_and(img, img, mask=cv.bitwise_not(thresh)) # versi lama make bitwise_not tidak mak einvers thresh
# cv.imshow("Masked", masked)

img_org = cv.imread("BBBB.jpg")
img_org = rescaleFrame(img_org)
cv.imshow("IMG ORG", img_org)

bilateral = cv.bilateralFilter(img_org, 25, 75, 75)
cv.imshow("Bilateral", bilateral)

gray = cv.cvtColor(bilateral, cv.COLOR_BGR2GRAY)
cv.imshow("gray", gray)

ret, thresh_inv = cv.threshold(gray, 110, 255, cv.THRESH_BINARY_INV)
cv.imshow("Threshold", thresh_inv)

masked = cv.bitwise_and(img_org, img_org, mask=thresh_inv)
cv.imshow("Masked no HistEq", masked)

masked_hist = cv.bitwise_and(img_org, img_org, mask=thresh_inv_hist)
cv.imshow("Masked with HistEq", masked_hist)

# Color Histogram
# plt.figure()
# plt.title('Grayscale histogram')
# plt.xlabel('Bins')
# plt.ylabel('# of pixels')
# colors = ('b', 'g', 'r')
# for i, col in enumerate(colors):
#     hist = cv.calcHist([img], [i], masked, [256], [0, 256])
#     plt.plot(hist, color=col)
#     plt.xlim([0, 256])

cv.waitKey(0)