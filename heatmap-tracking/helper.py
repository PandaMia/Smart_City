import os
import numpy as np
import cv2
import cv2
import numpy as np
import cmapy
import tqdm


def background(path, background_count=50):
    import numpy as np
    import cv2

    # Open Video
    cap = cv2.VideoCapture(path)

    frame_h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    # Randomly select N frames
    frameIds = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=background_count)

    # Store selected frames in an array
    frames = []
    i = 0
    for fid in tqdm.tqdm(frameIds):
        i+=1
        cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
        _, frame = cap.read()
        frames.append(frame)

    # Calculate the median along the time axis
    medianFrame = np.median(np.array(frames), axis=0).astype(dtype=np.uint8)

    # Display median frame
    cv2.imwrite('./background.jpg', medianFrame)
    cv2.waitKey(0)
    return frame_h, frame_w




def one_mask(path, base, height, width, threshold, intensity):
    with open(path, 'r') as f:
        line = f.read()

    for i in line.split('\n'):
        try:
            x, y, h, w = i.split()[1:]
            y_new = int((float(x))*width + float(h)*width) 
            x_new = int((float(y))*height)

            base[x_new-threshold:x_new+threshold,y_new-threshold:y_new+threshold] = intensity
        except:
            pass
    return base

def get_mask(path, height, width, threshold=5, intensity=30):
    mask = np.zeros((height, width), np.uint8)
    for file in tqdm.tqdm(sorted(os.listdir(path))):

        base = np.zeros((height, width), np.uint8)
        point = one_mask(os.path.join(path, file), 
                                base=base, 
                                height=height, 
                                width=width, 
                                threshold=threshold, 
                                intensity=intensity)

        
        # Очень долго работает. Но это прикольно выглядит простое размытие 2мерного массива по гаусу
        # from scipy.ndimage.filters import gaussian_filter
        # point = gaussian_filter(point, sigma=10)
        mask = cv2.add(mask, point)

    

    mask = np.array((mask - np.min(mask))/(np.max(mask)-np.min(mask))*255, np.uint8)

    color_image_video = cv2.applyColorMap(mask, cmapy.cmap('YlOrBr_r'))
    # color_image_video = cv2.applyColorMap(mask, cv2.COLORMAP_SUMMER)

    cv2.imwrite('./mask.jpg', color_image_video)



def merge(output_path, transparency=0.7):
    first_frame = cv2.imread('./background.jpg')
    color_image = cv2.imread('./mask.jpg')

    _, color_image = cv2.threshold(color_image, 130, 255, cv2.THRESH_TOZERO)
    result_overlay = cv2.addWeighted(first_frame, 0.7, color_image, transparency, 0)

    cv2.imwrite(output_path, result_overlay)