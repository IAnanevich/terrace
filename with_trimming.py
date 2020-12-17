from PIL import ImageDraw, Image, ImageFont
from math import sqrt, atan
from shapely.geometry import Polygon, LinearRing

font = ImageFont.truetype("arial.ttf", 20)  # Font using to display sizes

"""
Given coordinates to build a polygon & Given sizes of a plank (here for example)
"""
x = [100, 100, 1100, 1300, 1350, 1350, 1100, 1100, 900, 900]
y = [550, 950, 950, 1000, 900, 750, 750, 150, 150, 550]
plank_length = 33
plank_width = 13

"""
List with sets of coordinates to build a polygon
"""
polygon_coord = [(x[k], y[k]) for k in range(len(x))]

"""
Max & min coordinates
"""
max_x_coord = max(x)
min_x_coord = min(x)
max_y_coord = max(y)
min_y_coord = min(y)

"""
Creating a blank image
"""
img1 = Image.new("RGB", (int((max_x_coord - min_x_coord) * 1.8), int((max_y_coord - min_y_coord) * 1.8)), color="white")
ImageDraw.Draw(img1).polygon(polygon_coord, fill="white", outline="blue")

"""
Creating circuit using polygon
"""
circuit = Polygon(LinearRing(polygon_coord))

"""
Temporary variables
"""
x_coord_check = min_x_coord
count_x = 0

"""
Building up plank by plank from minimal values to maximum
"""
while x_coord_check < max_x_coord:
    y_coord_check = min_y_coord
    count_y = 0
    while y_coord_check < max_y_coord:
        coord = [
            (min_x_coord + count_x * plank_length, min_y_coord + count_y * plank_width),
            (min_x_coord + count_x * plank_length, min_y_coord + (count_y + 1) * plank_width),
            (min_x_coord + (count_x + 1) * plank_length, min_y_coord + (count_y + 1) * plank_width),
            (min_x_coord + (count_x + 1) * plank_length, min_y_coord + count_y * plank_width),
        ]
        b = Polygon(LinearRing(coord))
        """
        Checking if plank in circuit -> draw
        """
        if b.intersects(circuit) and not b.touches(circuit):
            ImageDraw.Draw(img1).polygon(coord, fill=None, outline="black")
        y_coord_check += plank_width
        count_y += 1
    x_coord_check += plank_length
    count_x += 1

"""
Temporary variables
"""
angle_index = 0
i = 0

"""
Dictionary with all angles (to display text right)
"""
dict_angle = {}

"""
Filling in dictionary
"""
while angle_index < (len(x)):
    delta_x = x[i] - x[i - 1]
    delta_y = y[i] - y[i - 1]
    if delta_x == 0:
        value = 90
    else:
        value = atan(abs(delta_y / delta_x))

    if delta_x >= 0 and delta_y >= 0:
        angle = value
    if delta_x < 0 and delta_y >= 0:
        angle = 180 - value
    if delta_x < 0 and delta_y < 0:
        angle = value - 180
    if delta_x >= 0 and delta_y < 0:
        angle = 360 - value
    dict_angle[angle_index + 1] = angle
    i += 1
    if i == (len(x)):
        i = 0
    angle_index += 1


"""
Image to display text on
"""
img3 = ImageDraw.Draw(img1)


"""
Display text with length on each line
"""
angle_index = 0
while angle_index < (len(x)):
    length = sqrt((x[angle_index] - x[angle_index - 1]) ** 2 + ((y[angle_index] - y[angle_index - 1]) ** 2))
    if dict_angle[angle_index + 1] == 90:
        img3.text(
            (((x[angle_index - 1] + x[angle_index]) / 2) - 60, (y[angle_index - 1] + y[angle_index]) / 2),
            f'{round(length, 3)}', font=font, fill='black', align="left"
        )
    elif dict_angle[angle_index + 1] == 180:
        img3.text(
            (((x[angle_index - 1] + x[angle_index]) / 2), ((y[angle_index - 1] + y[angle_index]) / 2) - 25),
            f'{round(length, 3)}', font=font, fill='black', align="left"
        )
    else:
        img3.text(
            ((x[angle_index - 1] + x[angle_index]) / 2, (y[angle_index - 1] + y[angle_index]) / 2),
            f'{round(length, 3)}', font=font, fill='black', align="left"
        )
    angle_index += 1

"""
Temporary variables
"""
angle_index = 0
i = 1
sum = 0
diff = 0

"""
Count all planks needed
"""
while angle_index < (len(x)):
    iter_sum = x[angle_index] * y[i]
    iter_diff = x[i] * y[angle_index]
    sum += iter_sum
    diff += iter_diff
    i += 1
    if i == (len(x)):
        i = 0
    angle_index += 1
planks_amount = plank_length * plank_width

"""
Count area of planks needed
"""
area = 0.5 * abs((sum - diff))


"""
Result text display
"""
img3.text(
    (int((max_x_coord - min_x_coord) * 0.3), int((max_y_coord - min_y_coord) * 1.5)),
    f'общая площадь: {round((area / 10000), 2)} м2, на неё нужно {int((area / planks_amount) * 1.03)}\
    досок заданного размера(с запасом 3%)',
    font=font,
    fill='black',
    align="left"
)


"""
Draw outer lines (parallel to polygon) for size display
"""
img3.line([(max_x_coord, int(max_y_coord * 1.05)), (min_x_coord, int(max_y_coord * 1.05))], fill='green', width=2)
img3.line([(int(max_x_coord * 1.1), max_y_coord), (int(max_x_coord * 1.1), min_y_coord)], fill='green', width=2)

"""
Getting object with stored pixels of image
"""
obj = img1.load()
room_rgb = obj[polygon_coord[0][0], polygon_coord[0][1]]

"""
Connecting outer lines with polygon to display sizes
"""
count = 0
while obj[(max_x_coord, int(max_y_coord * 1.05) - count)] != room_rgb:
    count += 1  # Count pixels
img3.line([(max_x_coord, int(max_y_coord * 1.05) - count), (max_x_coord, int(max_y_coord * 1.05))], fill='green', width=2)  # рисуем линию
count = 0
while obj[(min_x_coord, int(max_y_coord * 1.05) - count)] != room_rgb:
    count += 1
img3.line([(min_x_coord, int(max_y_coord * 1.05) - count), (min_x_coord, int(max_y_coord * 1.05))], fill='green', width=2)
count = 0
while obj[(int(max_x_coord * 1.1) - count, max_y_coord)] != room_rgb:
    count += 1
img3.line([(int(max_x_coord * 1.1) - count, max_y_coord), (int(max_x_coord * 1.1), max_y_coord)], fill='green', width=2)
count = 0
while obj[(int(max_x_coord * 1.1) - count, min_y_coord)] != room_rgb:
    count += 1
img3.line([(int(max_x_coord * 1.1) - count, min_y_coord), (int(max_x_coord * 1.1), min_y_coord)], fill='green', width=2)
img3.text(
    (int((max_x_coord + min_x_coord) / 2), int(max_y_coord * 1.06)),
    f'{max_x_coord - min_x_coord}',
    font=font,
    fill='black',
    align="left",
)
img3.text(
    (int(max_x_coord * 1.11), int((max_y_coord + min_y_coord) / 2)),
    f'{max_y_coord - min_y_coord}',
    font=font,
    fill='black',
    align="left",
)

"""
Saving image
"""
img1.save("with.png")
