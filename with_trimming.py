from PIL import ImageDraw, Image, ImageFont
from math import sqrt, atan
import shapely.geometry as sh

font = ImageFont.truetype("arial.ttf", 20)

x = [100, 100, 1100, 1300, 1350, 1350, 1100, 1100, 900, 900]
y = [550, 950, 950, 1000, 900, 750, 750, 150, 150, 550]

xy1 = []
xy2 = []

max_x = max(x)
min_x = min(x)
max_y = max(y)
min_y = min(y)
dict_point = {}

for k in range(len(x)):
    xy = (x[k], y[k])
    xy1.append(xy)
    dict_point[k + 1] = [x[k], y[k]]

dx = 33
dy = 13

img1 = Image.new("RGB", (int((max_x - min_x) * 1.8), int((max_y - min_y) * 1.8)), color="white")
ImageDraw.Draw(img1).polygon(xy1, fill="white", outline="blue")  # рисуем комнату

room = sh.Polygon(sh.LinearRing(xy1))

check_x = min_x
index_x = 0

while check_x < max_x:
    check_y = min_y
    index_y = 0
    while check_y < max_y:
        coord = [
            (min_x + index_x * dx, min_y + index_y * dy),
            (min_x + index_x * dx, min_y + (index_y + 1) * dy),
            (min_x + (index_x + 1) * dx, min_y + (index_y + 1) * dy),
            (min_x + (index_x + 1) * dx, min_y + index_y * dy),
        ]
        b = sh.Polygon(sh.LinearRing(coord))
        if b.intersects(room) and not b.touches(room):
            ImageDraw.Draw(img1).polygon(coord, fill=None, outline="black")
        check_y += dy
        index_y += 1
    check_x += dx
    index_x += 1

i = 0
z = 0
dict_angle = {}

while i < (len(x)):
    deltax1 = x[z] - x[z - 1]
    deltay1 = y[z] - y[z - 1]
    print(f'дельты х больше нуля? {deltax1 >= 0}, {deltax1}')
    print(f'дельты y больше нуля? {deltay1 >= 0}, {deltay1}')
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
    print(f'angle линии {i + 1}-{z + 2} = {angle}')
    dict_angle[i + 1] = angle
    z += 1
    if z == (len(x)):
        z = 0
    i += 1
    print('----------')

img3 = ImageDraw.Draw(img1)

i = 0
print(dict_angle)
while i < (len(x)):
    length = sqrt((x[i] - x[i - 1]) ** 2 + ((y[i] - y[i - 1]) ** 2))
    print(dict_angle[i + 1])

    if dict_angle[i + 1] == 90:
        img3.text(
            (((x[i - 1] + x[i]) / 2) - 60, (y[i - 1] + y[i]) / 2),
            f'{round(length, 3)}', font=font, fill='black', align="left"
        )
        print(f'сработало на точке {i + 1}')
    elif dict_angle[i + 1] == 180:
        img3.text(
            (((x[i - 1] + x[i]) / 2), ((y[i - 1] + y[i]) / 2) - 25),
            f'{round(length, 3)}', font=font, fill='black', align="left"
        )
        print(f'сработало на точке {i + 1}')
    else:
        img3.text(
            ((x[i - 1] + x[i]) / 2, (y[i - 1] + y[i]) / 2),
            f'{round(length, 3)}', font=font, fill='black', align="left"
        )
    print('------')
    i += 1

i = 0
z = 1
summa = 0
raznost = 0
while i < (len(x)):
    iteracia_sum = x[i] * y[z]
    iteracia_raz = x[z] * y[i]
    summa += iteracia_sum
    raznost += iteracia_raz
    z += 1
    if z == (len(x)):
        z = 0
    i += 1
doskaS = dx * dy

S = 0.5 * abs((summa - raznost))

img3.text(
    (int((max_x - min_x) * 0.3), int((max_y - min_y) * 1.5)),
    f'общая площадь: {round((S / 10000), 2)} м2, на неё нужно {int((S / doskaS) * 1.03)}\
    досок заданного размера(с запасом 3%)',
    font=font,
    fill='black',
    align="left"
)

img3.line([(max_x, int(max_y * 1.05)), (min_x, int(max_y * 1.05))], fill='green', width=2)  # рисуем линию нижнюю
img3.line([(int(max_x * 1.1), max_y), (int(max_x * 1.1), min_y)], fill='green', width=2)  # рисуем правую линию

ImageDraw.Draw(img1).polygon(xy1, fill=None, outline="blue")
obj = img1.load()  # вроде как какой-то обьект для получения пикселей
room_rgb = obj[xy1[0][0], xy1[0][1]]  # rgb контура комнаты

count = 0  # счетчик

# двигаемся в какую нить сторону, сравниваем цвет пикселя с цветом контура
while obj[(max_x, int(max_y * 1.05) - count)] != room_rgb:
    count += 1 # считаем кол-во пикселей
img3.line([(max_x, int(max_y * 1.05) - count), (max_x, int(max_y * 1.05))], fill='green', width=2)  # рисуем линию

# дальше точно также
count = 0
while obj[(min_x, int(max_y * 1.05) - count)] != room_rgb:
    count += 1
img3.line([(min_x, int(max_y * 1.05) - count), (min_x, int(max_y * 1.05))], fill='green', width=2)

count = 0
while obj[(int(max_x * 1.1) - count, max_y)] != room_rgb:
    count += 1
img3.line([(int(max_x * 1.1) - count, max_y), (int(max_x * 1.1), max_y)], fill='green', width=2)

count = 0
while obj[(int(max_x * 1.1) - count, min_y)] != room_rgb:
    count += 1
img3.line([(int(max_x * 1.1) - count, min_y), (int(max_x * 1.1), min_y)], fill='green', width=2)

img3.text(
    (int((max_x + min_x) / 2), int(max_y * 1.06)),
    f'{max_x - min_x}',
    font=font,
    fill='black',
    align="left",
)

img3.text(
    (int(max_x * 1.11), int((max_y + min_y) / 2)),
    f'{max_y - min_y}',
    font=font,
    fill='black',
    align="left",
)

img1.save("with.png")
