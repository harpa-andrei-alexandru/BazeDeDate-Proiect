from tkinter import *
from tkinter import ttk

import DataBase
import UserTab
import ResourcesTab
import InventoryTab
import ChampionsTab
import SkinsTab

host = 'bd-dc.cs.tuiasi.ro'
port = '1539'
user = 'bd021'
password = 'lab05'
service = 'orcl'


class GUI:
    def __init__(self, root):
        self.current_user = ''
        self.db = DataBase.DataBase(host, port, user, password, service)
        self.tabs = ttk.Notebook(root)
        self.user_tab = UserTab.UserTab(self.tabs, self.db, self, root)
        self.resources_tab = ResourcesTab.ResourcesTab(self.tabs, self.db, self)
        self.inventory_tab = InventoryTab.InventoryTab(self.tabs, self.db, self)
        self.champions_tab = ChampionsTab.ChampionsTab(self.tabs, self.db, self)
        self.skins_tab = SkinsTab.SkinsTab(self.tabs, self.db, self)

        self.create_tab_labels()
        self.add_tab_labels()
        self.create_tab_buttons()
        self.add_tab_buttons()
        self.create_tab_entries()
        self.add_tab_entries()
        self.create_tab_listbox()
        self.add_tab_listbox()

        self.add_tabs()
        self.get_data()
        self.commit_button = Button(root, text='Commit', command=self.db.commit)
        self.tabs.grid(row=0, column=0)
        self.commit_button.grid(row=0, column=1)

    def get_data(self):
        self.db.connect()
        self.db.get_users()
        self.db.get_clubs()
        self.user_tab.select_clubs()
        self.db.get_resources()
        self.db.get_inventories()
        self.db.get_champions()
        self.db.get_skins()
        self.champions_tab.select_champions()
        self.skins_tab.select_skins()

    def create_tab_labels(self):
        self.user_tab.create_labels()
        self.resources_tab.create_labels()
        self.inventory_tab.create_labels()
        self.champions_tab.create_labels()
        self.skins_tab.create_labels()

    def add_tab_labels(self):
        self.user_tab.add_labels()
        self.resources_tab.add_labels()
        self.inventory_tab.add_labels()
        self.champions_tab.add_labels()
        self.skins_tab.add_labels()

    def create_tab_entries(self):
        self.inventory_tab.create_entries()
        self.resources_tab.create_entries()

    def add_tab_entries(self):
        self.inventory_tab.add_entries()
        self.resources_tab.add_entries()

    def create_tab_buttons(self):
        self.user_tab.create_buttons()
        self.inventory_tab.create_buttons()
        self.resources_tab.create_buttons()
        self.champions_tab.create_buttons()
        self.skins_tab.create_buttons()

    def add_tab_buttons(self):
        self.user_tab.add_buttons()
        self.inventory_tab.add_buttons()
        self.resources_tab.add_buttons()
        self.champions_tab.add_buttons()
        self.skins_tab.add_buttons()

    def create_tab_listbox(self):
        self.user_tab.create_listbox()
        self.champions_tab.create_listbox()
        self.skins_tab.create_listbox()

    def add_tab_listbox(self):
        self.user_tab.add_listbox()
        self.champions_tab.add_listbox()
        self.skins_tab.add_listbox()

    def add_tabs(self):
        self.user_tab.add_tab()
        self.resources_tab.add_tab()
        self.inventory_tab.add_tab()
        self.champions_tab.add_tab()
        self.skins_tab.add_tab()

    def clear_labels(self):
        self.user_tab.clear_labels()
        self.resources_tab.clear_labels()
        self.inventory_tab.clear_labels()
        self.champions_tab.clear_owned_champions_list()
        self.skins_tab.clear_owned_skins_list()
