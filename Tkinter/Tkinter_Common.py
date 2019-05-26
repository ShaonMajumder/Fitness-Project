import ctypes
from PIL import ImageTk,Image
import PIL

def image_to_tkinter_img(filepath, size):
    #size = (90, 90)
    original = PIL.Image.open(filepath)
    resized = original.resize(size,PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(resized)
    return img

def get_screen_size():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize

def tkinter_center(toplevel):
    screen_width, screen_height = get_screen_size()
    toplevel.update_idletasks()
    width = toplevel.winfo_width()
    height = toplevel.winfo_height()
    x = screen_width//2 - width//2
    y = screen_height//2 - height//2
    toplevel.geometry('{}x{}+{}+{}'.format(width, height, x, y))