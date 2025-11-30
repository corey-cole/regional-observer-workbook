from __future__ import annotations
import cv2
import numpy as np


def image_as_grayscale(image: np.ndarray | None) -> np.ndarray | None:
    """Convert to grayscale if required"""
    if image is None:
        return None
    if len(image.shape) > 2:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


# TODO: Add better error handling
# For testing, we can align the original to itself and should get an image
# For negative testing, align PNG of same size but random content and confirm that it fails.
def align_to_original(
    scan: np.ndarray,
    original: np.ndarray,
    max_features: int = 500,
    keep_percent: float = 0.2,
) -> np.ndarray:
    imageGray = image_as_grayscale(scan)
    templateGray = image_as_grayscale(original)

    # Use ORB to detect keypoints and extract features
    orb = cv2.ORB_create(max_features)
    (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
    (kpsB, descsB) = orb.detectAndCompute(templateGray, None)

    # match features
    method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv2.DescriptorMatcher_create(method)
    matches = matcher.match(descsA, descsB, None)

    # Sort by distance (similarity)
    matches = sorted(matches, key=lambda x: x.distance)

    keep = int(len(matches) * keep_percent)
    matches = matches[:keep]

    ptsA = np.zeros((len(matches), 2), dtype="float")
    ptsB = np.zeros((len(matches), 2), dtype="float")

    for i, m in enumerate(matches):
        ptsA[i] = kpsA[m.queryIdx].pt
        ptsB[i] = kpsB[m.trainIdx].pt

    (H, _) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)

    (h, w) = original.shape[:2]
    aligned = cv2.warpPerspective(scan, H, (w, h))

    return aligned


def get_cell(
    row: int, col: int, aligned_image: np.ndarray, bbox: np.ndarray
) -> np.ndarray:
    if row >= bbox.shape[0]:
        raise IndexError(
            f"Row index {row} out of bounds for bounding box with shape {bbox.shape}"
        )
    if col >= bbox.shape[1]:
        raise IndexError(
            f"Column index {col} out of bounds for bounding box with shape {bbox.shape}"
        )
    if bbox.shape[2] != 4:
        raise ValueError(
            f"Bounding box third dimension must be of length 4, got {bbox.shape[2]}"
        )
    x, y, w, h = bbox[row, col]
    return aligned_image[y : y + h, x : x + w]
