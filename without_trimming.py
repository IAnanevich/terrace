from math import sqrt, atan
from PIL import ImageDraw, Image, ImageFont

font = ImageFont.truetype("arial.ttf", 20)  # Font using to display sizes

"""
Given coordinates to build a polygon & Given sizes of a plank (here for example)
"""
x = [100, 100, 1100, 1300, 1350, 1350, 1100, 1100, 900, 900]
y = [550, 950, 950, 1000, 900, 750, 750, 150, 150, 550]
plank_length = 33
plank_width = 13


"""
Max & min coordinates
"""
max_x_coord = max(x)
min_x_coord = min(x)
max_y_coord = max(y)
min_y_coord = min(y)

"""
List with sets of coordinates to build a polygon & List of coordinates to build rectangle
"""
polygon_coord = [(x[k], y[k]) for k in range(len(x))]
rectangle_coord = [min_x_coord, min_y_coord, min_x_coord, max_y_coord, max_x_coord, max_y_coord, max_x_coord,
                   max_y_coord]

"""
Creating blank image, drawing a circuit & rectangle on it
"""
img1 = Image.new("RGB", (int((max_x_coord - min_x_coord) * 1.8), int((max_y_coord - min_y_coord) * 1.8)), color="white")
img2 = Image.new("RGB", (int((max_x_coord - min_x_coord) * 1.8), int((max_y_coord - min_y_coord) * 1.8)),
                 color="white")  # Rectangle
ImageDraw.Draw(img1).polygon(polygon_coord, fill="white", outline="black")  # Polygon

"""
Function to draw exact amount of planks
"""
def draw(amount_x: int, amount_y: int) -> None:
    for j in range(amount_x):
        for i in range(amount_y):
            ImageDraw.Draw(img2).polygon(
                (
                    min_x_coord + j * plank_length, min_y_coord + i * plank_width,
                    min_x_coord + j * plank_length, min_y_coord + (i + 1) * plank_width,
                    min_x_coord + (j + 1) * plank_length, min_y_coord + (i + 1) * plank_width,
                    min_x_coord + (j + 1) * plank_length, min_y_coord + i * plank_width
                ),
                fill="white",
                outline="black"
            )

"""
Drawing planks in rectangle
"""
if not (max_x_coord - min_x_coord) % plank_length:
    if not (max_y_coord - min_y_coord) % plank_width:
        draw((max_x_coord - min_x_coord) // plank_length,
             (max_y_coord - min_y_coord) // plank_width)    # Full in rectangle
    else:
        draw((max_x_coord - min_x_coord) // plank_length,
             (max_y_coord - min_y_coord) // plank_width + 1)    # Doesn't fit on the right
else:
    if not (max_y_coord - min_y_coord) % plank_width:
        draw((max_x_coord - min_x_coord) // plank_length + 1,
             (max_y_coord - min_y_coord) // plank_width)    # Doesn't fit on the bottom
    else:
        draw((max_x_coord - min_x_coord) // plank_length + 1,
             (max_y_coord - min_y_coord) // plank_width + 1)  # Doesn't fit anywhere

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
    deltax1 = x[i] - x[i - 1]
    deltay1 = y[i] - y[i - 1]
    if deltax1 == 0:
        rumb = 90
    else:
        rumb = atan(abs(deltay1 / deltax1))

    if deltax1 >= 0 and deltay1 >= 0:
        angle = rumb
    if deltax1 < 0 and deltay1 >= 0:
        angle = 180 - rumb
    if deltax1 < 0 and deltay1 < 0:
        angle = rumb - 180
    if deltax1 >= 0 and deltay1 < 0:
        angle = 360 - rumb
    dict_angle[angle_index + 1] = angle
    i += 1
    if i == (len(x)):
        i = 0
    angle_index += 1

"""
Creating mask, filling in with rectangle, impose on circuit, show
"""
mask = Image.new("L", img2.size, 0)
tmp = ImageDraw.Draw(mask)
tmp.polygon(polygon_coord, fill=255)
img = Image.composite(img2, img1, mask)
img3 = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 20)


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
while angle_index < (len(x)):
    iter_sum = x[angle_index] * y[i]
    iter_diff = x[i] * y[angle_index]
    sum += iter_sum
    diff += iter_diff
    i += 1
    if i == (len(x)):
        i = 0
    angle_index += 1
plank_area = plank_length * plank_width

"""
Count area of planks needed
"""
area = 0.5 * abs((sum - diff))

"""
Result text display
"""
img3.text(
    (int((max_x_coord - min_x_coord) * 0.3), int((max_y_coord - min_y_coord) * 1.5)),
    f'общая площадь: {round((area / 10000), 2)} м2, на неё нужно {int((area / plank_area) * 1.03)}\
    досок заданного размера(с запасом 3%)',
    font=font,
    fill='black',
    align="left"
)

"""
Drawing circuit
"""
ImageDraw.Draw(img).polygon(polygon_coord, fill=None, outline="blue")

"""
Draw outer lines (parallel to polygon) for size display
"""
img3.line([(max_x_coord, int(max_y_coord * 1.05)), (min_x_coord, int(max_y_coord * 1.05))], fill='green', width=2)
img3.line([(int(max_x_coord * 1.1), max_y_coord), (int(max_x_coord * 1.1), min_y_coord)], fill='green', width=2)

"""
Getting object with stored pixels of image
"""
obj = img.load()
room_rgb = obj[polygon_coord[0][0], polygon_coord[0][1]]

"""
Connecting outer lines with polygon to display sizes
"""
count = 0
while obj[(max_x_coord, int(max_y_coord * 1.05) - count)] != room_rgb:
    count += 1  # Count pixels
img3.line([(max_x_coord, int(max_y_coord * 1.05) - count), (max_x_coord, int(max_y_coord * 1.05))],
          fill='green', width=2)
count = 0
while obj[(min_x_coord, int(max_y_coord * 1.05) - count)] != room_rgb:
    count += 1
img3.line([(min_x_coord, int(max_y_coord * 1.05) - count), (min_x_coord, int(max_y_coord * 1.05))],
          fill='green', width=2)
count = 0
while obj[(int(max_x_coord * 1.1) - count, max_y_coord)] != room_rgb:
    count += 1
img3.line([(int(max_x_coord * 1.1) - count, max_y_coord), (int(max_x_coord * 1.1), max_y_coord)],
          fill='green', width=2)
count = 0
while obj[(int(max_x_coord * 1.1) - count, min_y_coord)] != room_rgb:
    count += 1
img3.line([(int(max_x_coord * 1.1) - count, min_y_coord), (int(max_x_coord * 1.1), min_y_coord)],
          fill='green', width=2)
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
img.save("without.png")
