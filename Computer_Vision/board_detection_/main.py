import gc, os, sys, glob, argparse, utils
from utils import ImageObject
from slid import pSLID, SLID, slid_tendency  # == step 1
from laps import LAPS  # == step 2
from llr import LLR, llr_pad  # == step 3
import numpy as np
from keras import backend as K
import cv2
import time
import config as config

load = cv2.imread
save = cv2.imwrite

POINTS = []


def layer():
    global NC_LAYER, NC_IMAGE,POINTS  # , NC_SCORE
    # start = time()
    # --- 1 step --- find all possible lines (that makes sense) ----------------
    # print(utils.ribb(utils.head("SLID"), utils.clock(), "--- 1 step "))
    print("Etape 1")
    segments = pSLID(NC_IMAGE['main'])
    raw_lines = SLID(NC_IMAGE['main'], segments)
    lines = slid_tendency(raw_lines)

    # --- 2 step --- find interesting intersections (potentially a mesh grid) --
    print("Etape 2")

    # print(utils.ribb(utils.head("LAPS"), utils.clock(), "--- 2 step "))
    points = LAPS(NC_IMAGE['main'], lines)
    # print(abs(49 - len(points)), NC_SCORE)
    # if NC_SCORE != -1 and abs(49 - len(points)) > NC_SCORE * 4: return
    # NC_SCORE = abs(49 - len(points))

    # --- 3 step --- last layer reproduction (for chessboard corners) ----------
    # print(utils.ribb(utils.head(" LLR"), utils.clock(), "--- 3 step "))
    print("Etape 3")
    inner_points = LLR(NC_IMAGE['main'], points, lines)
    four_points = llr_pad(inner_points, NC_IMAGE['main'])  # padcrop

    # --- 4 step --- preparation for next layer (deep analysis) ----------------
    # print(utils.ribb(utils.head("   *"), utils.clock(), "--- 4 step "))
    print("Etape 4")
    print(four_points)
    try:
        NC_IMAGE.crop(four_points)
        POINTS = four_points
        print("Done")
    except:
        # utils.warn("Erreur lors du crop")
        NC_IMAGE.crop(inner_points)
        POINTS = inner_points
    print("\n")


################################################################################
import re  # regex


def detect(args):
    global NC_LAYER, NC_IMAGE, NC_CONFIG
    NC_LAYER = config.NC_LAYER
    NC_CONFIG = config.NC_CONFIG
    NC_IMAGE = config.NC_IMAGE
    # NC_LAYER =
    # print("_______________________________________________________))")
    # print(NC_CONFIG)
    # NC_CONFIG = config.NC_CONFIG
    # print(NC_CONFIG)
    if (not os.path.isfile(args)):
        utils.errn("error: the file \"%s\" does not exits" % args)
        return

    NC_IMAGE, NC_LAYER = ImageObject(cv2.imread(args)), 0
    for _ in range(NC_CONFIG['layers']):
        NC_LAYER += 1;
        layer()
    ext = re.findall(r'.\w+$', args)
    name = re.sub(r'.\w+$', '_cropped', args) + str(ext[0])
    cv2.imwrite(name, NC_IMAGE['orig'])
    # plot image
    # cv2.imshow('image', NC_IMAGE['orig']) # todo : remove
    # cv2.waitKey(0)
    print("DETECT: %s" % args)
    # return path of cropped image
    return name


def test(args):
    files = glob.glob('test/in/*.jpg')

    for iname in files:
        oname = iname.replace('in', 'out')
        args.input = iname;
        args.output = oname
        detect(args)
    print("TEST: %d images" % len(files))


# if __name__ == "__main__":
#     utils.reset()
#
#     # p = argparse.ArgumentParser(description= \
#     #                                 'Find, crop and create FEN from image.')
#
#     # p.add_argument('mode', nargs=1, type=str, \
#     #                help='detect | dataset | train')
#     # p.add_argument('--input', type=str, \
#     #                help='input image (default: input.jpg)')
#     # p.add_argument('--output', type=str, \
#     #                help='output path (default: output.jpg)')
#
#     # os.system("rm test/steps/*.jpg") # FIXME: to jest bardzo grozne
#     os.system("rm -rf test/steps; mkdir test/steps")
#
#     # args = p.parse_args();
#     # mode = str(args.mode[0])
#     # modes = {'detect': detect, 'dataset': dataset, 'train': train, 'test': test}
#
#     # if mode not in modes.keys():
#     #     utils.errn("hey, nie mamy takiej procedury!!! (wybrano: %s)" % mode)
#     # modes[mode](args);
#     # print(utils.clock(), "done")
#     K.clear_session();
#     gc.collect()  # FIX: tensorflow#3388

################################################################################

if __name__ == "__main__":
    utils.reset()
    args = sys.argv[1]
    # print("mode: ", r"C:\Users\ddbtn\PycharmProjects\chess_board_detection_refactor\test\test1.jpg")
    start = time.time()
    detect(args)
    print("time: ", time.time() - start)
    # while True:
    #     print("1. calibrate & detect 2. detect only (coordinates) and wait for user input")
    #     mode = int(input())
    #     if mode == 1:
    #         print("calibrate")
    #         detect(args)
    #     elif mode == 2:
    #         print("detect")
    #         NC_IMAGE, NC_LAYER = ImageObject(cv2.imread(args)), 0
    #         NC_IMAGE.crop(POINTS)
    #         cv2.imshow('image', NC_IMAGE['orig'])
    #         cv2.waitKey(0)
    #     else:
    #         print("wrong mode")
    #         break

    os.system("rm -rf test/steps; mkdir test/steps")

    K.clear_session();
    gc.collect()
