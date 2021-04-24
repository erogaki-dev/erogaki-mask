import numpy as np
from cv2 import erode
import skimage
from PIL import Image

from mrcnn.config import Config
from mrcnn import model as modellib, utils
from NoCensoredRegionsFoundError import NoCensoredRegionsFoundError

class ErogakiMaskConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "erogaki-mask"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background) 
    NUM_CLASSES = 1 + 1 + 1 

    # Number of training steps per epoch, equal to dataset train size
    STEPS_PER_EPOCH = 1490

    # Skip detections with < 75% confidence
    DETECTION_MIN_CONFIDENCE = 0.75

class Detector():
    def __init__(self, weights_path):
        self.weights_path = weights_path
        self.config = ErogakiMaskConfig()
        self.model = modellib.MaskRCNN(mode="inference", config=self.config, model_dir="logs")

    def load_weights(self):
        print("Loading weights...")
        try:
            self.model.load_weights(self.weights_path, by_name=True)
            print("Weights loaded")
        except Exception as e:
            print("ERROR in load_weights: Model Load. Ensure you have your weights.h5 file!", end=' ')
            print(e)

    """Apply cover over image. Based off of Mask-RCNN Balloon color splash function
    image: RGB image [height, width, 3]
    mask: instance segmentation mask [height, width, instance count]
    Returns result covered image.
    """
    def apply_cover(self, image, mask, dilation):
        # Copy color pixels from the original color image where mask is set
        green = np.zeros([image.shape[0], image.shape[1], image.shape[2]], dtype=np.uint8)
        green[:,:] = [0, 255, 0]

        if mask.shape[-1] > 0:
            # We're treating all instances as one, so collapse the mask into one layer
            mask = (np.sum(mask, -1, keepdims=True) < 1)
            # dilate mask to ensure proper coverage
            mimg = mask.astype('uint8')*255
            kernel = np.ones((dilation,dilation), np.uint8)
            mimg = erode(src=mask.astype('uint8'), kernel=kernel, iterations=1) #
            # dilation returns image with channels stripped (?!?). Reconstruct image channels
            mask_img = np.zeros([mask.shape[0], mask.shape[1],3]).astype('bool')
            mask_img[:,:,0] = mimg.astype('bool')
            mask_img[:,:,1] = mimg.astype('bool')
            mask_img[:,:,2] = mimg.astype('bool')
            
            cover = np.where(mask_img.astype('bool'), image, green).astype(np.uint8)
        else:
            # error case, return image
            cover = image
        return cover, mask 

    def detect_and_mask(self, image, is_mosaic=False, dilation=0):
        image = np.array(image)

        if image.ndim != 3: 
            image = skimage.color.gray2rgb(image) # convert to rgb if greyscale
        if image.shape[-1] == 4:
            image = image[..., :3] # strip alpha channel

        try:
            r = self.model.detect([image], verbose=0)[0]
        except Exception as e:
            print("ERROR in detect_and_cover: Model detection.",e)
            return

        # Remove unwanted class, code from https://github.com/matterport/Mask_RCNN/issues/1666
        if is_mosaic == True:
            remove_indices = np.where(r["class_ids"] != 2) # remove bars: class 2
        else:
            remove_indices = np.where(r["class_ids"] != 1) # remove mosaic: class 1
        new_masks = np.delete(r["masks"], remove_indices, axis=2)

        cov, mask = self.apply_cover(image, new_masks, dilation)

        if mask.size == 0:
            raise NoCensoredRegionsFoundError("No censored regions detected.")

        return Image.fromarray(cov.astype("uint8"))
