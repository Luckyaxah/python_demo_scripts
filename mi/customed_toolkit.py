import matplotlib.pyplot as plt
import numpy as np

from skimage.color import rgba2rgb,rgb2hsv
from scipy import ndimage as ndi


def show_with_mask(img, mask):
    img[mask,0]=1
    img[mask,1]=0
    img[mask,2]=0
    show_img(img, mask)

def show_img(*img):
    """
    展示图像
    """
    length = len(img)
    for i in range(length):
        plt.subplot(1,length,i+1)
        plt.imshow(img[i])
    plt.show()

def extract_edges_points(img):
    """
    获得边界mask和边界点集
    """
    from skimage.filters import sobel
    elevation_map = sobel(img)
    edges_mask = elevation_map > 0.5
    points = get_points_from_mask(edges_mask)
    return points, edges_mask

def get_points_from_mask(mask,origin='left-top'):
    """
    根据mask获取边界点
    """
    points = np.array( np.where(mask) )
    if origin == 'left-top':
        points = points[-1::-1]     # 直接将x,y坐标颠倒
    return points

def get_edges_from_curve(img):
    """
    根据标注曲线获取mask
    """
    img_hsv = rgb2hsv(img)
    img_hsv_saturation = img_hsv[:,:,1]
    edges_mask = img_hsv_saturation > 0.5
    points = get_points_from_mask(edges_mask)
    return points, edges_mask

def segment_by_mask(img_rgb,img_mask):
    """
    根据图像上的标注提取区域
    """
    img =np.ones((img_rgb.shape[0],img_rgb.shape[1],img_rgb.shape[2]))
    fill_holes = ndi.binary_fill_holes(img_mask)
    img[fill_holes] =img_rgb[fill_holes]
    return img