#!/usr/bin/env python
import sys
import numpy as np
import cv2
import cv2.aruco as aruco
import reportlab
from reportlab.pdfgen import canvas
import reportlab.lib.pagesizes as pagesizes
from reportlab.lib.utils import ImageReader
import argparse
from PIL import Image


def mm_to_points(mm):
    mm_in_inch = 25.4
    points_in_inch = 72
    return mm * points_in_inch / mm_in_inch


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Aruco marker creator.')
    parser.add_argument('markers', metavar='M', type=int, nargs='+',
                        help='marker values')
    parser.add_argument('-o', '--output', dest='output', type=argparse.FileType('w'),
                        default=sys.stdout, help='PDF output flie path');
    parser.add_argument('-c', '--cells', dest='cells', choices=range(4, 8), default=4,
                        help='number of row/columns in aruco mark (4..7)')
    parser.add_argument('-d', '--dict', dest='dict_size', choices=(50, 100, 250, 1000),
                        default=50, help='marker dictionary size')
    parser.add_argument('-l', '--length', dest='marker_length', type=int, default=50,
                        help='marker length in millimeters')
    parser.add_argument('--paper', dest='paper', choices=('letter', 'A4'), default='A4',
                        help='Paper size')
    parser.add_argument('--landscape', dest='landscape', action='store_const',
                        const=True, default=False, help='Landscape page')
    parser.add_argument('--portrait', dest='landscape', action='store_const',
                        const=False, default=False, help='Portrait page')
    parser.add_argument('--border', type=float, default=1,
                        help='Border factor (number of cells) included in length')
    parser.add_argument('--spacing', dest='spacing', type=float, default=20,
                        help='Marker spacing in vertical and horizontal (mm)')
    parser.add_argument('--pagemargin', dest='margins', type=float, default=15,
                        help='Page margins (mm)')
    parser.add_argument('--labels', dest='labels', action='store_const',
                        const=True, default=False, help='Print marker labels (default false)')
    args = parser.parse_args()
    
    dict_type = { (4, 50): aruco.DICT_4X4_50,
                  (4, 100): aruco.DICT_4X4_100,
                  (4, 250): aruco.DICT_4X4_250,
                  (4, 1000): aruco.DICT_4X4_1000,
                  (5, 50): aruco.DICT_5X5_50,
                  (5, 100): aruco.DICT_5X5_100,
                  (5, 250): aruco.DICT_5X5_250,
                  (5, 1000): aruco.DICT_5X5_1000,
                  (6, 50): aruco.DICT_6X6_50,
                  (6, 100): aruco.DICT_6X6_100,
                  (6, 250): aruco.DICT_6X6_250,
                  (6, 1000): aruco.DICT_6X6_1000,
                  (7, 50): aruco.DICT_7X7_50,
                  (7, 100): aruco.DICT_7X7_100,
                  (7, 250): aruco.DICT_7X7_250,
                  (7, 1000): aruco.DICT_7X7_1000
                }.get((args.cells, args.dict_size))
    aruco_dict = aruco.Dictionary_get(dict_type)
    
    # source: http://www.papersizes.org/a-paper-sizes.htm
    paper_dimensions = {
        'a4': (210, 297),
        'letter': (216, 279),
    }

    paper_types = {
        'a4': pagesizes.A4,
        'letter': pagesizes.letter,
    }
    
    (paper_width, paper_height) = paper_dimensions[args.paper.lower()]
    if (args.landscape):
        (paper_width, paper_height) = (paper_height, paper_width)
    surface = canvas.Canvas(args.output, pagesize=paper_types[args.paper.lower()])
    if args.labels:
        surface.setFont('Helvetica', 10)

    pos = (args.margins, args.margins)
    label_height = 0 if not args.labels else 5

    for marker in args.markers:
        # past horizontal margin?
        if pos[0] + args.marker_length > paper_width - args.margins:
            # one line down
            pos = (args.margins, pos[1] + args.marker_length + args.spacing + label_height)
        # past vertical margin?
        if pos[1] + args.marker_length > paper_height - args.margins:
            pos = (args.margins, args.margins)
            surface.showPage()
        img = aruco.drawMarker(aruco_dict, marker, sidePixels=int(mm_to_points(args.marker_length)), borderBits=args.border)
        print(marker, pos)
        surface.drawImage(ImageReader(Image.fromarray(img)), mm_to_points(pos[0]), mm_to_points(pos[1] + label_height))#, args.marker_length, args.marker_length)
        if args.labels:
            surface.drawString(mm_to_points(pos[0]), mm_to_points(pos[1]), str(marker))
        pos = (pos[0] + args.marker_length + args.spacing, pos[1])

        # debug
#        cv2.imwrite("marker_%d.jpg" % marker, img)

    surface.showPage()
    surface.save()
#    cv2.destroyAllWindows()

