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
root.geometry("1500x600")
root.resizable(True, True)

about_ship = "1 корабель — ряд із 4 клітин («лінкор», або «чотирипалубний»)\n" \
             "2 кораблі — ряд із 3 клітин («крейсери», або «трипалубні»)\n" \
             "3 кораблі — ряд із 2 клітин («есмінці», або «двопалубні»)\n" \
             "4 кораблі — 1 клітина («підводні човни», або «однопалубні»)"
Label(root, text=about_ship, font=("Times New Roman", 14)).place(x=0, y=400)
Label(root, text="Ваше полотно", font=("Times New Roman", 14)).place(x=110, y=0)
Label(root, text="Полотно суперника", font=("Times New Roman", 14)).place(x=1070, y=0)

ship = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
i = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
j = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
x, y, yi, xj = 0, 0, 0, 0

window_registration = None
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
chose_another_box = False
won = None


def clear_pole():
    ship_var_pole.delete("ship", "chip_to_place", "kill_my_ship")
    ship_var_pole_2.delete("i_kill_ship", "ship_opponent")


def click_2(event):
    global chose_another_box, won
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
        chose_another_box = False
    else:
        if (x1, y1, x2, y2) in opponent_ship:
            index_kill = opponent_ship.index((x1, y1, x2, y2))
            ship_var_pole_2.create_oval(x1, y1, x2, y2, fill="gray", tags="i_kill_ship")
            ship_var_pole_2.create_oval(x1 + 7, y1 + 7, x2 - 7, y2 - 7, fill="black", tags="i_kill_ship")
            opponent_ship.pop(index_kill)
            if len(opponent_ship) == 0:
                won = True
                ship_var_pole_2.unbind("<Button-1>")
                messagebox.showinfo("Перемога", "Ви перемогли")
                clear_pole()
        else:
            ship_var_pole_2.create_oval(x1 + 7, y1 + 7, x2 - 7, y2 - 7, fill="black", tags="i_kill_ship")

        if won is None:
            m_b()
        else:
            restart()
            pass


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
    global rand_place_ship_2, occupied_cells_for_opponent
    rand_place_ship_2 = True
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

            # перевірка на перетин з іншими кораблями
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

        if is_horizontal:
            ship_var_pole_2.create_rectangle(30 * x, 30 * y, 30 * x + 30 * ship_size, 30 * y + 30, fill="black",
                                             tags="ship_opponent")
        else:
            ship_var_pole_2.create_rectangle(30 * x, 30 * y, 30 * x + 30, 30 * y + 30 * ship_size, fill="black",
                                             tags="ship_opponent")


r_p_s_button = Button(root, text="r_p_s", command=random_place_ship)
r_p_s_button.place(x=200, y=400)
h_p_s_button = Button(root, text="h_p_s", command=himself_place_ship)
h_p_s_button.place(x=200, y=440)


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
    global m_b, won, give_up_button
    move_bot_list = []
    count_rand_place_ship = 0
    for i in your_ship:
        count_rand_place_ship += 1

    if count_rand_place_ship < 20:
        messagebox.showerror("Помилка", "Не виставлено всіх кораблів спробуйте заново")
        himself_place_ship()
        pass
    else:
        ship_var_pole.configure(width=300)
        if war_button.bind("<Button-1>", get_true):
            give_up_button = Button(root, text="Здатися", command=give_up)
            give_up_button.place(x=200, y=520)

        ship_var_pole_2.bind("<Button-1>", click_2)

        def move_bot():
            global won
            while True:
                x_ = random.randint(0, 9)
                y_ = random.randint(0, 9)
                x1, y1 = x_ * 30, y_ * 30
                x2, y2 = x1 + 30, y1 + 30
                move_bot = (x1, y1, x2, y2)

                if move_bot not in move_bot_list:
                    move_bot_list.append(move_bot)
                    break

            if move_bot in your_ship:
                index_kill_bot = your_ship.index(move_bot)
                ship_var_pole.create_oval(x1, y1, x2, y2, fill="gray", tags="kill_my_ship")
                ship_var_pole.create_oval(x1 + 7, y1 + 7, x2 - 7, y2 - 7, fill="black", tags="kill_my_ship")
                your_ship.pop(index_kill_bot)
                if len(your_ship) == 0:
                    won = False
                    messagebox.showinfo("Поразка", "Ви програли")
                    clear_pole()
                    ship_var_pole_2.unbind("<Button-1>")
            else:
                ship_var_pole.create_oval(x1 + 7, y1 + 7, x2 - 7, y2 - 7, fill="black", tags="kill_my_ship")

        if won is None:
            m_b = move_bot
        else:
            restart()
            pass


