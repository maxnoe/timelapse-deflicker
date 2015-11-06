Image Deflickering for Timelapse Videos
=======================================

After I made my first few timelapse videos I got really bothered by the
erratic small changes of exposure, which are caused by various effects:
\* Changes of the exposure settings (if not in full manual mode) \*
Uncertainties of the aperture \* Shutter jitter

I was looking for an existing solution and only found expensive
(O(100€)) software.

So I wrote this little (150 SLOCS) programm. The brightness of the
images are adjusted to fit a rolling mean over several consecutive
images.

Installation
------------

I recommend anaconda, it comes with the heavy dependencies of this
package: ``numpy`` and ``scikit-image``

Installation of ``deflicker``:

::

    $ pip install deflicker

Usage
-----

``deflicker`` expects all your pictures in one directory. The
alphabetical order has to be equivalent to the chronological order.

::

    deflicker <inputfolder> [options]

Options
~~~~~~~

-  ``-o <dir>, --outdir=<dir>`` Output directory [default: deflickered]
-  ``-w <N>, --window=<N>`` Window size for rolling mean [default: 10]
-  ``-q, --quiet`` Only output errors and warnings
-  ``-f <fmt>, --format=<fmt>`` Output format for the scaled images
   [default: png]
-  ``-s <s>, --sigma=<s>`` Sigma for the sigma clipping
