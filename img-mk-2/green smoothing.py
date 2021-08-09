import cv2 as cv

def rescaleFrame(frame, scale=.2):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

img = cv.imread("LBS HistEq.jpg")
# img = rescaleFrame(img)
cv.imshow("IMG", img)

bilateral = cv.bilateralFilter(img, 10, 50, 50)
cv.imshow("Bilateral HistEq", bilateral)

img_org = cv.imread("LBS.jpg")
img_org = rescaleFrame(img_org)
cv.imshow("IMG ORG", img_org)

b, g, r = cv.split(bilateral)
cv.imshow("Green", g)

ret, thresh_inv = cv.threshold(g, 100, 255, cv.THRESH_BINARY_INV)
cv.imshow("Threshold INV", thresh_inv)

masked = cv.bitwise_and(img_org, img_org, mask=thresh_inv)
cv.imshow("Masked HistEq", masked)

cv.waitKey(0)