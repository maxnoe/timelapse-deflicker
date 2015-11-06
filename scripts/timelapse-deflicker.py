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

import sys
import os
import logging
from docopt import docopt, DocoptExit
from schema import Schema, And, Or, Use, SchemaError

import deflicker


def mkdir_p(directory):
    logger = logging.getLogger()
    if not os.path.exists(directory):
        logger.info('Created directory: {}'.format(directory))
        os.makedirs(directory)
    return directory

formats = ['png', 'tiff', 'tif', 'jpg', 'jpeg']

args_schema = Schema({
    '<inputdir>': Schema(os.path.exists, '<inputdir> does not exist'),
    '--window': And(
        Use(int), lambda x: x > 0,
        error='--window has to be a positive integer'
    ),
    '--format': Or(*formats, error='Unsupported format'),
    '--sigma':  Or(
        None,
        And(Use(float), lambda x: x > 0, error='--sigma must be positive'),
    ),
    '--outdir': Use(mkdir_p),
    '--quiet': bool,
})


def main():
    try:
        args = docopt(__doc__, version=deflicker.__version__)
        args = args_schema.validate(args)

        logging.basicConfig(
            level=logging.WARNING if args['--quiet'] else logging.INFO,
            format='%(asctime)s - %(levelname)s | %(message)s',
            datefmt='%H:%M:%S',
        )
        logger = logging.getLogger()
        logger.info('This is deflicker {}'.format(deflicker.__version__))

        images = deflicker.find_images(args['<inputdir>'])
        if not images:
            logger.error('No images found in "{}"'.format(args['<inputdir>']))
            sys.exit(1)

        deflicker.deflicker_images(
            images,
            args['--window'],
            args['--outdir'],
            fmt=args['--format'],
            sigma=args['--sigma'],
        )
    except DocoptExit as e:
        print(e)
    except SchemaError as e:
        print(e)
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
