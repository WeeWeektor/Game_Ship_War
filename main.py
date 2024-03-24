from tkinter import *
from tkinter import messagebox
from email_validator import validate_email, EmailNotValidError
import webbrowser
import random
import mysql.connector
from mysql.connector import Error
from config import db_config


# ----------------------------------------------------------------------------------------------------------------------
root = Tk()
root.title("Морський бій")
root.geometry("1340x500+250+200")
root.resizable(True, True)

Label(root, text="Ваше полотно", font=("Times New Roman", 14)).place(x=110, y=0)
Label(root, text="Полотно суперника", font=("Times New Roman", 14)).place(x=1070, y=0)

ship = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
i = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
j = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
x, y, yi, xj = 0, 0, 0, 0

window_registration = None
window_user_info = None
rand_place_ship = None
list_with_line = []

ship_var_pole = Canvas(root, width=300, height=300, bg="blue")
ship_var_pole.place(x=20, y=60)

ship_var_pole_2 = Canvas(root, width=300, height=300, bg="blue")
ship_var_pole_2.place(x=1003, y=63)

for line in range(9):
    yi += 30
    ship_var_pole.create_line(0, yi, 300, yi)
    list_with_line.append([0, yi, 300, yi])
    ship_var_pole_2.create_line(0, yi, 300, yi)

for line in range(10):
    xj += 30
    ship_var_pole.create_line(xj, 0, xj, 300)
    list_with_line.append([xj, 0, xj, 300])
    ship_var_pole_2.create_line(xj, 0, xj, 300)

for element in i:
    x += 30
    Label(root, text=f'{element}', font=("Times New Roman", 12)).place(x=x, y=35)
    Label(root, text=f'{element}', font=("Times New Roman", 12)).place(x=980+x, y=40)

for element in j:
    y += 30
    Label(root, text=f'{element}', font=("Times New Roman", 12)).place(x=0, y=36+y)
    Label(root, text=f'{element}', font=("Times New Roman", 12)).place(x=980, y=36+y)


# ----------------------------------------------------------------------------------------------------------------------
coordinate_ship = []
coordinate_ship_2 = []
killed_ships_coordinates = []
chose_another_box = None
won = None


def clear_pole():
    ship_var_pole.delete("ship", "chip_to_place", "kill_my_ship", "cross_line")
    ship_var_pole_2.delete("i_kill_ship", "ship_opponent", "cross_line_opponent")


def click_2(event):
    global chose_another_box, won, get_all_win_war, war_info_list
    chose_another_box = False
    x11, y11 = event.x % 30, event.y % 30
    x1, y1 = event.x - x11, event.y - y11
    x2, y2 = x1 + 30, y1 + 30

    coordinate_ship_2.append((x1, y1, x2, y2))

    for i in range(len(coordinate_ship_2)):
        for j in range(i + 1, len(coordinate_ship_2)):
            if coordinate_ship_2[i] == coordinate_ship_2[j]:
                chose_another_box = True
                # print(f"{coordinate_ship_2[i]} дублюється в позиціях {i} та {j}")
                coordinate_ship_2.remove(coordinate_ship_2[i])

    if chose_another_box:
        pass
    else:
        if won is None:
            if (x1, y1, x2, y2) in opponent_ship:
                index_kill = opponent_ship.index((x1, y1, x2, y2))
                ship_var_pole_2.create_oval(x1, y1, x2, y2, fill="gray", tags="i_kill_ship")
                ship_var_pole_2.create_oval(x1 + 7, y1 + 7, x2 - 7, y2 - 7, fill="black", tags="i_kill_ship")
                opponent_ship.pop(index_kill)

                for elem_ship in ship_list_to_red_del_opponent:
                    if (x1, y1, x2, y2) in elem_ship:
                        elem_ship.remove((x1, y1, x2, y2))
                        if not elem_ship:
                            create_red_line = ship_list_to_red_del_opponent.index(elem_ship)
                            ship_var_pole_2.create_line(list_to_dell_ship_opponent[create_red_line], fill="red", width=3,
                                                        tags="cross_line_opponent")
                            ship_list_to_red_del_opponent.pop(create_red_line)
                            list_to_dell_ship_opponent.pop(create_red_line)
                        else:
                            pass
                    else:
                        pass

                if len(opponent_ship) == 0:
                    won = True
            else:
                ship_var_pole_2.create_oval(x1 + 7, y1 + 7, x2 - 7, y2 - 7, fill="black", tags="i_kill_ship")
                m_b()
        else:
            pass
        if won:
            if authenticated:
                get_all_win_war += 1
                war_info_list.insert(0, f"Бій №{get_all_war} - Виграно.")
            messagebox.showinfo("Перемога", "Ви перемогли")
            ship_var_pole_2.unbind("<Button-1>")
            give_up_button.destroy()
            restart()


# ----------------------------------------------------------------------------------------------------------------------
def random_place_ship():
    global rand_place_ship, occupied_cells
    rand_place_ship = True
    ship_var_pole.configure(width=300)
    clear_pole()
    ship_var_pole.unbind("<Button-1>")
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
            ship_var_pole.create_rectangle(30*x, 30*y, 30*x+30*ship_size, 30*y+30, fill="black", tags="ship")
        else:
            ship_var_pole.create_rectangle(30*x, 30*y, 30*x+30, 30*y+30*ship_size, fill="black", tags="ship")


