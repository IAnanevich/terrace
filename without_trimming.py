from math import sqrt, atan
from PIL import ImageDraw, Image, ImageFont

color = 'white'


def draw(amount_x: int, amount_y: int) -> None:
    for j in range(amount_x):
        for i in range(amount_y):
            ImageDraw.Draw(img2).polygon(
                (
                    min_x + j * dx, min_y + i * dy,
                    min_x + j * dx, min_y + (i + 1) * dy,
                    min_x + (j + 1) * dx, min_y + (i + 1) * dy,
                    min_x + (j + 1) * dx, min_y + i * dy
                ),
                fill=color,
                outline="black"
            )


x = [100, 100, 1100, 1300, 1350, 1350, 1100, 1100, 900, 900]
y = [550, 950, 950, 1000, 900, 750, 750, 150, 150, 550]

# x = [200, 200, 500, 500, 900, 900, 500, 500]  # x1, x2, x3, x4, x5, x6
# y = [200, 500, 500, 800, 800, 300, 300, 200]  # y1, y2, y3, y4, y5, y6


# x = [100, 100, 500, 500, 1005, 1005]  # x1, x2, x3, x4, x5, x6
# y = [100, 400, 400, 605, 605, 100]  # y1, y2, y3, y4, y5, y6


xy1 = []  # для построения комнаты
xy2 = []  # для построения прямоугольника комнаты
dict_point = {}
for k in range(len(x)):  # заполнение списка для комнаты
    xy1.append(x[k])
    xy1.append(y[k])
    dict_point[k + 1] = [x[k], y[k]]

max_x = max(x)  # нахождение углов прямоугольника
min_x = min(x)
max_y = max(y)
min_y = min(y)

xy2.append(min_x)  # заполнение для построения прямоугольника
xy2.append(min_y)
xy2.append(min_x)
xy2.append(max_y)
xy2.append(max_x)
xy2.append(max_y)
xy2.append(max_x)
xy2.append(min_y)

dx = 33  # длина доски
dy = 13  # ширина доски

# изображение с комнатой
img1 = Image.new("RGB", (int((max_x - min_x) * 1.8), int((max_y - min_y) * 1.8)), color="white")
img2 = Image.new("RGB", (int((max_x - min_x) * 1.8), int((max_y - min_y) * 1.8)), color="white")  # прямоугольник
ImageDraw.Draw(img1).polygon(xy1, fill="white", outline="black")  # рисуем комнату

if not (max_x - min_x) % dx:  # кладем доски
    if not (max_y - min_y) % dy:
        draw((max_x - min_x) // dx, (max_y - min_y) // dy)  # не вылезет
    else:
        draw((max_x - min_x) // dx, (max_y - min_y) // dy + 1)  # вылезет справа
else:
    if not (max_y - min_y) % dy:
        draw((max_x - min_x) // dx + 1, (max_y - min_y) // dy)  # вылезет снизу
    else:
        draw((max_x - min_x) // dx + 1, (max_y - min_y) // dy + 1)  # везде

ImageDraw.Draw(img2).polygon(xy2, fill=None, outline="black")  # рисуем прямоугольник

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

mask = Image.new("L", img2.size, 0)  # создаем маску
tmp = ImageDraw.Draw(mask)  # на маске рисуем tmp
tmp.polygon(xy1, fill=255)  # заполяем tmp комнатой
img = Image.composite(img2, img1, mask)  # отображаем
img3 = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 20)
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

ImageDraw.Draw(img).polygon(xy1, fill=None, outline="blue")  # контур комнаты

img3.line([(max_x, int(max_y * 1.05)), (min_x, int(max_y * 1.05))], fill='green', width=2)  # рисуем линию нижнюю
img3.line([(int(max_x * 1.1), max_y), (int(max_x * 1.1), min_y)], fill='green', width=2)  # рисуем правую линию

obj = img.load()  # вроде как какой-то обьект для получения пикселей
room_rgb = obj[xy1[0], xy1[1]]  # rgb контура комнаты

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

img.save("without.png")

