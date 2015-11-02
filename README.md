# Image Deflickering for Timelapse Videos

After I made my first few timelapse videos I got really
bothered by the erratic small changes of exposure, which are caused
by various effects:
* Changes of the exposure settings (if not in full manual mode)
* Uncertainties of the aperture
* Shutter jitter

I was looking for an existing solution and only found expensive (O(100€))
software.

So I wrote this little (150 SLOCS) programm.
The brightness of the images are adjusted to fit a rolling mean several consecutive images.