def get_ships_for_start_war():
    create_ship_opponent()
    global your_ship, sh_cord, opponent_ship
    opponent_occupied_cells = []
    yours_ships = []

    for i in occupied_cells_for_opponent:
        x_o = i[0] * 30
        y_o = i[1] * 30
        opponent_occupied_cells.append((x_o, y_o, x_o+30, y_o+30))
    opponent_ship = opponent_occupied_cells

    if rand_place_ship:
        for i in occupied_cells:
            x = i[0] * 30
            y = i[1] * 30
            yours_ships.append((x, y, x+30, y+30))
    else:
        for i in ship_place_pole:
            if i[2] - i[0] > i[3] - i[1]:
                is_horizontal = True
            else:
                is_horizontal = False

            counter_1 = 0
            counter_2 = 30
            if is_horizontal:
                len_ship = int((i[2] - i[0]) / 30)
                for j in range(len_ship):
                    yours_ships.append((i[0]+counter_1, i[1], i[0]+counter_2, i[1]+30))
                    counter_1 += 30
                    counter_2 += 30
            else:
                len_ship = int((i[3] - i[1]) / 30)
                for j in range(len_ship):
                    yours_ships.append((i[0], i[1]+counter_1, i[0]+30, i[1]+counter_2))
                    counter_1 += 30
                    counter_2 += 30

    your_ship = yours_ships
    start_war(your_ship, opponent_ship)


def give_up():
    giveUp = messagebox.askyesno("Здатися?", "Ви дійсно бажаєте здатися?")
    if giveUp:
        messagebox.showinfo("Поразка", "Ви програли")
        restart()
        clear_pole()
        ship_var_pole.unbind("<Button-1>")
        ship_var_pole_2.unbind("<Button-1>")


def restart():
    global coordinate_ship, coordinate_ship_2, won, count_rand_place_ship
    coordinate_ship = []
    coordinate_ship_2 = []
    count_rand_place_ship = 0
    war_button.destroy()
    give_up_button.destroy()
    won = None



def place_button_to_root(event):
    global war_button
    war_button = Button(root, text="Бій", command=get_ships_for_start_war)
    war_button.place(x=200, y=480)


r_p_s_button.bind("<Button-1>", place_button_to_root)
h_p_s_button.bind("<Button-1>", place_button_to_root)


def get_true():
    return True


def on_enter(event):
    forgot_password_label.config(fg="blue", cursor="hand2")


def on_leave(event):
    forgot_password_label.config(fg="black", cursor="arrow")


# ----------------------------------------------------------------------------------------------------------------------
window_reg = None


