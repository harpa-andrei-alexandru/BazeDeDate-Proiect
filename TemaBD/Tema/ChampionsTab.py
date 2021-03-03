from tkinter import *
from tkinter import font, ttk, messagebox
from cx_Oracle import IntegrityError


def champion_update_error():
    popup = Toplevel()
    popup.title('Warning')
    popup.geometry('300x100')

    message = Label(popup, text='Out of range input values!!!'
                                '\nhealth: 480.0 <-> 740.0\narmor: 18.0 <-> 47.0'
                                '\nattack damage: 45 <-> 70\nmagic resist: 25.0 <-> 39.0')

    message.pack(side=LEFT)


class ChampionsTab:
    def __init__(self, tabs, data_base, root):
        self.__root = root
        self.__db = data_base
        self.__tabs = tabs
        self.__champions_tab = Frame(self.__tabs, width='700', height='500', bg='red')
        self.__owned_champions_label = None
        self.__champions_label = None
        self.__owned_champions_list = None
        self.__owned_champions_scrollbar = None
        self.__champions_list = None
        self.__champions_scrollbar = None

        self.__champ_name_label = None
        self.__health_label = None
        self.__armor_label = None
        self.__attack_damage_label = None
        self.__magic_resist_label = None
        self.__release_date_label = None
        self.__champion_status_label = None
        self.__price_rp_label = None
        self.__price_be_label = None

        self.__buy_with_be_button = None
        self.__buy_with_rp_button = None
        self.__update_button = None
        self.__add_button = None
        self.__add_new_champion_button = None

        self.__label_font = font.Font(family="Courier", size=10, weight="bold")

    def create_labels(self):
        self.__owned_champions_label = Label(self.__champions_tab, text='Owned Champions', width=20,
                                             font=('Courier', 10, 'bold'))
        self.__champions_label = Label(self.__champions_tab, text='Champions', width=20,
                                       font=('Courier', 10, 'bold'))

    def create_buttons(self):
        self.__add_new_champion_button = Button(self.__champions_tab, text='Add new Champion', command=self.__add_new_champion_popup)

    def add_buttons(self):
        self.__add_new_champion_button.grid(row=2, column=2, padx=(40, 0))

    def add_labels(self):
        self.__owned_champions_label.grid(row=0, column=0, pady=(50, 20), padx=(10, 0))
        self.__champions_label.grid(row=0, column=2, pady=(50, 20), padx=(50, 0))

    def add_tab(self):
        self.__champions_tab.pack(fill='both', expand=1)
        self.__tabs.add(self.__champions_tab, text='Champions')

    def create_listbox(self):
        self.__owned_champions_list = Listbox(self.__champions_tab, height=13, width=40, font=self.__label_font)
        self.__champions_list = Listbox(self.__champions_tab, height=13, width=40, font=self.__label_font)
        self.__add_listbox_scrollbar()
        self.__add_listbox_callback()

    def __add_listbox_scrollbar(self):
        self.__owned_champions_scrollbar = Scrollbar(self.__champions_tab, orient='vertical',
                                                     command=self.__owned_champions_list.yview)
        self.__champions_scrollbar = Scrollbar(self.__champions_tab, orient='vertical',
                                               command=self.__champions_list.yview)
        self.__owned_champions_list.config(yscrollcommand=self.__owned_champions_scrollbar.set)
        self.__champions_list.config(yscrollcommand=self.__champions_scrollbar.set)

    def __add_listbox_callback(self):
        self.__owned_champions_list.bind('<Double-Button>', self.__get_details)
        self.__champions_list.bind('<Double-Button>', self.__handle_champion)

    def add_listbox(self):
        self.__owned_champions_list.grid(row=1, column=0, pady=10, padx=(30, 0))
        self.__owned_champions_scrollbar.grid(row=1, column=1, ipady=60)

        self.__champions_list.grid(row=1, column=2, pady=10, padx=(50, 0))
        self.__champions_scrollbar.grid(row=1, column=3, ipady=60)

    def __create_detail_labels(self, master, champ_name, details):
        self.__champ_name_label = Label(master, text='Name: {0}'.format(champ_name), width='30', anchor='w')
        self.__health_label = Label(master, text='Health: {0}'.format(details['health']), width='30', anchor='w')
        self.__armor_label = Label(master, text='Armor: {0}'.format(details['armor']), width='30', anchor='w')
        self.__attack_damage_label = Label(master, text='Attack Damage: {0}'.format(details['attack_damage']),
                                           width='30', anchor='w')
        self.__magic_resist_label = Label(master, text='Magic Resist: {0}'.format(details['magic_resist']), width='30',
                                          anchor='w')
        self.__release_date_label = Label(master, text='Release Date: {0}'.format(details['release_date']), width='30',
                                          anchor='w')
        self.__champion_status_label = Label(master, text='Status: ', width=20, anchor='w', bg='red')
        self.__price_rp_label = Label(master, text='Riot Points Price: {0}'.format(details['price_rp']), width='30',
                                      anchor='w')
        self.__price_be_label = Label(master, text='Blue Essence Price: {0}'.format(details['price_blue_essence']),
                                      width='30', anchor='w')

    def __add_detail_labels(self):
        self.__champ_name_label.grid(row=0, column=0, pady=5)
        self.__health_label.grid(row=1, column=0, pady=5)
        self.__armor_label.grid(row=2, column=0, pady=5)
        self.__attack_damage_label.grid(row=3, column=0, pady=5)
        self.__magic_resist_label.grid(row=4, column=0, pady=5)
        self.__release_date_label.grid(row=5, column=0, pady=5)
        self.__champion_status_label.grid(row=0, column=1, pady=5)
        self.__price_rp_label.grid(row=6, column=0, pady=5)
        self.__price_be_label.grid(row=7, column=0, pady=5)

    def __create_update_labels(self, master):
        self.__health_label = Label(master, text='Health: ', width='15', anchor='w')
        self.__armor_label = Label(master, text='Armor: ', width='15', anchor='w')
        self.__attack_damage_label = Label(master, text='Attack Damage: ', width='15', anchor='w')
        self.__magic_resist_label = Label(master, text='Magic Resist: ', width='15', anchor='w')

    def __add_update_labels(self):
        self.__health_label.grid(row=0, column=0, pady=5)
        self.__armor_label.grid(row=1, column=0, pady=5)
        self.__attack_damage_label.grid(row=2, column=0, pady=5)
        self.__magic_resist_label.grid(row=3, column=0, pady=5)

    def __create_buttons(self, master, champion_name):
        self.__buy_with_be_button = Button(master, text='Buy With Blue Essence', anchor='w',
                                           command=lambda: self.__buy_champion(champion_name, 1))
        self.__buy_with_rp_button = Button(master, text='Buy With Riot Points', anchor='w',
                                           command=lambda: self.__buy_champion(champion_name, 2))
        self.__update_button = Button(master, text='Update', anchor='w',
                                      command=lambda: self.__update_champion(champion_name))
        self.__add_button = Button(master, text='Add', anchor='w', command=lambda: self.__add_champion(champion_name))

    def __add_buttons(self):
        self.__buy_with_be_button.grid(row=1, column=1)
        self.__buy_with_rp_button.grid(row=2, column=1)
        self.__update_button.grid(row=3, column=1)
        self.__add_button.grid(row=5, column=1)

    def __get_details(self, event):
        widget = event.widget
        idx = int(widget.curselection()[0])
        champion_name = widget.get(idx)

        popup = Toplevel()
        popup.title('Details')
        popup.geometry('400x250')
        popup.resizable(False, False)

        details = self.__db.champions[champion_name]
        self.__create_detail_labels(popup, champion_name, details)
        self.__add_detail_labels()
        self.__champion_status_label.config(text='Status: Owned', bg='green')

    def __handle_champion(self, event):
        widget = event.widget
        idx = int(widget.curselection()[0])
        champion_name = widget.get(idx)

        popup = Toplevel()
        popup.title('Details')
        popup.geometry('400x250')
        popup.resizable(False, False)

        details = self.__db.champions[champion_name]
        self.__create_detail_labels(popup, champion_name, details)
        self.__add_detail_labels()
        self.__create_buttons(popup, champion_name)
        self.__add_buttons()
        if self.__root.current_user != '':
            if champion_name in self.__db.champions_owned[self.__root.current_user]:
                self.__add_button.config(state=DISABLED)
                self.__buy_with_be_button.config(state=DISABLED)
                self.__buy_with_rp_button.config(state=DISABLED)
                self.__champion_status_label.config(text='Status: Owned', bg='green')
            else:
                self.__champion_status_label.config(text='Status: Ready To Buy', bg='yellow')
            if self.__db.resources[self.__root.current_user]['riot_points'] < int(details['price_rp']):
                self.__buy_with_rp_button.config(state=DISABLED)
            if self.__db.resources[self.__root.current_user]['blue_essence'] < int(details['price_blue_essence']):
                self.__buy_with_be_button.config(state=DISABLED)

    def __update_champion(self, champion_name):
        popup = Toplevel()
        popup.title('Details')
        popup.geometry('400x200')
        popup.resizable(False, False)

        self.__create_update_labels(popup)
        self.__add_update_labels()
        health_entry = Entry(popup, width=10)
        armor_entry = Entry(popup, width=10)
        attack_damage_entry = Entry(popup, width=10)
        magic_resist_entry = Entry(popup, width=10)

        details = self.__db.champions[champion_name]
        health_entry.insert(END, details['health'])
        armor_entry.insert(END, details['armor'])
        attack_damage_entry.insert(END, details['attack_damage'])
        magic_resist_entry.insert(END, details['magic_resist'])

        done_button = Button(popup, text='Done', command=lambda: self.__done_callback(champion_name, health_entry.get(),
                                                                                      armor_entry.get(),
                                                                                      attack_damage_entry.get(),
                                                                                      magic_resist_entry.get(), popup))

        health_entry.grid(row=0, column=1)
        armor_entry.grid(row=1, column=1)
        attack_damage_entry.grid(row=2, column=1)
        magic_resist_entry.grid(row=3, column=1)
        done_button.grid(row=4, column=1)

    def __done_callback(self, champion_name, health, armor, attack_damage, magic_resist, popup):
        try:
            self.__db.update_champion(champion_name, health, armor, attack_damage, magic_resist)
        except IntegrityError as e:
            error_obj, = e.args
            print("Not enough resources")
            print("Error Code:", error_obj.code)
            print("Error Message:", error_obj.message)
            champion_update_error()
        else:
            popup.destroy()

    def select_owned_champions(self, user_name):
        owned_champions = self.__db.get_owned_champions(user_name)
        self.__owned_champions_list.delete(0, END)
        for champion in owned_champions:
            self.__owned_champions_list.insert(0, champion)

    def select_champions(self):
        champions = [*self.__db.champions.keys()]
        for champion in champions:
            self.__champions_list.insert(0, champion)

    def __add_champion(self, champion_name):
        if self.__root.current_user != '':
            self.__owned_champions_list.insert(0, champion_name)
            self.__db.add_champion(champion_name, self.__root.current_user)
            self.__add_button.config(state=DISABLED)
            self.__buy_with_be_button.config(state=DISABLED)
            self.__buy_with_rp_button.config(state=DISABLED)

    def __buy_champion(self, champion_name, t):
        if self.__root.current_user != '':
            try:
                self.__db.buy_champion(champion_name, self.__root.current_user, t)
            except IntegrityError as e:
                error_obj, = e.args
                print("Not enough resources")
                print("Error Code:", error_obj.code)
                print("Error Message:", error_obj.message)
            else:
                self.__owned_champions_list.insert(0, champion_name)
                self.__add_button.config(state=DISABLED)
                self.__buy_with_be_button.config(state=DISABLED)
                self.__buy_with_rp_button.config(state=DISABLED)
                if t == 1:
                    self.__root.resources_tab.blue_essence_label.config(text='Blue Essence: '
                                                                             + str(
                        self.__db.resources[self.__root.current_user]['blue_essence']))
                elif t == 2:
                    self.__root.resources_tab.riot_points_label.config(text='Riot Points: '
                                                                            + str(
                        self.__db.resources[self.__root.current_user]['riot_points']))

    def __add_new_champion_popup(self):
        popup = Toplevel(self.__champions_tab)
        popup.title('Add new Champion')
        popup.geometry('400x300')
        popup.resizable(False, False)

        name_label = Label(popup, text='Name: ', width=20, anchor='w')
        health_label = Label(popup, text='Health: ', width=20, anchor='w')
        armor_label = Label(popup, text='Armor:', width=20, anchor='w')
        attack_damage_label = Label(popup, text='Attack Damage:', width=20, anchor='w')
        magic_resist_label = Label(popup, text='Magic Resist:', width=20, anchor='w')
        price_rp_label = Label(popup, text='Price RP: ', width=20, anchor='w')
        price_be_label = Label(popup, text='Price Blue Essence: ', width=20, anchor='w')
        release_date_label = Label(popup, text='Release Date: ', width=20, anchor='w')

        name_entry = Entry(popup, width=30)
        health_entry = Entry(popup, width=10)
        armor_entry = Entry(popup, width=10)
        attack_damage_entry = Entry(popup, width=10)
        magic_resist_entry = Entry(popup, width=10)
        release_date_entry = Entry(popup, width=10)

        rp_prices = ttk.Combobox(popup, state='readonly')
        be_prices = ttk.Combobox(popup, state='readonly')
        rp_prices['values'] = ('260', '585', '790', '880', '975')
        be_prices['values'] = ('450', '1350', '4800', '6300', '7800')

        add_button = Button(popup, text='Add', command=lambda: self.__add_new_champion(popup, name_entry.get(), health_entry.get(),
                                                            armor_entry.get(), attack_damage_entry.get(), magic_resist_entry.get(),
                                                            rp_prices.get(), be_prices.get(), release_date_entry.get()))

        name_label.grid(row=0, column=0, pady=5)
        health_label.grid(row=1, column=0, pady=5)
        armor_label.grid(row=2, column=0, pady=5)
        attack_damage_label.grid(row=3, column=0, pady=5)
        magic_resist_label.grid(row=4, column=0, pady=5)
        price_rp_label.grid(row=5, column=0, pady=5)
        price_be_label.grid(row=6, column=0, pady=5)
        release_date_label.grid(row=7, column=0, pady=5)

        name_entry.grid(row=0, column=1, pady=5)
        health_entry.grid(row=1, column=1, pady=5)
        armor_entry.grid(row=2, column=1, pady=5)
        attack_damage_entry.grid(row=3, column=1, pady=5)
        magic_resist_entry.grid(row=4, column=1, pady=5)
        rp_prices.grid(row=5, column=1, pady=5)
        be_prices.grid(row=6, column=1, pady=5)
        release_date_entry.grid(row=7, column=1, pady=5)

        add_button.grid(row=8, column=1, pady=5)

    def __add_new_champion(self, master, name, health, armor, attack, magic_resist, price_rp, price_be, release_date):
        regex = '^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)\d\d$'
        if len(name) < 3:
            messagebox.showerror('Error', 'The name must have at least 3 characters!')
        if health == '':
            messagebox.showerror('Error', 'Field Health empty!')
        elif float(health) < 480.0 or float(health) > 740.0:
            messagebox.showerror('Error', 'Health must be between 480.0 and 740.0!')
        if armor == '':
            messagebox.showerror('Error', 'Field Armor empty!')
        elif float(armor) < 18.0 or float(armor) > 47.0:
            messagebox.showerror('Error', 'Armor must be between 18.0 and 47.0!')
        if attack == '':
            messagebox.showerror('Error', 'Field Attack Damage empty!')
        elif float(attack) < 45.0 or float(attack) > 70.0:
            messagebox.showerror('Error', 'Attack Damage must be between 45.0 and 70.0!')
        if magic_resist == '':
            messagebox.showerror('Error', 'Field Magic Resist empty!')
        elif float(magic_resist) < 25.0 or float(magic_resist) > 39.0:
            messagebox.showerror('Error', 'Magic Resist must be between 25.0 and 39.0!')
        if price_rp == '':
            messagebox.showerror('Error', 'Select a rp price!')
        if price_be == '':
            messagebox.showerror('Error', 'Select a blue essence price!')
        if not re.search(regex, release_date):
            messagebox.showerror('Error', 'Wrong date or date format, please use dd.mm.yyyy format!')
        else:
            self.__db.add_new_champion(name, health, armor, attack, magic_resist, price_rp, price_be, release_date)
            self.__champions_list.insert(0, name)
            master.destroy()

    def clear_owned_champions_list(self):
        self.__owned_champions_list.delete(0, END)
