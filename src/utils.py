import time
from PIL import Image
try:
    import httplib
except:
    import http.client as httplib


def time_it(method):
    def timed(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        run_time = time.time()-start_time
        print("Call took {} seconds".format(run_time))
        return result
    return timed


def check_wifi_status():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    #cropped_image.show()
