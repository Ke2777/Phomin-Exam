import random
import os

from PIL import Image, ImageDraw
from math import sqrt

# defines
n = 5  # count of layers
height = 1000  # height of layer
width = 1000  # width of layer


class Point:
    x: float
    y: float

class Layer:
    count: int  # count of points
    points: list

class Layers:
    count: int
    layer: list

class Images:
    count: int
    images: list


def lerp(a: float, b: float, t: float) -> float: 
    return a * (1.0 - t) + b * t

def unlerp(x: float, x0: float, x1: float) -> float:
    return (x - x0) / (x1 - x0)

def map(x: float, x0: float, x1: float, a: float, b: float) -> float:
    t = unlerp(x, x0, x1)
    return lerp(a, b, t)


def load_images(images, path):
    im  = []
    for i in range(images.count):
        with open(os.path.join(path, f'layer-{i}-a.raw'), 'rb') as f:
            im.append(list(f.read()))
    images.images = im

def find_points(images, l):
    layers = []
    for i in range(images.count):
        points = []
        for y in range(height):
            for x in range(width):
                p = x + y * width  # point
                if images.images[i][p] < 127:  # black point?
                    """
                    The center of the sheet is at the origin (x = 0, y = 0). The top left corner has coordinates (x = -0.5, y = +0.5). 
                    The X axis is directed to the right, Y is upward.
                    """
                    point = Point()
                    point.x = float(x) / float(width - 1) - 0.5
                    point.y = float(y) / float(height - 1) - 0.5
                    points.append(point)
        layer = Layer()
        layer.count = len(points)
        layer.points = points
        layers.append(layer)
    l.count = len(layers)
    l.layer = layers

def draw_layer(layers, size: tuple) -> None:
    for i in range(layers.count):
        img = Image.new('RGB', size, color='white')
        draw = ImageDraw.Draw(img)

        # draw axes 
        draw.line((size[0] / 2, 0, size[0] / 2, (size[1]) / 2 + 50), fill=(0, 0, 255, 255))  # y 
        draw.line(((size[0] / 2) - 50, size[1] / 2, size[0], size[1] / 2), fill=(255, 0, 0, 255))  # x

        for lay in range(layers.layer[i].count - 1):
            # draw point (x = -0.5, y = +0.5)
            hline = 8
            px = layers.layer[i].points[lay].x
            py = layers.layer[i].points[lay].y
            x = map(px, -0.5, 0.5, 0, size[0])
            y = map(py, 0.5, -0.5, size[1], 0)
            draw.line((x - hline, y - hline, x + hline, y + hline), fill=(0, 0, 255, 255)) # rgba 
            draw.line((x + hline, y - hline, x - hline, y + hline), fill=(0, 0, 255, 255))

        dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        img.save(os.path.join(os.path.join(dirname, 'examples'), f'layers-{i}-a.png'))


def found_inliers(iterations, tolerance, allpoints, number):
    maximum_inlierscount = 0
    best_model = []
    for iteration in range(iterations):
        # generate a random points
        point1 = random.randint(0, len(allpoints) - 1)
        point2 = random.randint(0, len(allpoints) - 1)

        d = allpoints[point1].x + allpoints[point2].y 

        # find the count of points lying within tolerance of this line
        inlierscount = 0
        line = []
        for i in range(0, len(allpoints)):
            distance = abs(allpoints[i].x + allpoints[i].y - d)
            if distance < tolerance:
                line.append([allpoints])
                inlierscount += 1
        if inlierscount > maximum_inlierscount:
            maximum_inlierscount = inlierscount
            best_model = [allpoints[point1], allpoints[point2]]

    p1x = map(best_model[0].x, -0.5, 0.5, 0, 512)
    p1y = map(best_model[0].y, 0.5, -0.5, 512, 0)
    p2x = map(best_model[1].x, -0.5, 0.5, 0, 512)
    p2y = map(best_model[1].y, 0.5, -0.5, 512, 0)

    # draw line
    img = Image.open(f'examples/layers-{number}-a.png')
    draw = ImageDraw.Draw(img)
    draw.line((p1x, p1y, p2x, p2y), fill=(0, 255, 0, 255))
    img.save(f'examples/test-{number}.png')

def main():
    # path to folder with layers
    layers_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'layers')

    # loads all images
    images = Images()
    images.count = n
    load_images(images, layers_path)


    # find all points
    layers = Layers()
    find_points(images, layers)


    # output layers and points and point coordinates
    print("layer\tpoint\tx\ty")
    for i in range(layers.count):
        for lay in range(layers.layer[i].count):
            print(f'{i}\t{lay}\t{round(layers.layer[i].points[lay].x, 2)}\t{round(layers.layer[i].points[lay].y, 2)}')

    # draw points
    im_width = 512
    im_height = 512
    size = (im_width, im_height)
    draw_layer(layers, size)

    '''
    # find inliers
    for lay in range(layers.count):
        allpoints = []
        for point in range(layers.layer[lay].count):
            allpoints.append(layers.layer[lay].points[point])
        found_inliers(100, tolerance=0.3, allpoints=allpoints, number=lay)
    '''
    allpoints = []
    for lay in range(layers.count):
        for point in range(layers.layer[lay].count):
            allpoints.append(layers.layer[lay].points[point])
    #found_inliers(100, tolerance=0.3, allpoints=allpoints, number=)

if __name__ == '__main__':
    main()