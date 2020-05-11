import matplotlib.pyplot as plt
import numpy as np

from skimage.color import rgba2rgb,rgb2hsv
from skimage.feature import canny
from scipy import ndimage as ndi
from scipy.ndimage import find_objects
from customed_toolkit import extract_edges_points,show_with_mask,show_img


def get_edges_from_colouration(img_rgb):
    """
    提取蒙层的边界
    """

    height = img_rgb.shape[0]
    width = img_rgb.shape[1]

    # rgb2hsv
    img_hsv = rgb2hsv(img_rgb)
    img_hsv_hue = img_hsv[:,:,0]

    # Edge-based segmentation
    edges = canny(img_hsv_hue)

    # fill holes
    fill_holes = ndi.binary_fill_holes(edges)

    # label, 填充
    structure = [[1,1,1], [1,1,1], [1,1,1]]
    label_objects,nb_labels = ndi.label(fill_holes,structure)

    
    # 剔除额外的标签
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes> (height*width)*1e-5
    mask_sizes[0] = 0
    bin_img_cleaned = mask_sizes[label_objects]


    # 提取边界点
    return extract_edges_points(bin_img_cleaned)


if __name__ == "__main__":
    from skimage import io
    img = io.imread('./img1.png')
    channel = img.shape[2]
    if channel == 4:
        img_rgb = rgba2rgb(img)
    points,edges_mask = get_edges_from_colouration(img_rgb)
    
    # 结果呈现
    # plt.plot(points[0],points[1],'.')     # 根据坐标点画边界曲线
    show_with_mask(img_rgb,edges_mask)