def himself_place_ship():
    global rand_place_ship, occupied_cells_2, ship_place_pole
    rand_place_ship = False
    ship_var_pole.configure(width=570)
    clear_pole()
    occupied_cells_2 = []
    ship_place_pole = []

    list_with_ship_to_add = []
    x = 330
    y = 10
    count_of_ship = 0
    k = -1

    for ship_4_1 in ship:
        width = 30 * count_of_ship
        width_2 = 30 * k
        start_weight = 30 * ship_4_1

        if count_of_ship >= 5:
            x0, y0, x1, y1 = x+150, y+width_2+5, start_weight+x+150, y+30+width_2+5
            k += 1
        else:
            x0, y0, x1, y1 = x, y + width, start_weight + x, y + 30 + width

        list_with_ship_to_add.append([x0, y0, x1, y1])
        ship_var_pole.create_rectangle(x0, y0, x1, y1, fill="black", tags="chip_to_place")

        count_of_ship += 1
        y += 5

    ship_var_pole.bind("<Button-1>", clic_to_get_ship)
    ship_var_pole.bind("<B1-Motion>", relocation_himself)
    ship_var_pole.bind("<Button-3>", clic_to_revers_ship)
    ship_var_pole.bind("<ButtonRelease-1>", place_to_pole)


def create_ship_opponent():
    global occupied_cells_for_opponent
    occupied_cells_for_opponent = []

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

            peretun = False
            for i in range(-1, safe_zone):
                for j in range(-1, safe_zone):
                    cell = (x + i, y + j)
                    if cell in occupied_cells_for_opponent:
                        peretun = True
                        break

            if not peretun:
                break

        for i in range(ship_size):
            if is_horizontal:
                occupied_cells_for_opponent.append((x + i, y))
            else:
                occupied_cells_for_opponent.append((x, y + i))

        # if is_horizontal:
        #     ship_var_pole_2.create_rectangle(30 * x, 30 * y, 30 * x + 30 * ship_size, 30 * y + 30, fill="black",
        #                                      tags="ship_opponent")
        # else:
        #     ship_var_pole_2.create_rectangle(30 * x, 30 * y, 30 * x + 30, 30 * y + 30 * ship_size, fill="black",
        #                                      tags="ship_opponent")


r_p_s_button = Button(root, text="Згенерувати\nвипадковим\nчином", width=12, bg="black", fg="white",
                      font=("Times New Roman", 12), command=random_place_ship)
r_p_s_button.place(x=40, y=390)
h_p_s_button = Button(root, text="З\nчистого\nлиста", width=12, bg="black", fg="white",
                      font=("Times New Roman", 12), command=himself_place_ship)
h_p_s_button.place(x=180, y=390)


# ----------------------------------------------------------------------------------------------------------------------
is_reversed = False
selected_item = 0


def clic_to_revers_ship(event):
    global selected_item, is_reversed
    ship_var_pole.bind("<Button-3>", clic_to_get_ship(event))

    if selected_item and not rand_place_ship:
        x0, y0, x1, y1 = ship_var_pole.coords(selected_item)
        width = x1 - x0
        height = y1 - y0
        if is_reversed:
            ship_var_pole.coords(selected_item, x0, y0, x0 + width, y0 + height)
            is_reversed = False
        else:
            ship_var_pole.coords(selected_item, x0, y0, x0 + height, y0 + width)
            is_reversed = True
    else:
        pass


def relocation_himself(event):
    global selected_item, relocated_ship
    x, y = event.x, event.y
    if selected_item and not rand_place_ship:
        x0, y0, x1, y1 = ship_var_pole.coords(selected_item)
        width = x1 - x0
        height = y1 - y0
        relocated_ship = ship_var_pole.coords(selected_item,
                                              x - offset_x, y - offset_y, x + width - offset_x, y + height - offset_y)
    else:
        pass


def clic_to_get_ship(event):
    global selected_item, offset_x, offset_y
    if not rand_place_ship:
        selected_item = ship_var_pole.find_overlapping(event.x, event.y, event.x, event.y)
    if selected_item:
        x0, y0, x1, y1 = ship_var_pole.coords(selected_item)
        offset_x = event.x - x0
        offset_y = event.y - y0
        if [x0, y0, x1, y1] in list_with_line:
            selected_item = 0
    else:
        pass


