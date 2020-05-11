

if __name__ == "__main__":

    from skimage import io
    from skimage.color import rgba2rgb
    from customed_toolkit import get_edges_from_curve, segment_by_mask, show_img


    img = io.imread('./img2.png')
    channel = img.shape[2]
    if channel == 4:
        img_rgb = rgba2rgb(img)
    points, edges_mask = get_edges_from_curve(img_rgb)
    processed_img = segment_by_mask(img_rgb,edges_mask)

    show_img(img_rgb,processed_img)