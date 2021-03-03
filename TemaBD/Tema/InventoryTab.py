from tkinter import *
from tkinter import font, messagebox


class InventoryTab:
    def __init__(self, tabs, data_base, root):
        self.root = root
        self.db = data_base
        self.tabs = tabs
        self.inventory_tab = Frame(self.tabs, width='700', height='500', bg='purple')
        self.inventory_label = None
        self.champion_chests_label = None
        self.skin_chests_label = None
        self.chest_keys_label = None
        self.key_fragments_label = None
        self.gemstones_label = None

        self.__label_font = font.Font(family="Courier", size=8, weight="bold")
        self.__add_chest_keys_button = None
        self.__add_champion_chests_button = None
        self.__add_skin_chests_button = None
        self.__add_key_fragments_button = None
        self.__add_gemstones_button = None

        self.__chest_keys_entry = None
        self.__champion_chests_entry = None
        self.__skin_chests_entry = None
        self.__key_fragments_entry = None
        self.__gemstones_entry = None

    def create_labels(self):
        self.inventory_label = Label(self.inventory_tab, text='Inventory', width=20, font=('Courier', 10, 'bold'))
        self.champion_chests_label = Label(self.inventory_tab, text='Champion Chests: ', width=40, anchor='w',
                                           font=self.__label_font)
        self.skin_chests_label = Label(self.inventory_tab, text='Skin Chests: ', width=40, anchor='w',
                                       font=self.__label_font)
        self.chest_keys_label = Label(self.inventory_tab, text='Chest Keys: ', width=40, anchor='w',
                                      font=self.__label_font)
        self.key_fragments_label = Label(self.inventory_tab, text='Key Fragments: ', width=40, anchor='w',
                                         font=self.__label_font)
        self.gemstones_label = Label(self.inventory_tab, text='Gemstones', width=40, anchor='w',
                                     font=self.__label_font)

    def create_buttons(self):
        self.__add_chest_keys_button = Button(self.inventory_tab, text='Add Chest Keys', command=self.__add_chest_keys)
        self.__add_champion_chests_button = Button(self.inventory_tab, text='Add Champion Chests', command=self.__add_champion_chests)
        self.__add_skin_chests_button = Button(self.inventory_tab, text='Add Skin Chests', command=self.__add_skin_chests)
        self.__add_key_fragments_button = Button(self.inventory_tab, text='Add Key Fragments', command=self.__add_key_fragments)
        self.__add_gemstones_button = Button(self.inventory_tab, text='Add Gemstones', command=self.__add_gemstones)

    def create_entries(self):
        self.__champion_chests_entry = Entry(self.inventory_tab, width='10')
        self.__chest_keys_entry = Entry(self.inventory_tab, width='10')
        self.__skin_chests_entry = Entry(self.inventory_tab, width='10')
        self.__key_fragments_entry = Entry(self.inventory_tab, width='10')
        self.__gemstones_entry = Entry(self.inventory_tab, width='10')

        self.__champion_chests_entry.insert(END, '0')
        self.__skin_chests_entry.insert(END, '0')
        self.__chest_keys_entry.insert(END, '0')
        self.__key_fragments_entry.insert(END, '0')
        self.__gemstones_entry.insert(END, '0')

    def add_entries(self):
        self.__champion_chests_entry.grid(row=1, column=1, padx=10)
        self.__skin_chests_entry.grid(row=2, column=1, padx=10)
        self.__chest_keys_entry.grid(row=3, column=1, padx=10)
        self.__key_fragments_entry.grid(row=4, column=1, padx=10)
        self.__gemstones_entry.grid(row=5, column=1, padx=10)

    def add_labels(self):
        self.inventory_label.grid(row=0, column=0, pady=(100, 10))
        self.champion_chests_label.grid(row=1, column=0, pady=10)
        self.skin_chests_label.grid(row=2, column=0, pady=10)
        self.chest_keys_label.grid(row=3, column=0, pady=10)
        self.key_fragments_label.grid(row=4, column=0, pady=10)
        self.gemstones_label.grid(row=5, column=0, pady=10)

    def add_buttons(self):
        self.__add_champion_chests_button.grid(row=1, column=2, padx=10)
        self.__add_skin_chests_button.grid(row=2, column=2, padx=10)
        self.__add_chest_keys_button.grid(row=3, column=2, padx=10)
        self.__add_key_fragments_button.grid(row=4, column=2, padx=10)
        self.__add_gemstones_button.grid(row=5, column=2, padx=10)

    def add_tab(self):
        self.inventory_tab.pack(fill='both', expand=1)
        self.tabs.add(self.inventory_tab, text='Inventory')

    def select_inventory(self, user_name):
        inventory = self.db.get_user_inventory(user_name)
        self.champion_chests_label.config(text='Champion Chests: ' + str(inventory['champion_chests']))
        self.skin_chests_label.config(text='Skin Chests: ' + str(inventory['skin_chests']))
        self.chest_keys_label.config(text='Chest Keys: ' + str(inventory['chest_keys']))
        self.key_fragments_label.config(text='Key Fragments: ' + str(inventory['key_fragments']))
        self.gemstones_label.config(text='Gemstones: ' + str(inventory['gemstones']))

    def __add_chest_keys(self):
        if self.root.current_user != '':
            amount = int(self.__chest_keys_entry.get())
            if amount < 0:
                messagebox.showwarning('warning', 'The quantity must be a positive integer!')
            else:
                self.db.add_chest_keys(amount, self.root.current_user)
                new_amount = self.db.inventories[self.root.current_user]['chest_keys']
                self.chest_keys_label.config(text='Chest Keys: ' + str(new_amount))
                self.__chest_keys_entry.delete(0, END)
                self.__chest_keys_entry.insert(0, '0')

    def __add_champion_chests(self):
        if self.root.current_user != '':
            amount = int(self.__champion_chests_entry.get())
            if amount < 0:
                messagebox.showwarning('warning', 'The quantity must be a positive integer!')
            else:
                self.db.add_champion_chests(amount, self.root.current_user)
                new_amount = self.db.inventories[self.root.current_user]['champion_chests']
                self.champion_chests_label.config(text='Champion Chests: ' + str(new_amount))
                self.__champion_chests_entry.delete(0, END)
                self.__champion_chests_entry.insert(0, '0')

    def __add_skin_chests(self):
        if self.root.current_user != '':
            amount = int(self.__skin_chests_entry.get())
            if amount < 0:
                messagebox.showwarning('warning', 'The quantity must be a positive integer!')
            else:
                self.db.add_skin_chests(amount, self.root.current_user)
                new_amount = self.db.inventories[self.root.current_user]['skin_chests']
                self.skin_chests_label.config(text='Skin Chests: ' + str(new_amount))
                self.__skin_chests_entry.delete(0, END)
                self.__skin_chests_entry.insert(0, '0')

    def __add_key_fragments(self):
        if self.root.current_user != '':
            amount = int(self.__key_fragments_entry.get())
            if amount < 0:
                messagebox.showwarning('warning', 'The quantity must be a positive integer!')
            else:
                self.db.add_key_fragments(amount, self.root.current_user)
                new_amount = self.db.inventories[self.root.current_user]['key_fragments']
                self.key_fragments_label.config(text='Key Fragments: ' + str(new_amount))
                self.__key_fragments_entry.delete(0, END)
                self.__key_fragments_entry.insert(0, '0')

    def __add_gemstones(self):
        if self.root.current_user != '':
            amount = int(self.__gemstones_entry.get())
            if amount < 0:
                messagebox.showwarning('warning', 'The quantity must be a positive integer!')
            else:
                self.db.add_gemstones(amount, self.root.current_user)
                new_amount = self.db.inventories[self.root.current_user]['gemstones']
                self.gemstones_label.config(text='Gemstones: ' + str(new_amount))
                self.__gemstones_entry.delete(0, END)
                self.__gemstones_entry.insert(0, '0')

    def clear_labels(self):
        self.champion_chests_label.config(text='Champion Chests: ')
        self.skin_chests_label.config(text='Skin Chests: ')
        self.chest_keys_label.config(text='Chest Keys: ')
        self.key_fragments_label.config(text='Key Fragments: ')
        self.gemstones_label.config(text='Gemstones: ')