def place_to_pole(event):
    global selected_item, is_reversed, occupied_cells_2, ship_place_pole

    if selected_item and not rand_place_ship:
        x0, y0, x1, y1 = ship_var_pole.coords(selected_item)
        width = x1 - x0
        height = y1 - y0
        x = width // 30
        y = height // 30

        if x > y:
            is_horizontal = True
        else:
            is_horizontal = False

        ship_size = int(x if width > height else y)
        safe_zone = ship_size + 1

        # Знаходимо найближчу допустиму позицію для елемента
        closest_x, closest_y = None, None
        min_distance = float('inf')
        for x in range(10 - ship_size + 1):
            for y in range(10 - safe_zone + 1):
                # Перевіряємо, чи можна розмістити елемент
                can_place = True
                for i in range(ship_size):
                    for j in range(-1, safe_zone):
                        if is_horizontal:
                            cell = (x + i, y + j)
                        else:
                            cell = (x + j, y + i)
                        if cell[0] < 0 or cell[1] < 0 or cell in occupied_cells_2:
                            can_place = False
                            break
                    if not can_place:
                        break

                if can_place:
                    distance = (x - event.x // 30) ** 2 + (y - event.y // 30) ** 2
                    if distance < min_distance:
                        min_distance = distance
                        closest_x, closest_y = x, y

        if closest_x is not None and closest_y is not None:
            # Видаляємо стару позицію елемента з occupied_cells
            old_x, old_y = x0 // 30, y0 // 30
            old_cells = []
            for i in range(ship_size):
                if is_horizontal:
                    old_row = [(old_x + i, old_y - 1), (old_x + i, old_y + 1)]
                    old_cells.extend(old_row)
                    for j in range(-1, 2):
                        old_cells.append((old_x + i + j, old_y))
                else:
                    old_row = [(old_x - 1, old_y + i), (old_x + 1, old_y + i)]
                    old_cells.extend(old_row)
                    for j in range(-1, 2):
                        old_cells.append((old_x, old_y + i + j))

            for cell in old_cells:
                if cell in occupied_cells_2:
                    occupied_cells_2.remove(cell)

            # Оновлюємо координати елемента та додаємо нову позицію до occupied_cells
            if is_horizontal:
                new_x1 = min(30 * closest_x + 30 * ship_size, 300)
                new_y1 = min(30 * closest_y + 30, 300)
                ship_var_pole.coords(selected_item, 30 * closest_x,  30 * closest_y, new_x1, new_y1)
                ship_place_pole.append((30 * closest_x,  30 * closest_y, new_x1, new_y1))
                for i in range(ship_size):
                    occupied_cells_2.extend([(closest_x + i, closest_y - 1), (closest_x + i, closest_y + 1)])
                    for j in range(-1, 2):
                        occupied_cells_2.append((closest_x + i + j, closest_y))

            else:
                new_x1 = min(30 * closest_x + 30, 300)
                new_y1 = min(30 * closest_y + 30 * ship_size, 300)
                ship_var_pole.coords(selected_item, 30 * closest_x, 30 * closest_y, new_x1, new_y1)
                ship_place_pole.append((30 * closest_x, 30 * closest_y, new_x1, new_y1))
                for i in range(ship_size):
                    occupied_cells_2.extend([(closest_x - 1, closest_y + i), (closest_x + 1, closest_y + i)])
                    for j in range(-1, 2):
                        occupied_cells_2.append((closest_x, closest_y + i + j))

            # print(occupied_cells_2)

        else:
            print("Немає доступних позицій для розміщення корабля.")

    else:
        pass


# ----------------------------------------------------------------------------------------------------------------------
def start_war(your_ship, opponent_ship):
    global won, give_up_button, m_b, last_hit_coord, get_all_war
    move_bot_list = []
    count_rand_place_ship = 0
    for i in your_ship:
        count_rand_place_ship += 1

    if count_rand_place_ship < 20:
        restart()
        messagebox.showerror("Помилка", "Не виставлено всіх кораблів спробуйте заново")
    else:
        if authenticated:
            get_all_war += 1
        ship_var_pole.configure(width=300)
        if war_button.bind("<Button-1>", get_true):
            war_button.destroy()
            give_up_button = Button(root, text="Здатися", width=12, height=3, bg="black", fg="white",
                                    font=("Times New Roman", 12), command=give_up)
            give_up_button.place(x=600, y=390)

        ship_var_pole_2.bind("<Button-1>", click_2)

        list_to_dell_ship = []
        for e_s in ship_list_to_red_del:
            xy1 = e_s[0]
            xy2 = e_s[-1]
            list_to_dell_ship.append((xy1[0], xy1[1], xy2[2], xy2[3]))

        def move_bot():
            global won, m_b, last_hit_coord, get_all_loss_war, war_info_list

            def find_next_move(coord):
                x, y = coord
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                random.shuffle(directions)
                for dx, dy in directions:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < 10 and 0 <= new_y < 10 and (
                            new_x * 30, new_y * 30, new_x * 30 + 30, new_y * 30 + 30) not in move_bot_list:
                        return new_x * 30, new_y * 30, new_x * 30 + 30, new_y * 30 + 30
                return None

            while True:
                if last_hit_coord is None:
                    x_ = random.randint(0, 9)
                    y_ = random.randint(0, 9)
                    x1, y1 = x_ * 30, y_ * 30
                    x2, y2 = x1 + 30, y1 + 30
                    move_bot_ = (x1, y1, x2, y2)
                else:
                    move_bot_ = find_next_move(last_hit_coord)
                    if move_bot_ is None:
                        last_hit_coord = None
                        continue

                if move_bot_ not in move_bot_list:
                    move_bot_list.append(move_bot_)
                    break

            if move_bot_ in your_ship:
                index_kill_bot = your_ship.index(move_bot_)
                your_ship.pop(index_kill_bot)
                ship_var_pole.create_oval(move_bot_[0], move_bot_[1], move_bot_[2], move_bot_[3], fill="gray",
                                          tags="kill_my_ship")
                ship_var_pole.create_oval(move_bot_[0] + 7, move_bot_[1] + 7, move_bot_[2] - 7, move_bot_[3] - 7,
                                          fill="black", tags="kill_my_ship")

                for elem_ship in ship_list_to_red_del:
                    if move_bot_ in elem_ship:
                        elem_ship.remove(move_bot_)
                        if not elem_ship:
                            create_red_line = ship_list_to_red_del.index(elem_ship)
                            ship_var_pole.create_line(list_to_dell_ship[create_red_line], fill="red", width=3,
                                                      tags="cross_line")
                            ship_list_to_red_del.pop(create_red_line)
                            list_to_dell_ship.pop(create_red_line)
                            last_hit_coord = None
                        else:
                            last_hit_coord = (move_bot_[0] // 30, move_bot_[1] // 30)
                    else:
                        pass

                move_bot()
                if len(your_ship) == 0:
                    won = False
                    if authenticated:
                        get_all_loss_war += 1
                        war_info_list.insert(0, f"Бій №{get_all_war} - Програно.")
                    restart()
                    give_up_button.destroy()
                    ship_var_pole_2.unbind("<Button-1>")
                    messagebox.showinfo("Поразка", "Ви програли")
            else:
                ship_var_pole.create_oval(move_bot_[0]+7, move_bot_[1]+7, move_bot_[2]-7, move_bot_[3]-7, fill="black",
                                          tags="kill_my_ship")

        if won is None:
            m_b = move_bot
        else:
            restart()

        last_hit_coord = None


def get_ships_for_start_war():
    create_ship_opponent()
    global your_ship, sh_cord, opponent_ship, ship_list_to_red_del, ship_list_to_red_del_opponent, list_to_dell_ship_opponent
    opponent_ship = []
    yours_ship = []
    ship_list_to_red_del = []
    ship_list_to_red_del_opponent = []
    list_to_dell_ship_opponent = []

    for i in occupied_cells_for_opponent:
        x_o = i[0] * 30
        y_o = i[1] * 30
        opponent_ship.append((x_o, y_o, x_o+30, y_o+30))

    opponent_ship_2 = opponent_ship.copy()
    for i in ship:
        ship_2 = []
        for j in range(i):
            ship_2.append(opponent_ship_2[0])
            opponent_ship_2.pop(0)
        ship_list_to_red_del_opponent.append(ship_2)

    for e_s_o in ship_list_to_red_del_opponent:
        xy3 = e_s_o[0]
        xy4 = e_s_o[-1]
        list_to_dell_ship_opponent.append((xy3[0], xy3[1], xy4[2], xy4[3]))


    if rand_place_ship:
        for i in occupied_cells:
            x = i[0] * 30
            y = i[1] * 30
            yours_ship.append((x, y, x+30, y+30))

        yours_ships_2 = yours_ship.copy()
        for i in ship:
            ship_ = []
            for j in range(i):
                ship_.append(yours_ships_2[0])
                yours_ships_2.pop(0)
            ship_list_to_red_del.append(ship_)

    else:
        for i in ship_place_pole:
            if i[2] - i[0] > i[3] - i[1]:
                is_horizontal = True
            else:
                is_horizontal = False

            counter_1 = 0
            counter_2 = 30
            ship_ = []
            if is_horizontal:
                len_ship = int((i[2] - i[0]) / 30)
                for j in range(len_ship):
                    yours_ship.append((i[0]+counter_1, i[1], i[0]+counter_2, i[1]+30))
                    ship_.append((i[0]+counter_1, i[1], i[0]+counter_2, i[1]+30))
                    counter_1 += 30
                    counter_2 += 30
                ship_list_to_red_del.append(ship_)

            else:
                len_ship = int((i[3] - i[1]) / 30)
                for j in range(len_ship):
                    yours_ship.append((i[0], i[1]+counter_1, i[0]+30, i[1]+counter_2))
                    ship_.append((i[0], i[1]+counter_1, i[0]+30, i[1]+counter_2))
                    counter_1 += 30
                    counter_2 += 30
                ship_list_to_red_del.append(ship_)

    start_war(yours_ship, opponent_ship)


def give_up():
    global get_all_loss_war, war_info_list
    giveUp = messagebox.askyesno("Здатися?", "Ви дійсно бажаєте здатися?")
    if giveUp:
        if authenticated:
            get_all_loss_war += 1
            war_info_list.insert(0, f"Бій №{get_all_war} - Програно.")
        messagebox.showinfo("Поразка", "Ви програли")
        give_up_button.destroy()
        ship_var_pole.unbind("<Button-1>")
        ship_var_pole_2.unbind("<Button-1>")
        restart()


def restart():
    global coordinate_ship, coordinate_ship_2, won, rand_place_ship, count_rand_place_ship, occupied_cells, ship_place_pole, occupied_cells_2
    coordinate_ship = []
    coordinate_ship_2 = []
    count_rand_place_ship = 0
    war_button.destroy()
    ship_var_pole.configure(width=300)
    rand_place_ship = None
    won = None
    clear_pole()


def place_button_to_root(event):
    global war_button
    war_button = Button(root, text="Розпочати\nБій", width=12, height=3, bg="black", fg="white",
                        font=("Times New Roman", 12), command=get_ships_for_start_war)
    war_button.place(x=600, y=390)


r_p_s_button.bind("<Button-1>", place_button_to_root)
h_p_s_button.bind("<Button-1>", place_button_to_root)


def get_true():
    return


def on_enter(event):
    forgot_password_label.config(fg="blue", cursor="hand2")


def on_leave(event):
    forgot_password_label.config(fg="black", cursor="arrow")


# ----------------------------------------------------------------------------------------------------------------------
def root_by():
    by = messagebox.askyesno("Вихід", "Видійсно бажаєте завершити гру?")
    if by:
        root.quit()
    else:
        pass


def open_browser_to_get_info(url):
    webbrowser.open_new_tab(url)


def show_info():
    message = "Перейти за посиланням?\nuk.wikipedia.org/wiki/Морський_бій_(настільна_гра)"
    get_info = messagebox.askyesno("Правила гри", message)
    if get_info:
        open_browser_to_get_info("https://uk.wikipedia.org/wiki/%D0%9C%D0%BE%D1%80%D1%81%D1%8C%D0%BA%D0%B8%D0%B9_"
                                 "%D0%B1%D1%96%D0%B9_(%D0%BD%D0%B0%D1%81%D1%82%D1%96%D0%BB%D1%8C%D0%BD%D0%B0_"
                                 "%D0%B3%D1%80%D0%B0)")


def get_colour_dracula():
    root.configure(bg="black")


def get_color():
    root.configure(bg="red")


# ----------------------------------------------------------------------------------------------------------------------
window_reg = None
authenticated = False


def create_connection_to_mysql_db(db_host, user_name, user_password, db_name):
    global connection
    connection = None
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to DB in method is good")
    except Error as db_connection_error:
        print("Error in db connection: ", db_connection_error)
        if window_reg is True:
            mistake.configure(text="Помилка з підєднанням\nдо бази даних!")
            mistake.place(x=75, y=300)
        else:
            mistake_login.configure(text="Помилка з підєднанням\nдо бази даних!")
            mistake_login.place(x=70, y=180)
    return connection


def window_for_registration(event=None):
    global mistake, window_reg, print_password, registration_done
    window_reg = True
    window_registration.title("Реєстрація")
    window_registration.geometry("300x350+760+300")
    for widget in window_registration.winfo_children():
        widget.destroy()

    button_beck = Button(window_registration, text="Відмінити", width=10, bg="black", fg="white",
                         font=("Times New Roman", 12))
    button_beck.place(x=0, y=0)
    button_beck.bind("<Button-1>", window_for_login)

    Label(window_registration, text="Введіть email:", font=("Times New Roman", 12)).place(x=90, y=40)
    get_post_registration_entry = Entry(window_registration)
    get_post_registration_entry.place(x=90, y=60)
    Label(window_registration, text="Введіть ім'я:", font=("Times New Roman", 12)).place(x=90, y=90)
    get_name_registration_entry = Entry(window_registration)
    get_name_registration_entry.place(x=90, y=110)
    print_password = Label(window_registration, text="Введіть пароль:", font=("Times New Roman", 12))
    print_password.place(x=90, y=140)
    get_password_registration_entry = Entry(window_registration, show="*")
    get_password_registration_entry.place(x=90, y=160)
    Label(window_registration, text="Повторіть пароль:", font=("Times New Roman", 12)).place(x=90, y=190)
    get_password_registration_entry_repeat = Entry(window_registration, show="*")
    get_password_registration_entry_repeat.place(x=90, y=210)

    registration_done = Button(window_registration, text="Зареєструватись", width=15, bg="black", fg="white",
                               font=("Times New Roman", 12))
    registration_done.place(x=80, y=260)

    mistake = Label(window_registration, foreground="red", font=("Times New Roman", 12))
    mistake.place(x=80, y=300)


    def registration(event):
        global cursor_reg, conn_reg, conn_forgot_pass, authenticated, get_id_from_post, get_name_from_post, \
               get_all_war, get_all_win_war, get_all_loss_war, war_info_list, post__get
        post__get = get_post_registration_entry.get()
        name_get = get_name_registration_entry.get()
        password_reg_get = get_password_registration_entry.get()
        password_reg_rep_get = get_password_registration_entry_repeat.get()

        try:
            email_is_valid = validate_email(post__get, check_deliverability=True)
            print('Email is valid')

            if password_reg_get != '' and password_reg_rep_get != '' and name_get != '' and post__get != '' and not window_reg_forgot:
                if password_reg_rep_get != password_reg_get:
                    mistake.configure(text="Неправильний пароль!")
                    mistake.place(x=75, y=300)
                else:
                    mistake.configure(text="")
                    print("good")

                    try:
                        conn_reg = create_connection_to_mysql_db(db_config["mysql"]["host"],
                                                                 db_config["mysql"]["user"],
                                                                 db_config["mysql"]["pass"],
                                                                 "War_ship_game")
                        with conn_reg.cursor() as cursor_reg:
                            post_list = []
                            select_post_from_db = 'SELECT post FROM User_registration'
                            cursor_reg.execute(select_post_from_db)
                            get_post_db = cursor_reg.fetchall()
                            for posts in get_post_db:
                                post_list.append(posts[0])

                        if post__get not in post_list:
                            # print data to table
                            with conn_reg.cursor() as cursor_reg:
                                insert_data_registration = f'''
                                                            INSERT INTO 
                                                                `User_registration` (`post`, `name`, `password`)
                                                            VALUES 
                                                                 ('{post__get}', '{name_get}', '{password_reg_get}')
                                                            '''
                                cursor_reg.execute(insert_data_registration)
                                conn_reg.commit()

                            with conn_reg.cursor() as cursor_reg:
                                get_id_registration = 'SELECT LAST_INSERT_ID()'
                                cursor_reg.execute(get_id_registration)
                                get_id_reg = cursor_reg.fetchone()
                                get_id_from_post = get_id_reg[0]
                                authenticated = True
                                get_all_war, get_all_win_war, get_all_loss_war, war_info_list = None, None, None, None
                                get_name_from_post = name_get
                                authenticated_get_data(event=None)

                        else:
                            mistake.configure(text="Користувач з цією\nпоштою вже зареєстрований!")
                            mistake.place(x=50, y=300)

                    except Error as error:
                        mistake.configure(text="Помилка з доступом\nдо бази даних!")
                        mistake.place(x=80, y=300)
                        print("Error: ", error)

                    finally:
                        cursor_reg.close()
                        conn_reg.close()

            elif password_reg_get != '' and password_reg_rep_get != '' and name_get != '' and post__get != '' and window_reg_forgot:
                mistake.configure(text="")

                try:
                    conn_forgot_pass = create_connection_to_mysql_db(db_config["mysql"]["host"],
                                                                     db_config["mysql"]["user"],
                                                                     db_config["mysql"]["pass"],
                                                                     "War_ship_game")
                    with conn_forgot_pass.cursor() as cursor_forgot:
                        select_post_name_from_db = f'''SELECT post, name, id from User_registration 
                                                        where post = '{post__get}' and name = '{name_get}' '''
                        cursor_forgot.execute(select_post_name_from_db)
                        get_post_name_db = cursor_forgot.fetchone()
                        print(get_post_name_db)

                        if get_post_name_db is None:
                            mistake.configure(text="Неправильний email\nчи ім'я користувача")
                            mistake.place(x=80, y=300)
                        else:
                            if password_reg_rep_get != password_reg_get:
                                mistake.configure(text="Неправильний пароль!")
                                mistake.place(x=75, y=300)
                            else:
                                with conn_forgot_pass.cursor() as cursor_forgot:
                                    update_user_password_forgot = f'''UPDATE User_registration SET 
                                                                      password = '{password_reg_get}' WHERE 
                                                                      id = '{get_post_name_db[2]}' '''
                                    cursor_forgot.execute(update_user_password_forgot)
                                    conn_forgot_pass.commit()
                                    print("nev password created")

                                window_for_login()

                except Error as error:
                    mistake.configure(text="Помилка з доступом\nдо бази даних!")
                    mistake.place(x=80, y=300)
                    print("Error: ", error)

                finally:
                    cursor_forgot.close()
                    conn_forgot_pass.close()

            else:
                mistake.configure(text="Заповніть всі поля!")
                mistake.place(x=80, y=300)

        except EmailNotValidError as e:
            mistake.configure(text="Email заповнений невірно!")
            mistake.place(x=60, y=300)
            print(str(e))
        except AttributeError and NameError:
            pass

    registration_done.bind("<Button-1>", registration)


# ----------------------------------------------------------------------------------------------------------------------
def window_for_login(event=None):
    global window_registration, window_reg_forgot, authenticated, post__get, get_post_login_label, get_post_login_entry, \
           get_password_login_label, get_password_login_entry, login_button, registration_button, mistake_login, \
           forgot_password_label
    if window_registration and window_registration.winfo_exists():
        window_registration.destroy()

    window_registration = Toplevel(root)
    window_registration.title("Вхід")
    window_registration.geometry("300x250+760+300")
    window_registration.resizable(True, True)

    window_reg_forgot = False

    get_post_login_label = Label(window_registration, text="Введіть логін:", font=("Times New Roman", 12))
    get_post_login_label.pack()
    get_post_login_entry = Entry(window_registration)
    get_post_login_entry.pack()

    get_password_login_label = Label(window_registration, text="Введіть пароль:", font=("Times New Roman", 12))
    get_password_login_label.pack()
    get_password_login_entry = Entry(window_registration, show="*")
    get_password_login_entry.pack()

    login_button = Button(window_registration, text="Вхід", width=10, bg="black", fg="white",
                          font=("Times New Roman", 12))
    login_button.place(x=100, y=110)
    registration_button = Button(window_registration, text="Реєстрація", width=10, bg="black", fg="white",
                                 font=("Times New Roman", 12))
    registration_button.place(x=100, y=140)

    mistake_login = Label(window_registration, foreground="red", font=("Times New Roman", 12))
    mistake_login.place(x=80, y=180)
    forgot_password_label = Label(window_registration, text="Забув пароль")
    forgot_password_label.place(x=110, y=230)

    registration_button.bind("<Button-1>", window_for_registration)

    def login(event):
        global conn_log, cursor_log, authenticated, get_id_from_post, get_name_from_post, get_all_war, get_all_win_war, \
               get_all_loss_war, war_info_list, post__get
        post__get = get_post_login_entry.get()
        password_log_get = get_password_login_entry.get()

        if post__get != '' and password_log_get != '':
            try:
                conn_log = create_connection_to_mysql_db(db_config["mysql"]["host"],
                                                         db_config["mysql"]["user"],
                                                         db_config["mysql"]["pass"],
                                                         "War_ship_game")

                with conn_log.cursor() as cursor_log:
                    post_list = []
                    select_post_from_db = 'SELECT post FROM User_registration'
                    cursor_log.execute(select_post_from_db)
                    get_post_db = cursor_log.fetchall()
                    for posts in get_post_db:
                        post_list.append(posts[0])

                if post__get in post_list:
                    with conn_log.cursor() as cursor_log:
                        select_id_pass_for_post_from_db = f'''SELECT id, password, name
                                                          from User_registration WHERE post = '{post__get}' '''
                        cursor_log.execute(select_id_pass_for_post_from_db)
                        get_id_pass_from_post = cursor_log.fetchone()
                        get_pass_from_post = get_id_pass_from_post[1]

                    if get_pass_from_post == password_log_get:
                        get_id_from_post = get_id_pass_from_post[0]
                        get_name_from_post = get_id_pass_from_post[2]
                        authenticated = True
                        get_all_war, get_all_win_war, get_all_loss_war, war_info_list = None, None, None, None
                        authenticated_get_data(event=None)
                        print(get_id_from_post)
                    else:
                        mistake_login.configure(text="Невірно введений пароль!")
                        mistake_login.place(x=60, y=180)
                else:
                    mistake_login.configure(text="Користувача не знайдено!\nСпочатку треба зареєструватись.")
                    mistake_login.place(x=40, y=180)

            except Error as error:
                mistake_login.configure(text="Помилка з доступом\nдо бази даних!")
                mistake_login.place(x=80, y=180)
                print("Error: ", error)
            except AttributeError:
                pass

            finally:
                if connection is not None:
                    cursor_log.close()
                    conn_log.close()
                else:
                    pass

        else:
            mistake_login.configure(text="Заповніть всі поля!")
            mistake_login.place(x=80, y=180)

    login_button.bind("<Button-1>", login)

    def forgot_password(event):
        global window_reg_forgot
        window_reg_forgot = True
        window_for_registration(event=None)

        window_registration.title("Забув пароль")
        print_password.configure(text="Введіть новий пароль:")
        print_password.place(x=75, y=140)
        registration_done.configure(text="Відновити пароль")


    forgot_password_label.bind("<Enter>", on_enter)
    forgot_password_label.bind("<Leave>", on_leave)
    forgot_password_label.bind("<Button-1>", forgot_password)


# ----------------------------------------------------------------------------------------------------------------------
def authenticated_get_data(event):
    global authenticated, label_authentication, get_info_user_button
    if authenticated:
        window_registration.destroy()
        add_menu.entryconfigure(login_leave_index, label='Вийти з системи')
        add_menu.entryconfigure(login_leave_index, command=leave_authenticated)

        get_info_user_button = Button(root, text=f"Інформація\nпро\n{get_name_from_post}", width=12, height=3,
                                      bg="black", fg="white", font=("Times New Roman", 12))
        get_info_user_button.place(x=320, y=390)
        get_info_user_button.bind("<Button-1>", get_user_information)
    else:
        pass


def get_user_information(event):
    global window_user_info, get_info, get_history_button, get_all_war, get_all_win_war, get_all_loss_war, \
           get_history_war, war_info_list, all_war_label, win_war_label, loss_war_label, info_war_text
    if window_user_info and window_user_info.winfo_exists():
        window_user_info.destroy()

    window_user_info = Toplevel(root)
    window_user_info.title(f"{get_name_from_post}")
    window_user_info.geometry("400x500+705+220")
    window_user_info.resizable(True, True)

    Label(window_user_info, text=f"Ім'я: {get_name_from_post}", font=("Times New Roman", 12)).pack()
    Label(window_user_info, text=f"Пошта: {post__get}", font=("Times New Roman", 12)).pack()
    get_history_button = Button(window_user_info, text="Історія\nостанніх\nбоїв:", width=10, height=3, bg="black",
                                fg="white", font=("Times New Roman", 12))
    get_history_button.pack()
    all_war_label = Label(window_user_info, font=("Times New Roman", 12))
    all_war_label.pack()
    win_war_label = Label(window_user_info, font=("Times New Roman", 12))
    win_war_label.pack()
    loss_war_label = Label(window_user_info, font=("Times New Roman", 12))
    loss_war_label.pack()
    info_war_text = Listbox(window_user_info, width=30, height=10, font=("Times New Roman", 12))
    info_war_text.pack()
    button_leave_info = Button(window_user_info, text="Вийти з системи", bg="black", fg="white",
                               font=("Times New Roman", 12), command=leave_authenticated_info)
    button_leave_info.pack()
    mistake_info = Label(window_user_info, font=("Times New Roman", 12), foreground="red")
    mistake_info.pack()

    try:
        get_info = create_connection_to_mysql_db(db_config["mysql"]["host"],
                                                 db_config["mysql"]["user"],
                                                 db_config["mysql"]["pass"],
                                                 "War_ship_game")
        with get_info.cursor() as cursor_get_info:
            id_list = []
            select_id_from_db = 'SELECT id FROM User_info'
            cursor_get_info.execute(select_id_from_db)
            get_id_db = cursor_get_info.fetchall()
            for id in get_id_db:
                id_list.append(id[0])

        if get_id_from_post not in id_list:
            with get_info.cursor() as cursor_get_info:
                insert_data_info = f'''
                                    INSERT INTO
                                        `User_info` (`id`, `count`, `count_win`, `count_loos`, `col_10`, `col_9`, 
                                                     `col_8`, `col_7`, `col_6`, `col_5`, `col_4`, `col_3`, `col_2`, 
                                                     `col_1`)
                                    VALUES
                                        ('{get_id_from_post}', 0, 0, 0, 'N10', 'N9', 'N8', 'N7', 'N6', 
                                        'N5', 'N4', 'N3', 'N2', 'N1')
                                    '''
                cursor_get_info.execute(insert_data_info)
                get_info.commit()
        else:
            pass

    except Error as error:
        mistake_info.configure(text="Помилка з доступом\nдо бази даних!")
        print("Error: ", error)

    finally:
        cursor_get_info.close()
        get_info.close()


    def get_history_war(event):
        global get_user_info, get_all_war, get_all_win_war, get_all_loss_war, war_info_list
        try:
            get_user_info = create_connection_to_mysql_db(db_config["mysql"]["host"],
                                                          db_config["mysql"]["user"],
                                                          db_config["mysql"]["pass"],
                                                          "War_ship_game")
            if get_all_war is None or get_all_loss_war is None or get_all_win_war is None or war_info_list == []:
                with get_user_info.cursor() as cursor_get_user_info:
                    select_user_game_data_from_db = f'''SELECT * FROM User_info where id = '{get_id_from_post}' '''
                    cursor_get_user_info.execute(select_user_game_data_from_db)
                    get_data_db = cursor_get_user_info.fetchone()

                war_info_list = []
                get_all_war = int(get_data_db[1])
                get_all_win_war = int(get_data_db[2])
                get_all_loss_war = int(get_data_db[3])
                co = 4
                for war_info in range(4, 14):
                    war_info_list.append(get_data_db[war_info])
                    co += 1

            else:
                with get_user_info.cursor() as cursor_get_user_info:
                    update_user_war_info = f'''UPDATE User_info SET 
                                                            count = '{get_all_war}',
                                                            count_win = '{get_all_win_war}',
                                                            count_loos = '{get_all_loss_war}',
                                                            col_10 = '{war_info_list[0]}',
                                                            col_9 = '{war_info_list[1]}',
                                                            col_8 = '{war_info_list[2]}',
                                                            col_7 = '{war_info_list[3]}',
                                                            col_6 = '{war_info_list[4]}',
                                                            col_5 = '{war_info_list[5]}',
                                                            col_4 = '{war_info_list[6]}',
                                                            col_3 = '{war_info_list[7]}',
                                                            col_2 = '{war_info_list[8]}',
                                                            col_1 = '{war_info_list[9]}'
                                                        WHERE id = '{get_id_from_post}' '''
                    cursor_get_user_info.execute(update_user_war_info)
                    get_user_info.commit()

                for elem in war_info_list:
                    info_war_text.insert(END, elem)

                all_war_label.configure(text=f"Кількість зіграних боїв: {get_all_war}")
                win_war_label.configure(text=f"Кількість виграних боїв: {get_all_win_war}")
                loss_war_label.configure(text=f"Кількість програних боїв: {get_all_loss_war}")

        except Error as error:
            mistake_info.configure(text="Помилка з доступом\nдо бази даних!")
            print("Error: ", error)

        finally:
            cursor_get_user_info.close()
            get_user_info.close()

    get_history_button.bind("<Button-1>", get_history_war)


def leave_authenticated():
    global authenticated, get_id_from_post, leave, get_name_from_post
    if authenticated:
        leave = messagebox.askyesno("Вийти", "Вийти з акаунта?")
        if leave:
            authenticated = False
            get_id_from_post = None
            get_name_from_post = None
            add_menu.entryconfigure(login_leave_index, label='Вхід в систему')
            add_menu.entryconfigure(login_leave_index, command=window_for_login)
            get_info_user_button.destroy()
        else:
            pass


def leave_authenticated_info():
    leave_authenticated()
    window_user_info.destroy()


# ----------------------------------------------------------------------------------------------------------------------
main_menu = Menu(root)
root.config(menu=main_menu)

add_menu = Menu(main_menu, tearoff=0)
add_menu.add_command(label='Вийти з гри', command=root_by)
add_menu.add_command(label="Правила гри.", command=show_info)
add_menu.add_command(label='Вхід в систему', command=window_for_login)
main_menu.add_cascade(label='Меню', menu=add_menu)
login_leave_index = add_menu.index("Вхід в систему")

color_meny = Menu(main_menu, tearoff=0)
color_meny.add_command(label='Dracula', command=get_colour_dracula)
color_meny.add_command(label="wtf", command=get_color)
main_menu.add_cascade(label="Тема", menu=color_meny)


root.mainloop()
