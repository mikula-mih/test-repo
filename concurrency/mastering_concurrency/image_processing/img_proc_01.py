import numpy as np
import cv2

im = cv2.imread('richard_stallman.jpeg')
cv2.imshow('Test', im)
cv2.waitKey(0) # press any key to move forward here

print(im)
print('Type: ', type(im))
print('Shape: ', im.shape)
print('Top-left pixel: ', im[0, 0])

print('Done')

def grayscaling():
    gray_im = cv2.cvtColor(im, cv2.COLOR_BRG2GRAY)

    cv2.imshow('Grayscale', gray_im)
    cv2.waitKey(0)

    print(gray_im)
    print('Type: ', type(gray_im))
    print('Shape: ', gray_im.shape)
    cv2.imwrite('output/richard_stallman.jpeg', gray_im)

    print('Done')

def thresholding():
    gray_im = cv2.cvtColor(im, cv2.COLOR_BRG2GRAY)

    ret, custom_thresh_im = cv2.threshold(gray_im, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite('output/custom_richard_stallman.jpeg', custom_threash_im)

    print('Done')

def adaptive_thresholding():
    # Adaptive_Mean_Thresholding
    # Adaptive_Gaussian Thresholding
    im = cv2.cvtColor(im, cv2.COLOR_BRG2GRAY)

    mean_thresh_im = cv2.asaptiveThreshold(im, 255, cv2.ADAPTIVE_THESH_MEAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite('output/mean_thresh_stallman.jpeg', mean_thresh_im)

    gauss_thresh_im = cv2.adaptiveThreshold(im, 255,
                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite('output/gauss_thresh_stallman.jpeg', gauss_thresh_im)

    print('Done')