def root_by():
    root.quit()


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
    global mistake, window_reg, print_password
    window_reg = True
    window_registration.title("Реєстрація")
    window_registration.geometry("300x350")
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
        global cursor_reg, conn_reg
        post_reg_get = get_post_registration_entry.get()
        name_get = get_name_registration_entry.get()
        password_reg_get = get_password_registration_entry.get()
        password_reg_rep_get = get_password_registration_entry_repeat.get()

        try:
            email_is_valid = validate_email(post_reg_get, check_deliverability=True)
            print('Email is valid')

            if password_reg_get != '' and password_reg_rep_get != '' and name_get != '' and post_reg_get != '' and not window_reg_forgot:
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
                        # create_table
                        with conn_reg.cursor() as cursor_reg:
                            create_table = '''
                                            CREATE TABLE IF NOT EXISTS User_registration (
                                            id INT AUTO_INCREMENT,
                                            post TEXT NOT NULL,
                                            name TEXT NOT NULL,
                                            password TEXT NOT NULL,
                                            PRIMARY KEY (id)
                                            ) ENGINE = InnoDB
                                            '''
                            cursor_reg.execute(create_table)
                            conn_reg.commit()

                        # get data from table
                        with conn_reg.cursor() as cursor_reg:
                            post_list = []
                            select_post_from_db = 'SELECT post FROM User_registration'
                            cursor_reg.execute(select_post_from_db)
                            get_post_db = cursor_reg.fetchall()
                            for posts in get_post_db:
                                post_list.append(posts[0])

                        if post_reg_get not in post_list:
                            # print data to table
                            with conn_reg.cursor() as cursor_reg:
                                insert_data_registration = f'''
                                                            INSERT INTO 
                                                                `User_registration` (`post`, `name`, `password`)
                                                            VALUES 
                                                                 ('{post_reg_get}', '{name_get}', '{password_reg_get}')
                                                            '''
                                cursor_reg.execute(insert_data_registration)
                                conn_reg.commit()

                            with conn_reg.cursor() as cursor_reg:
                                get_id_registration = 'SELECT LAST_INSERT_ID()'
                                cursor_reg.execute(get_id_registration)
                                get_id_reg = cursor_reg.fetchone()
                                get_id = get_id_reg[0]
                                window_registration.destroy()

                        else:
                            mistake.configure(text="Користувач з цією\nпоштою вже зареєстрований!")
                            mistake.place(x=50, y=300)

                    except Error as error:
                        mistake.configure(text="Помилка з доступом\nдо бази даних!")
                        mistake.place(x=80, y=300)
                        print("fucking error: ", error)

                    finally:
                        cursor_reg.close()
                        conn_reg.close()

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
    global window_registration, window_reg_forgot
    if window_registration and window_registration.winfo_exists():
        window_registration.destroy()

    window_registration = Toplevel(root)
    window_registration.title("Вхід")
    window_registration.geometry("300x250")
    window_registration.resizable(True, True)

    window_reg_forgot = False

    global get_post_login_label, get_post_login_entry, get_password_login_label, get_password_login_entry, \
           login_button, registration_button, mistake_login, forgot_password_label
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
        global conn_log, cursor_log
        post_log_get = get_post_login_entry.get()
        password_log_get = get_password_login_entry.get()

        if post_log_get != '' and password_log_get != '':
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

                if post_log_get in post_list:
                    with conn_log.cursor() as cursor_log:
                        select_id_pass_for_post_from_db = f'''SELECT id, password
                                                          from User_registration WHERE post = '{post_log_get}' '''
                        cursor_log.execute(select_id_pass_for_post_from_db)
                        get_id_pass_from_post = cursor_log.fetchone()
                        get_pass_from_post = get_id_pass_from_post[1]

                    if get_pass_from_post == password_log_get:
                        get_id_from_post = get_id_pass_from_post[0]
                        print(get_id_from_post)
                        window_registration.destroy()
                    else:
                        mistake_login.configure(text="Невірно введений пароль!")
                        mistake_login.place(x=60, y=180)
                else:
                    mistake_login.configure(text="Користувача не знайдено!\nСпочатку треба зареєструватись.")
                    mistake_login.place(x=40, y=180)

            except Error as error:
                mistake_login.configure(text="Помилка з доступом\nдо бази даних!")
                mistake_login.place(x=80, y=180)
                print("fucking error: ", error)
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






    forgot_password_label.bind("<Enter>", on_enter)
    forgot_password_label.bind("<Leave>", on_leave)
    forgot_password_label.bind("<Button-1>", forgot_password)


# ----------------------------------------------------------------------------------------------------------------------
main_menu = Menu(root)
root.config(menu=main_menu)

add_menu = Menu(main_menu, tearoff=0)
add_menu.add_command(label='Вийти', command=root_by)
add_menu.add_command(label='Вхід', command=window_for_login)
add_menu.add_command(label="Правила гри.", command=show_info)
main_menu.add_cascade(label='Меню', menu=add_menu)

color_meny = Menu(main_menu, tearoff=0)
color_meny.add_command(label='Dracula', command=get_colour_dracula)
color_meny.add_command(label="wtf", command=get_color)
main_menu.add_cascade(label="Тема", menu=color_meny)


root.mainloop()
