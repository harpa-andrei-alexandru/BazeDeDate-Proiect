from tkinter import *
from tkinter import font, ttk, messagebox
from cx_Oracle import IntegrityError


class SkinsTab:
    def __init__(self, tabs, data_base, root):
        self.__root = root
        self.__db = data_base
        self.__tabs = tabs
        self.__skins_tab = Frame(self.__tabs, width='700', height='500', bg='green')
        self.__owned_skins_label = None
        self.__skins_label = None
        self.__owned_skins_list = None
        self.__owned_skins_scrollbar = None
        self.__skins_list = None
        self.__skins_scrollbar = None

        self.__skin_name_label = None
        self.__release_date_label = None
        self.__type_label = None
        self.__skin_status_label = None
        self.__price_rp_label = None
        self.__price_oe_label = None

        self.__buy_with_oe_button = None
        self.__buy_with_rp_button = None
        self.__add_button = None
        self.__add_new_skin_button = None

        self.__label_font = font.Font(family="Courier", size=10, weight="bold")

    def create_labels(self):
        self.__owned_skins_label = Label(self.__skins_tab, text='Owned Skins', width=20,
                                         font=('Courier', 10, 'bold'))
        self.__skins_label = Label(self.__skins_tab, text='Skins', width=20,
                                   font=('Courier', 10, 'bold'))

    def add_labels(self):
        self.__owned_skins_label.grid(row=0, column=0, pady=(50, 20), padx=(10, 0))
        self.__skins_label.grid(row=0, column=2, pady=(50, 20), padx=(50, 0))

    def create_buttons(self):
        self.__add_new_skin_button = Button(self.__skins_tab, text='Add new Skin',
                                            command=self.__add_new_skin_popup)

    def add_buttons(self):
        self.__add_new_skin_button.grid(row=2, column=2, padx=(40, 0))

    def add_tab(self):
        self.__skins_tab.pack(fill='both', expand=1)
        self.__tabs.add(self.__skins_tab, text='Skins')

    def create_listbox(self):
        self.__owned_skins_list = Listbox(self.__skins_tab, height=13, width=40, font=self.__label_font)
        self.__skins_list = Listbox(self.__skins_tab, height=13, width=40, font=self.__label_font)
        self.__add_listbox_scrollbar()
        self.__add_listbox_callback()

    def __add_listbox_scrollbar(self):
        self.__owned_skins_scrollbar = Scrollbar(self.__skins_tab, orient='vertical',
                                                 command=self.__owned_skins_list.yview)
        self.__skins_scrollbar = Scrollbar(self.__skins_tab, orient='vertical',
                                           command=self.__skins_list.yview)
        self.__owned_skins_list.config(yscrollcommand=self.__owned_skins_scrollbar.set)
        self.__skins_list.config(yscrollcommand=self.__skins_scrollbar.set)

    def __add_listbox_callback(self):
        self.__owned_skins_list.bind('<Double-Button>', self.__get_details)
        self.__skins_list.bind('<Double-Button>', self.__handle_skin)

    def add_listbox(self):
        self.__owned_skins_list.grid(row=1, column=0, pady=10, padx=(30, 0))
        self.__owned_skins_scrollbar.grid(row=1, column=1, ipady=60)

        self.__skins_list.grid(row=1, column=2, pady=10, padx=(50, 0))
        self.__skins_scrollbar.grid(row=1, column=3, ipady=60)

    def __create_detail_labels(self, master, skin_name, details):
        self.__skin_name_label = Label(master, text='Name: {0}'.format(skin_name), width='30', anchor='w')
        self.__release_date_label = Label(master, text='Release Date: {0}'.format(details['release_date']), width='30',
                                          anchor='w')
        self.__type_label = Label(master, text='Type: {0}'.format(details['type']), width='30', anchor='w')
        self.__skin_status_label = Label(master, text='Status: ', width=20, anchor='w', bg='red')
        self.__price_rp_label = Label(master, text='Riot Points Price: {0}'.format(details['price_rp']), width='30',
                                      anchor='w')
        self.__price_oe_label = Label(master, text='Orange Essence Price: {0}'.format(details['price_orange_essence']),
                                      width='30', anchor='w')

    def __add_detail_labels(self):
        self.__skin_name_label.grid(row=0, column=0, pady=5)
        self.__type_label.grid(row=1, column=0, pady=5)
        self.__price_rp_label.grid(row=2, column=0, pady=5)
        self.__price_oe_label.grid(row=3, column=0, pady=5)
        self.__release_date_label.grid(row=4, column=0, pady=5)
        self.__skin_status_label.grid(row=0, column=1, pady=5)

    def __create_buttons(self, master, skin_name):
        self.__buy_with_oe_button = Button(master, text='Buy With Orange Essence', anchor='w',
                                           command=lambda: self.__buy_skin(skin_name, 1))
        self.__buy_with_rp_button = Button(master, text='Buy With Riot Points', anchor='w',
                                           command=lambda: self.__buy_skin(skin_name, 2))
        self.__add_button = Button(master, text='Add', anchor='w', command=lambda: self.__add_skin(skin_name))

    def __add_buttons(self):
        self.__buy_with_oe_button.grid(row=1, column=1)
        self.__buy_with_rp_button.grid(row=2, column=1)
        self.__add_button.grid(row=4, column=1)

    def __get_details(self, event):
        widget = event.widget
        idx = int(widget.curselection()[0])
        skin_name = widget.get(idx)

        popup = Toplevel()
        popup.title('Details')
        popup.geometry('400x200')
        popup.resizable(False, False)

        details = self.__db.skins[skin_name]
        self.__create_detail_labels(popup, skin_name, details)
        self.__add_detail_labels()
        self.__skin_status_label.config(text='Status: Owned', bg='green')

    def __handle_skin(self, event):
        widget = event.widget
        idx = int(widget.curselection()[0])
        skin_name = widget.get(idx)

        popup = Toplevel()
        popup.title('Details')
        popup.geometry('400x200')
        popup.resizable(False, False)

        details = self.__db.skins[skin_name]
        self.__create_detail_labels(popup, skin_name, details)
        self.__add_detail_labels()
        self.__create_buttons(popup, skin_name)
        self.__add_buttons()
        if self.__root.current_user != '':
            if self.__db.get_champ_name(skin_name) not in self.__db.champions_owned[self.__root.current_user]:
                self.__add_button.config(state=DISABLED)
                self.__buy_with_oe_button.config(state=DISABLED)
                self.__buy_with_rp_button.config(state=DISABLED)
                print('merge')
            if skin_name in self.__db.skins_owned[self.__root.current_user]:
                self.__add_button.config(state=DISABLED)
                self.__buy_with_oe_button.config(state=DISABLED)
                self.__buy_with_rp_button.config(state=DISABLED)
                self.__skin_status_label.config(text='Status: Owned', bg='green')
            else:
                self.__skin_status_label.config(text='Status: Ready To Buy', bg='yellow')

            if self.__db.resources[self.__root.current_user]['riot_points'] < int(details['price_rp']):
                self.__buy_with_rp_button.config(state=DISABLED)
            if self.__db.resources[self.__root.current_user]['orange_essence'] < int(details['price_orange_essence']):
                self.__buy_with_oe_button.config(state=DISABLED)

    def select_owned_skins(self, user_name):
        owned_skins = self.__db.get_owned_skins(user_name)
        self.__owned_skins_list.delete(0, END)
        for skin in owned_skins:
            self.__owned_skins_list.insert(0, skin)

    def select_skins(self):
        skins = [*self.__db.skins.keys()]
        for skin in skins:
            self.__skins_list.insert(0, skin)

    def __buy_skin(self, skin_name, t):
        if self.__root.current_user != '':
            try:
                self.__db.buy_skin(skin_name, self.__root.current_user, t)
            except IntegrityError as e:
                error_obj, = e.args
                print("Not enough resources")
                print("Error Code:", error_obj.code)
                print("Error Message:", error_obj.message)
            else:
                self.__owned_skins_list.insert(0, skin_name)
                self.__add_button.config(state=DISABLED)
                self.__buy_with_oe_button.config(state=DISABLED)
                self.__buy_with_rp_button.config(state=DISABLED)
                if t == 1:
                    self.__root.resources_tab.orange_essence_label.config(text='Orange Essence: '
                                                                               + str(
                        self.__db.resources[self.__root.current_user]['orange_essence']))
                elif t == 2:
                    self.__root.resources_tab.riot_points_label.config(text='Riot Points: '
                                                                            + str(
                        self.__db.resources[self.__root.current_user]['riot_points']))

    def __add_skin(self, skin_name):
        if self.__root.current_user != '':
            self.__db.add_skin(skin_name, self.__root.current_user)
            self.__owned_skins_list.insert(0, skin_name)
            self.__add_button.config(state=DISABLED)
            self.__buy_with_oe_button.config(state=DISABLED)
            self.__buy_with_rp_button.config(state=DISABLED)

    def __add_new_skin_popup(self):
        popup = Toplevel(self.__skins_tab)
        popup.title('Add new Skin')
        popup.geometry('400x300')
        popup.resizable(False, False)

        name_label = Label(popup, text='Name: ', width=20, anchor='w')
        type_label = Label(popup, text='Type: ', width=20, anchor='w')
        price_rp_label = Label(popup, text='Price RP: ', width=20, anchor='w')
        price_oe_label = Label(popup, text='Price Orange Essence: ', width=20, anchor='w')
        release_date_label = Label(popup, text='Release Date: ', width=20, anchor='w')
        champion_label = Label(popup, text='Champion: ', width=20, anchor='w')

        name_entry = Entry(popup, width=30)
        release_date_entry = Entry(popup, width=10)

        champion = ttk.Combobox(popup, state='readonly')
        skin_types = ttk.Combobox(popup, state='readonly')
        rp_prices = ttk.Combobox(popup, state='readonly')
        oe_prices = ttk.Combobox(popup, state='readonly')

        rp_prices['values'] = ('0', '520', '750', '975', '1350', '1820', '2775', '3250')
        oe_prices['values'] = ('220', '450', '675', '1050', '1520', '2150', '2950')
        skin_types['values'] = ('Deluxe', 'Epic', 'Legacy', 'Legendary', 'Mythic',
                                'Standard', 'Timeworn', 'Ultimate')
        champion['values'] = [*self.__db.champions.keys()]

        add_button = Button(popup, text='Add', command=lambda: self.__add_new_skin(popup, name_entry.get(), skin_types.get(),
                                                                                   rp_prices.get(), oe_prices.get(),
                                                                                   release_date_entry.get(),
                                                                                   champion.get()))

        name_label.grid(row=0, column=0, pady=5)
        type_label.grid(row=1, column=0, pady=5)
        price_rp_label.grid(row=2, column=0, pady=5)
        price_oe_label.grid(row=3, column=0, pady=5)
        release_date_label.grid(row=4, column=0, pady=5)
        champion_label.grid(row=5, column=0, pady=5)

        name_entry.grid(row=0, column=1, pady=5)
        skin_types.grid(row=1, column=1, pady=5)
        rp_prices.grid(row=2, column=1, pady=5)
        oe_prices.grid(row=3, column=1, pady=5)
        release_date_entry.grid(row=4, column=1, pady=5)
        champion.grid(row=5, column=1, pady=5)

        add_button.grid(row=6, column=1, pady=5)

    def __add_new_skin(self, master, name, skin_type, price_rp, price_oe, release_date, champion):
        regex = '^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)\d\d$'
        if name == '':
            messagebox.showerror('Error', 'The skin must have a name!')
        if skin_type == '':
            messagebox.showerror('Error', 'The skin must have a type!')
        if price_rp == '':
            messagebox.showerror('Error', 'Select a rp price!')
        if price_oe == '':
            messagebox.showerror('Error', 'Select a blue essence price!')
        if not re.search(regex, release_date):
            messagebox.showerror('Error', 'Wrong date or date format, please use dd.mm.yyyy format!')
        if champion == '':
            messagebox.showerror('Error', 'The skin must belong to a champion!')
        else:
            self.__db.add_new_skin(name, skin_type, price_rp, price_oe, release_date, champion)
            self.__skins_list.insert(0, name)
            master.destroy()

    def clear_owned_skins_list(self):
        self.__owned_skins_list.delete(0, END)
