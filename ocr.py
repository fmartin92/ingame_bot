from PIL import Image, ImageOps, ImageGrab
import pytesseract
from config import *

def length(coords):
    return coords[2]-coords[0]
def height(coords):
    return coords[3]-coords[1]
def crop_by_coords(original, coords, inv=False):
	img = original.crop(coords)
	if inv:
		img = ImageOps.invert(img)
	return img.resize((3*length(coords), 3*height(coords)))

def read_question():
    #si se rompe la captura: import pyscreenshot as ImageGrab
    screenshot = ImageGrab.grab()
    if GAME == 'ingame':
        q_coords = (640, 303, 970, 388)
        o_coords=[[(670, 381, 920, 420),(670, 451, 920, 497), (670, 526, 920, 568)],
            [(670, 403, 920, 442),(670, 473, 920, 519),(670, 548, 920, 590)],
            [(670, 425, 920, 464),(670, 496, 920, 542),(670, 571, 920, 613)]]
    else:
        q_coords = (651, 218, 949, 343)
        o_coords = [(651, 367, 949, 399), (651, 414, 949, 447),
                    (651, 463, 949, 498), (651, 513, 949, 547)]


    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    invert = True if GAME == 'ingame' else False
    q_img = crop_by_coords(screenshot, q_coords, inv=invert)
    q_lines = pytesseract.image_to_string(q_img, lang='spa').split('\n')
    q_text = ' '.join(q_lines)
    o_text = []
    correct_coords = o_coords[len(q_lines)-1] if GAME == 'ingame' else o_coords
    for i in correct_coords:
        o_img = crop_by_coords(screenshot, i)
        text_lines = pytesseract.image_to_string(o_img, lang='spa').split('\n')
        o_text.append(max(text_lines, key=len))
    return q_text, o_text
