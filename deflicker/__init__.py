import logging
import numpy as np
import os
import warnings
from progressbar import ProgressBar
from skimage import io
from skimage import img_as_ubyte, img_as_uint, img_as_float

import pkg_resources
__version__ = pkg_resources.require('deflicker')[0].version


def rolling_mean(data, window):
    ''' compute the rolling mean of the data over the given window '''

    result = np.full_like(data, np.nan)

    conv = np.convolve(data, np.ones(window)/window, mode='valid')
    result[(len(data) - len(conv))//2: (len(conv) - len(data))//2] = conv

    return result


def getProgressBar(logger, level=logging.INFO, **kwargs):
    if logger.getEffectiveLevel() <= level:
        prog = ProgressBar(**kwargs)
    else:
        prog = lambda x:  x
    return prog


def find_images(directory, extensions=['.jpg', '.png', '.tiff', '.tif']):
    logger = logging.getLogger()

    images = []
    # walk just the parent dir, reuturn empty list of nothing found
    root, _, files = next(os.walk(directory), (None, None, []))
    for f in files:
        name, extension = os.path.splitext(f)
        if extension.lower() in extensions:
            images.append(os.path.join(root, f))

    logger.info(
        'Found {} images in directory {}'.format(len(images), directory)
    )
    return sorted(images)


def calc_brightness(images, sigma=2.5):
    logger = logging.getLogger()
    logger.info('Calculating brightness of the images')

    brightness = []
    prog = getProgressBar(logger)
    for filename in prog(images):
        image = io.imread(filename)
        mask = np.ones_like(image[:, :, 0], dtype=bool)

        if sigma is not None:
            for channel in range(3):
                mean = np.mean(image[:, :, channel])
                std = np.std(image[:, :, channel])
                dist = np.abs(image[:, :, channel] - mean) / std
                mask[dist > sigma] = False

        brightness.append(np.mean(image[mask]))

    return np.array(brightness)


def scale_image_brightness(image, scale):
    ''' scale image brightness by a factor '''
    adjusted_image = scale * img_as_float(image)
    # handle overflow:
    adjusted_image[adjusted_image >= 1.0] = 1.0

    # catch warning for loosing some accuracy by converting back to int types
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=UserWarning)
        if image.dtype == np.dtype('uint8'):
            adjusted_image = img_as_ubyte(adjusted_image)
        elif image.dtype == np.dtype('uint16'):
            adjusted_image = img_as_uint(adjusted_image)

    return adjusted_image


def deflicker_images(images, window, outdir, fmt='png', sigma=2.5):
    ''' Deflicker images
    Image brightness is scaled to match a rolling mean to avoid flickering

    Parameters
    ----------
    images: list of strings
        Filenames of the images that should be processed
    window: int
        The width of the window for the rolling mean
    outdir: string
        The directory where the adjusted images are saved
    fmt: string
        Output format. One of png, tiff, jpg
    '''
    logger = logging.getLogger()
    brightness = calc_brightness(images, sigma=sigma)

    target_brightness = rolling_mean(brightness, window)

    logger.info('Start brightness correction')
    prog = getProgressBar(logger, maxval=len(images))
    for filename, b, tb in prog(zip(images, brightness, target_brightness)):
        image = io.imread(filename)
        if np.isnan(tb):
            adjusted_image = image.copy()
        else:
            adjusted_image = scale_image_brightness(image, tb / b)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=UserWarning)
            io.imsave(
                os.path.join(
                    outdir,
                    os.path.splitext(os.path.basename(filename))[0] + '.' + fmt
                ),
                adjusted_image,
            )
    print()
    logger.info('Brightness correction finished')
