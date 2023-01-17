"""OpenCV image processing functions."""

import cv2 as cv
import numpy as np


def extract_signature(image, method="binary"):
    """Extract signature from image."""
    grayscale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # convert to grayscale
    match method:
        case "binary":
            extracted = binary(grayscale)
        case "adaptive":
            extracted = adaptive(grayscale)
        case "otsu":
            extracted = otsu(grayscale)
        case "canny":
            extracted = canny(grayscale)
        case "sobel":
            extracted = sobel(grayscale)
        case "laplacian":
            extracted = laplacian(grayscale)
        case _:
            extracted = binary(grayscale)

    rgba = cv.cvtColor(extracted, cv.COLOR_GRAY2RGBA)  # convert to RGBA
    rgba[np.where((rgba == [255, 255, 255, 255]).all(axis=2))] = [0, 0, 0, 0]
    return rgba


def invert(image) -> np.ndarray:
    """Invert image."""
    return cv.bitwise_not(image)


def fill(image) -> np.ndarray:
    """Fill area within signature."""
    contours, _ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)[1:]
    cv.drawContours(image, contours, 0, 0, -1)
    return image


def binary(grayscale) -> np.ndarray:
    """Convert grayscale image to binary."""
    _, converted = cv.threshold(grayscale, 127, 255, cv.THRESH_BINARY)
    return converted


def adaptive(grayscale) -> cv.Mat:
    """Convert grayscale image to binary using adaptive thresholding."""
    converted = cv.adaptiveThreshold(grayscale, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    return converted


def otsu(grayscale) -> cv.Mat:
    """Convert grayscale image to binary using Otsu's method."""
    _, converted = cv.threshold(grayscale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return converted


def canny(grayscale) -> cv.Mat:
    """Convert grayscale image to binary using Canny edge detection."""
    edges = cv.Canny(grayscale, 100, 200)
    _, converted = cv.threshold(edges, 127, 255, cv.THRESH_BINARY)
    return fill(invert(converted))


def sobel(grayscale) -> cv.Mat:
    """Convert grayscale image to binary using Sobel edge detection."""
    edges = cv.Sobel(grayscale, cv.CV_8U, 1, 0, ksize=3)
    _, converted = cv.threshold(edges, 127, 255, cv.THRESH_BINARY)
    return fill(invert(converted))


def laplacian(grayscale) -> cv.Mat:
    """Convert grayscale image to binary using Laplacian edge detection."""
    edges = cv.Laplacian(grayscale, cv.CV_8U, ksize=3)
    _, converted = cv.threshold(edges, 127, 255, cv.THRESH_BINARY)
    return fill(invert(converted))
