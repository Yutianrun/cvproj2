#!/usr/bin/python3

import numpy as np

def compute_normalized_patch_descriptors(
    image_bw: np.ndarray, X: np.ndarray, Y: np.ndarray, feature_width: int
) -> np.ndarray:

    K = X.shape[0]
    D = feature_width ** 2
    fvs = np.zeros((K, D))

    for i in range(K):
        x_center = int(X[i])
        y_center = int(Y[i])

        start_x = max(0, x_center - feature_width // 2)
        end_x = min(image_bw.shape[1], x_center + feature_width // 2 + 1)
        start_y = max(0, y_center - feature_width // 2)
        end_y = min(image_bw.shape[0], y_center + feature_width // 2 + 1)

        patch = image_bw[start_y:end_y, start_x:end_x]

        patch_flat = patch.flatten()

        norm = np.linalg.norm(patch_flat)

        if norm!= 0:
            fvs[i] = patch_flat / norm

    return fvs

def compute_normalized_patch_descriptors_copilot(
    image_bw: np.ndarray, X: float, Y: float, feature_width: int
) -> np.ndarray:
    """Create local features using normalized patches.

    Normalize image intensities in a local window centered at keypoint to a
    feature vector with unit norm. This local feature is simple to code and
    works OK.

    Choose the top-left option of the 4 possible choices for center of a square
    window.

    Args:
        image_bw: array of shape (M,N) representing grayscale image
        X: array of shape (K,) representing x-coordinate of keypoints
        Y: array of shape (K,) representing y-coordinate of keypoints
        feature_width: size of the square window

    Returns:
        fvs: array of shape (K,D) representing feature descriptors
    """
    K = len(X)
    D = feature_width * feature_width
    fvs = np.zeros((K, D))

    half_width = feature_width // 2

    for i in range(K):
        x = int(X[i])
        y = int(Y[i])
        
        # Ensure the patch is within the image boundaries
        if x - half_width < 0 or x + half_width >= image_bw.shape[1] or \
           y - half_width < 0 or y + half_width >= image_bw.shape[0]:
            continue
        
        patch = image_bw[y - half_width:y + half_width, x - half_width:x + half_width]
        patch = patch.flatten()
        
        # Normalize the patch to have unit norm
        norm = np.linalg.norm(patch)
        if norm != 0:
            patch = patch / norm
        
        fvs[i, :] = patch

    return fvs
