from tkinter import *
import random

# ----------------------------------------------------------------------------------------------------------------------
root = Tk()
root.title("Морський бій")
root.geometry("1500x600")
root.resizable(True, True)

about_ship = "1 корабель — ряд із 4 клітин («лінкор», або «чотирипалубний»)\n" \
             "2 кораблі — ряд із 3 клітин («крейсери», або «трипалубні»)\n" \
             "3 кораблі — ряд із 2 клітин («есмінці», або «двопалубні»)\n" \
             "4 кораблі — 1 клітина («підводні човни», або «однопалубні»)"
Label(root, text=about_ship, font=("Times New Roman", 14)).place(x=0, y=400)
Label(root, text="Ваше полотно", font=("Times New Roman", 14)).place(x=110, y=0)
Label(root, text="Полотно суперника", font=("Times New Roman", 14)).place(x=1070, y=0)

test = 1
ship = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
i = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
j = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
x, y, yi, xj = 0, 0, 0, 0

coordinate_ship_2 = []

ship_canvas = Canvas(root, width=602, height=700, bg="lightblue")
ship_canvas.place(x=20, y=60)

ship_var_pole = Canvas(root, width=300, height=300, bg="blue")
ship_var_pole.place(x=20, y=60)

ship_canvas.create_window(153, 153, window=ship_var_pole, width=300, height=300)

ship_var_pole_2 = Canvas(root, width=300, height=300, bg="blue")
ship_var_pole_2.place(x=1003, y=63)

for line in range(9):
    yi += 30
    ship_var_pole.create_line(0, yi, 300, yi)
    ship_var_pole_2.create_line(0, yi, 300, yi)

for line in range(9):
    xj += 30
    ship_var_pole.create_line(xj, 0, xj, 300)
    ship_var_pole_2.create_line(xj, 0, xj, 300)

for element in i:
    x += 30
    Label(root, text=f'{element}', font=("Times New Roman", 12)).place(x=x, y=40)
    Label(root, text=f'{element}', font=("Times New Roman", 12)).place(x=980+x, y=40)

for element in j:
    y += 30
    Label(root, text=f'{element}', font=("Times New Roman", 12)).place(x=0, y=36+y)
    Label(root, text=f'{element}', font=("Times New Roman", 12)).place(x=980, y=36+y)


# ----------------------------------------------------------------------------------------------------------------------
coordinate_ship = []
coordinate_ship_2 = []


def click(event):
    x11, y11 = event.x % 30, event.y % 30
    x1, y1 = event.x - x11, event.y - y11
    x2, y2 = x1 + 30, y1 + 30

    coordinate_ship.append([x1, y1, x2, y2])
    print(coordinate_ship)

    ship_var_pole.create_rectangle(x1, y1, x2, y2, fill="gray", tags="ship")

    for i in range(len(coordinate_ship)):
        for j in range(i + 1, len(coordinate_ship)):
            if coordinate_ship[i] == coordinate_ship[j]:
                print(f"{coordinate_ship[i]} дублюється в позиціях {i} та {j}")
                ship_var_pole.create_rectangle(coordinate_ship[i], fill="blue", tags="ship")
                coordinate_ship.remove(coordinate_ship[i])
                coordinate_ship.remove(coordinate_ship[j - 1])


def click_2(event):
    x11, y11 = event.x % 30, event.y % 30
    x1, y1 = event.x - x11, event.y - y11
    x2, y2 = x1 + 30, y1 + 30

    coordinate_ship_2.append([x1, y1, x2, y2])
    print(coordinate_ship_2)

    ship_var_pole_2.create_rectangle(x1, y1, x2, y2, fill="gray")

    for i in range(len(coordinate_ship_2)):
        for j in range(i + 1, len(coordinate_ship_2)):
            if coordinate_ship_2[i] == coordinate_ship_2[j]:
                print(f"{coordinate_ship_2[i]} дублюється в позиціях {i} та {j}")
                coordinate_ship_2.remove(coordinate_ship_2[i])


