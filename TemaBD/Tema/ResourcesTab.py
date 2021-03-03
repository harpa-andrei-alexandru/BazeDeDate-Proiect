from tkinter import *
from tkinter import font, messagebox


class ResourcesTab:
    def __init__(self, tabs, data_base, root):
        self.root = root
        self.db = data_base
        self.tabs = tabs
        self.resources_tab = Frame(self.tabs, width='700', height='500', bg='pink')
        self.resources_label = None
        self.riot_points_label = None
        self.blue_essence_label = None
        self.orange_essence_label = None

        self.__add_blue_essence_button = None
        self.__add_orange_essence_button = None
        self.__add_riot_points_button = None

        self.__blue_essence_entry = None
        self.__orange_essence_entry = None
        self.__riot_points_entry = None

        self.__label_font = font.Font(family="Courier", size=8, weight="bold")

    def create_labels(self):
        self.resources_label = Label(self.resources_tab, text='Resources', width=20, font=('Courier', 10, 'bold'))
        self.riot_points_label = Label(self.resources_tab, text='Riot Points: ', width=40, anchor='w',
                                       font=self.__label_font)
        self.blue_essence_label = Label(self.resources_tab, text='Blue Essences: ', width=40, anchor='w',
                                        font=self.__label_font)
        self.orange_essence_label = Label(self.resources_tab, text='Orange Essences: ', width=40, anchor='w',
                                          font=self.__label_font)

    def create_buttons(self):
        self.__add_blue_essence_button = Button(self.resources_tab, text='Add blue essence', command=self.__add_blue_essence)
        self.__add_orange_essence_button = Button(self.resources_tab, text='Add orange essence', command=self.__add_orange_essence)
        self.__add_riot_points_button = Button(self.resources_tab, text='Add riot points', command=self.__add_riot_points)

    def create_entries(self):
        self.__riot_points_entry = Entry(self.resources_tab, width='10')
        self.__blue_essence_entry = Entry(self.resources_tab, width='10')
        self.__orange_essence_entry = Entry(self.resources_tab, width='10')

        self.__riot_points_entry.insert(END, '0')
        self.__blue_essence_entry.insert(END, '0')
        self.__orange_essence_entry.insert(END, '0')

    def add_entries(self):
        self.__riot_points_entry.grid(row=1, column=1, padx=10)
        self.__blue_essence_entry.grid(row=2, column=1, padx=10)
        self.__orange_essence_entry.grid(row=3, column=1, padx=10)

    def add_labels(self):
        self.resources_label.grid(row=0, column=0, pady=(120, 20))
        self.riot_points_label.grid(row=1, column=0, pady=15)
        self.blue_essence_label.grid(row=2, column=0, pady=15)
        self.orange_essence_label.grid(row=3, column=0, pady=15)

    def add_buttons(self):
        self.__add_riot_points_button.grid(row=1, column=2, padx=10)
        self.__add_blue_essence_button.grid(row=2, column=2, padx=10)
        self.__add_orange_essence_button.grid(row=3, column=2, padx=10)

    def add_tab(self):
        self.resources_tab.pack(fill='both', expand=1)
        self.tabs.add(self.resources_tab, text='Resources')

    def select_resources(self, user_name):
        resources = self.db.get_user_resources(user_name)
        self.riot_points_label.config(text='Riot Points: ' + str(resources['riot_points']))
        self.blue_essence_label.config(text='Blue Essence: ' + str(resources['blue_essence']))
        self.orange_essence_label.config(text='Orange Essence: ' + str(resources['orange_essence']))

    def __add_riot_points(self):
        if self.root.current_user != '':
            amount = int(self.__riot_points_entry.get())
            if amount < 0:
                messagebox.showwarning('warning', 'The quantity must be a positive integer!')
            else:
                self.db.add_riot_points(amount, self.root.current_user)
                new_amount = self.db.resources[self.root.current_user]['riot_points']
                self.riot_points_label.config(text='Riot Points: ' + str(new_amount))
                self.__riot_points_entry.delete(0, END)
                self.__riot_points_entry.insert(0, '0')

    def __add_blue_essence(self):
        if self.root.current_user != '':
            amount = int(self.__blue_essence_entry.get())
            if amount < 0:
                messagebox.showwarning('warning', 'The quantity must be a positive integer!')
            else:
                self.db.add_blue_essence(amount, self.root.current_user)
                new_amount = self.db.resources[self.root.current_user]['blue_essence']
                self.blue_essence_label.config(text='Blue Essence: ' + str(new_amount))
                self.__blue_essence_entry.delete(0, END)
                self.__blue_essence_entry.insert(0, '0')

    def __add_orange_essence(self):
        if self.root.current_user != '':
            amount = int(self.__orange_essence_entry.get())
            if amount < 0:
                messagebox.showwarning('warning', 'The quantity must be a positive integer!')
            else:
                self.db.add_orange_essence(amount, self.root.current_user)
                new_amount = self.db.resources[self.root.current_user]['orange_essence']
                self.orange_essence_label.config(text='Orange Essence: ' + str(new_amount))
                self.__orange_essence_entry.delete(0, END)
                self.__orange_essence_entry.insert(0, '0')

    def clear_labels(self):
        self.riot_points_label.config(text='Riot Points: ')
        self.blue_essence_label.config(text='Blue Essence: ')
        self.orange_essence_label.config(text='Orange Essence: ')

