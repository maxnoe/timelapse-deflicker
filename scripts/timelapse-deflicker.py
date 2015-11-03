#!/usr/bin/env python
'''
A small tool for deflickering images for time lapse videos.
The brightness of the images are adjusted to a rolling mean above <N> images
For the calculation of the image brightness, outliers are discarded via
sigma clipping if the --sigma option is given

Usage:
    timelapse-deflicker.py <inputdir> [options]

Options:
    -o <dir>, --outdir=<dir>  Output directory [default: deflickered]
    -w <N>, --window=<N>      Window size for rolling mean [default: 10]
    -q, --quiet               Only output errors and warnings
    -f <fmt>, --format=<fmt>  Output format for the scaled images [default: png]
    -s <s>, --sigma=<s>       Sigma for the sigma clipping
'''


import logging
from docopt import docopt
import deflicker
import os


def main(args):
    logger = logging.getLogger()
    logging.info('This is deflicker {}'.format(deflicker.__version__))
    images = deflicker.find_images(args['<inputdir>'])
    window = int(args['--window'])
    outdir = args['--outdir']
    sigma = float(args['--sigma']) if args['--sigma'] else None

    if args['--format'].lower() not in ['png', 'tiff', 'tif', 'jpg', 'jpeg']:
        message = 'Not supported output format: {}'.format(args['--format'])
        logger.error(message)
        raise ValueError(message)

    if not os.path.exists(outdir):
        logger.info('Outputdir {} does not exist, creating it'.format(outdir))
        os.makedirs(outdir)

    deflicker.deflicker_images(
        images,
        window,
        outdir,
        fmt=args['--format'],
        sigma=sigma,
    )


if __name__ == '__main__':
    args = docopt(__doc__, version=deflicker.__version__)

    if args['--quiet']:
        loglevel = logging.WARNING
    else:
        loglevel = logging.INFO

    logging.basicConfig(
        level=loglevel,
        format='%(asctime)s - %(levelname)s | %(message)s',
        datefmt='%H:%M:%S',
    )

    try:
        main(args)
    except (KeyboardInterrupt, SystemExit):
        pass