ship_var_pole_2.bind("<Button-1>", click_2)
# ship_var_pole.bind("<Button-1>", click)


# ----------------------------------------------------------------------------------------------------------------------
def clear_pole():
    ship_var_pole.delete("ship")
    ship_canvas.delete("chip_to_place")


def random_place_ship():
    clear_pole()
    occupied_cells = []

    for ship_size in ship:
        safe_zone = ship_size + 1

        while True:
            is_horizontal = random.choice([True, False])
            x = random.randint(0, 9)
            y = random.randint(0, 9)

            if is_horizontal:
                if x + safe_zone > 10:
                    continue
            else:
                if y + safe_zone > 10:
                    continue

            # перевірка на перетин з іншими кораблями
            peretun = False
            for i in range(-1, safe_zone):
                for j in range(-1, safe_zone):
                    cell = (x + i, y + j)
                    if cell in occupied_cells:
                        peretun = True
                        break

            if not peretun:
                break

        for i in range(ship_size):
            if is_horizontal:
                occupied_cells.append((x + i, y))
            else:
                occupied_cells.append((x, y + i))

        if is_horizontal:
            ship_var_pole.create_rectangle(30*x, 30*y, 30*x+30*ship_size, 30*y+30, fill="gray", tags="ship")
        else:
            ship_var_pole.create_rectangle(30*x, 30*y, 30*x+30, 30*y+30*ship_size, fill="gray", tags="ship")


def himself_place_ship():
    clear_pole()

    list_with_ship_to_add = []
    y = 310
    count_of_ship = 0

    for ship_4_2 in ship:
        width = 30 * count_of_ship
        start_weight = 30 * ship_4_2

        list_with_ship_to_add.append([0, y + width, start_weight, y + 30 + width])

        x0, y0, x1, y1 = 0, y + width, start_weight, y + 30 + width
        ship_canvas.create_rectangle(x0, y0, x1, y1, fill="black", tags="chip_to_place")

        count_of_ship += 1
        y += 5

    ship_canvas.bind("<Button-1>", clic_to_get_ship)
    ship_canvas.bind("<B1-Motion>", relocation_himself)
    ship_canvas.bind("<Double-1>", clic_to_revers_ship)


r_p_s_button = Button(root, text="r_p_s", command=random_place_ship)
r_p_s_button.place(x=200, y=400)
r_p_s_button = Button(root, text="h_p_s", command=himself_place_ship)
r_p_s_button.place(x=200, y=440)


# ----------------------------------------------------------------------------------------------------------------------
is_reversed = False
selected_item = 0


def clic_to_revers_ship(event):
    global selected_item, is_reversed
    if selected_item:
        x0, y0, x1, y1 = ship_canvas.coords(selected_item)
        width = x1 - x0
        height = y1 - y0
        if is_reversed:
            ship_canvas.coords(selected_item, x0, y0, x0 + width, y0 + height)
            is_reversed = False
        else:
            ship_canvas.coords(selected_item, x0, y0, x0 + height, y0 + width)
            is_reversed = True
    else:
        pass


def relocation_himself(event):
    global ship_place, selected_item
    ship_var_pole.delete("spam_ship")
    x, y = event.x, event.y

    if selected_item:
        x0, y0, x1, y1 = ship_canvas.coords(selected_item)
        width = x1 - x0
        height = y1 - y0
        ship_canvas.coords(selected_item, x - offset_x, y - offset_y, x + width - offset_x, y + height - offset_y)
        ship_place = ship_var_pole.create_rectangle(x-offset_x, y-offset_y, x+width-offset_x, y+height-offset_y,
                                                    tags="spam_ship", fill="yellow")
    else:
        pass


def clic_to_get_ship(event):
    global selected_item, offset_x, offset_y
    selected_item = ship_canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if selected_item:
        x0, y0, x1, y1 = ship_canvas.coords(selected_item)
        offset_x = event.x - x0
        offset_y = event.y - y0
    else:
        pass


root.mainloop()
