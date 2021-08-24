import cv2 as cv
import os

def rescaleFrame(frame, scale=0.2):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

img = cv.imread("LBS HistEq.jpg")
# img = rescaleFrame(img)
# cv.imshow("IMG HistEq", img)

# Bilateral 
bilateral_hist = cv.bilateralFilter(img, 10, 50, 50)
# cv.imshow("Bilateral HistEq", bilateral_hist)

## baru
b, g, r = cv.split(bilateral_hist)
# cv.imshow("Green Channel", g)

ret, thresh_inv_hist = cv.threshold(g, 100, 255, cv.THRESH_BINARY_INV)
cv.imshow("Threshold INV Green Channel", thresh_inv_hist)
## baru

img_org = cv.imread("LBS.jpg")
img_org = rescaleFrame(img_org)
# cv.imshow("IMG Original", img_org)

bilateral = cv.bilateralFilter(img_org, 25, 75, 75)
# cv.imshow("Bilateral Original", bilateral)

gray = cv.cvtColor(bilateral, cv.COLOR_BGR2GRAY)
# cv.imshow("Gray Original", gray)

ret, thresh_inv = cv.threshold(gray, 110, 255, cv.THRESH_BINARY_INV)
# cv.imshow("Threshold Original", thresh_inv)

masked = cv.bitwise_and(img_org, img_org, mask=thresh_inv)
cv.imshow("Masked no HistEq", masked)
cv.imwrite("Masked no HistEq.jpg", masked)

masked_hist = cv.bitwise_and(img_org, img_org, mask=thresh_inv_hist)
cv.imshow("Masked with HistEq", masked_hist)
# cv.imwrite("Masked with HistEq.jpg", masked_hist)
print(type(img))
cv.waitKey(0)
