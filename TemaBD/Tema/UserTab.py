from tkinter import *
from tkinter import ttk, font, messagebox
import re


def create_rank(rank):
    values = ['U']
    for division in ['B', 'S', 'G', 'P', 'D']:
        for subdivision in range(1, 6):
            values.append(division + str(subdivision))
    values.append('M')
    values.append('GM')
    values.append('C')
    rank['values'] = values


class UserTab:
    def __init__(self, tabs, data_base, gui, root):
        self.root = root
        self.gui = gui
        self.db = data_base
        self.tabs = tabs
        self.user_tab = Frame(self.tabs, width='700', height='500', bg='blue')
        self.details_label = None
        self.clubs_label = None
        self.user_label = None
        self.email_label = None
        self.summoner_name_label = None
        self.level_label = None
        self.rank_solo_duo_label = None
        self.rank_flex_label = None
        self.club_label = None

        self.choose_user_button = None
        self.add_user_button = None
        self.delete_user_button = None
        self.add_club_button = None

        self.clubs_list = None
        self.clubs_scrollbar = None

        self.__label_font = font.Font(family="Courier", size=8, weight="bold")

    def create_labels(self):
        self.details_label = Label(self.user_tab, text='Details', width=20, font=('Courier', 10, 'bold'))
        self.clubs_label = Label(self.user_tab, text='Clubs', width=20, font=('Courier', 10, 'bold'))
        self.user_label = Label(self.user_tab, text='Current User:  ', width=40, anchor='w',
                                font=self.__label_font)
        self.email_label = Label(self.user_tab, text='Email:    ', width=40, anchor='w', font=self.__label_font)
        self.summoner_name_label = Label(self.user_tab, text='Summoner Name:    ', width=40, anchor='w',
                                         font=self.__label_font)
        self.level_label = Label(self.user_tab, text='Level:    ', width=40, anchor='w', font=self.__label_font)
        self.rank_solo_duo_label = Label(self.user_tab, text='Rank Solo-Duo:    ', width=40, anchor='w',
                                         font=self.__label_font)
        self.rank_flex_label = Label(self.user_tab, text='Rank Flex:    ', width=40, anchor='w',
                                     font=self.__label_font)
        self.club_label = Label(self.user_tab, text='Club:    ', width=40, anchor='w', font=self.__label_font)

    def add_labels(self):
        self.details_label.grid(row=0, column=0, pady=(50, 10))
        self.clubs_label.grid(row=0, column=2, pady=(50, 10), padx=(100, 0))
        self.user_label.grid(row=1, column=0, pady=10)
        self.email_label.grid(row=2, column=0, pady=10)
        self.summoner_name_label.grid(row=3, column=0, pady=10)
        self.level_label.grid(row=4, column=0, pady=10)
        self.rank_solo_duo_label.grid(row=5, column=0, pady=10)
        self.rank_flex_label.grid(row=6, column=0, pady=10)
        self.club_label.grid(row=7, column=0, pady=10)

    def create_buttons(self):
        self.choose_user_button = Button(self.user_tab, text='Choose User', command=self.choose_user_popup)
        self.add_user_button = Button(self.user_tab, text='Add User', command=self.add_user)
        self.delete_user_button = Button(self.user_tab, text='Delete User', state=DISABLED, command=self.delete_user)
        self.add_club_button = Button(self.user_tab, text='Add Club', command=self.add_club)

    def add_buttons(self):
        self.choose_user_button.grid(row=8, column=0, pady=20)
        self.add_user_button.grid(row=8, column=1, pady=20)
        self.delete_user_button.grid(row=8, column=2, pady=20)
        self.add_club_button.grid(row=8, column=3, pady=20)

    def create_listbox(self):
        self.clubs_list = Listbox(self.user_tab, height=13, width=40, font=self.__label_font)
        self.__add__listbox_scrollbar()
        self.__add_listbox_callback()

    def __add__listbox_scrollbar(self):
        self.clubs_scrollbar = Scrollbar(self.user_tab, orient='vertical',
                                         command=self.clubs_list.yview)
        self.clubs_list.config(yscrollcommand=self.clubs_scrollbar.set)

    def __add_listbox_callback(self):
        self.clubs_list.bind('<Double-Button>', self.__club_details)

    def add_listbox(self):
        self.clubs_list.grid(row=1, column=2, rowspan=4, columnspan=2, padx=(50, 0))
        self.clubs_scrollbar.grid(row=1, column=4, rowspan=4, ipady=74)

    def add_tab(self):
        self.user_tab.pack(fill='both', expand=1)
        self.tabs.add(self.user_tab, text='User')

    def choose_user_popup(self):
        popup = Toplevel()
        popup.title('Choose user')
        popup.geometry('250x100')
        popup.resizable(False, False)

        users = ttk.Combobox(popup, state='readonly')
        users['values'] = self.db.get_users_name()

        select_button = Button(popup, text='Select', command=lambda: self.select(users.get(), popup))

        users.grid(row=0, column=0, columnspan=3, padx=30)
        select_button.grid(row=1, column=0, columnspan=3, pady=50)

    def select(self, user_name, popup):
        if user_name != '':
            self.select_user_details(user_name)
            self.gui.resources_tab.select_resources(user_name)
            self.gui.inventory_tab.select_inventory(user_name)
            self.gui.champions_tab.select_owned_champions(user_name)
            self.gui.skins_tab.select_owned_skins(user_name)
            self.gui.current_user = user_name
            self.delete_user_button.config(state=NORMAL)
            popup.destroy()
        else:
            messagebox.showwarning("Warning", "Please select an user or add a user!")

    def select_user_details(self, user_name):
        self.gui.current_user = user_name
        details = self.db.get_user_details(user_name)
        self.user_label.config(text='Current User:   ' + user_name)
        self.email_label.config(text='Email:   ' + details['email'])
        self.summoner_name_label.config(text='Summoner Name:   ' + details['summoner_name'])
        self.level_label.config(text="Level:   " + str(details['lvl']))
        self.rank_solo_duo_label.config(text='Rank Solo-Duo:   ' + details['rank_solo_duo'])
        self.rank_flex_label.config(text='Rank Flex:   ' + details['rank_flex'])
        self.club_label.config(text='Club:   ' + self.db.get_club_name(user_name))

    def add_user(self):
        popup = Toplevel()
        popup.title('Add User')
        popup.geometry('450x300')
        popup.resizable(False, False)

        name_label = Label(popup, text='Name: ')
        email_label = Label(popup, text='Email: ')
        summoner_name_label = Label(popup, text='Summoner Name: ')
        lvl_label = Label(popup, text='Level: ')
        solo_duo_label = Label(popup, text='Rank Solo-Duo: ')
        flex_label = Label(popup, text='Rank Flex: ')
        club_label = Label(popup, text='Club: ')

        name = Entry(popup, width=30)
        email = Entry(popup, width=50)
        summoner_name = Entry(popup, width=30)
        lvl = Entry(popup, width=20)
        lvl.insert(END, '1')

        solo_duo = ttk.Combobox(popup, state='readonly')
        flex = ttk.Combobox(popup, state='readonly')
        club = ttk.Combobox(popup, state='readonly')

        create_rank(solo_duo)
        create_rank(flex)
        club['values'] = [*self.db.clubs.keys()]
        solo_duo.current(0)
        flex.current(0)

        name_label.grid(row=0, column=0, pady=5)
        email_label.grid(row=1, column=0, pady=5)
        summoner_name_label.grid(row=2, column=0, pady=5)
        lvl_label.grid(row=3, column=0, pady=5)
        solo_duo_label.grid(row=4, column=0, pady=5)
        flex_label.grid(row=5, column=0, pady=5)
        club_label.grid(row=6, column=0, pady=5)

        name.grid(row=0, column=1)
        email.grid(row=1, column=1)
        summoner_name.grid(row=2, column=1)
        lvl.grid(row=3, column=1)
        solo_duo.grid(row=4, column=1)
        flex.grid(row=5, column=1)
        club.grid(row=6, column=1)

        add_button = Button(popup, text='Add',
                            command=lambda: self.__add_user(name.get(), email.get(),
                                                            summoner_name.get(), lvl.get(),
                                                            solo_duo.get(), flex.get(), club.get(), popup))

        add_button.grid(row=7, columnspan=2, pady=30)

    def __add_user(self, name, email, summoner_name, lvl, solo_duo, flex, club, popup):
        regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if len(name) < 5:
            messagebox.showerror('Error', 'The length of the name must be at least 5 characters!')
        if len(summoner_name) < 5:
            messagebox.showerror('Error', 'The length of the summoner name must be at least 5 characters!')
        if not re.search(regex, email):
            messagebox.showerror('Error', 'Invalid email address!')
        if len(club) == 0:
            messagebox.showerror('Error', 'You need to be in a Club!\nCreate one or select one!')
        else:
            self.db.insert_user(name, email, summoner_name, lvl, solo_duo, flex, club)
            popup.destroy()

    def __club_details(self, event):
        popup = Toplevel(self.user_tab)
        popup.title('Details')
        popup.geometry('250x150')
        popup.resizable(False, False)

        widget = event.widget
        idx = int(widget.curselection()[0])
        name = widget.get(idx)
        details = self.db.clubs[name]

        name_label = Label(popup, text='Name: {0}'.format(name), width=20, bg='yellow')
        create_date_label = Label(popup, text='Create Date: {0}'.format(details['create_date']), width=20, bg='yellow')
        num_of_members_label = Label(popup, text='Number Of Members: {0}'.format(details['number_of_members']), width=20, bg='yellow')

        name_label.grid(row=0, column=0, pady=15, padx=50)
        create_date_label.grid(row=1, column=0, pady=15)
        num_of_members_label.grid(row=2, column=0, pady=15)

    def add_club(self):
        popup = Toplevel(self.user_tab)
        popup.title('Add Club')
        popup.geometry('300x200')
        popup.resizable(False, False)

        name_label = Label(popup, text='Name: ', width=20, anchor='w')
        create_date_label = Label(popup, text='Create Date: ', width=20, anchor='w')
        num_of_members_label = Label(popup, text='Number Of Members: ', width=20, anchor='w')

        name_entry = Entry(popup, width=20)
        create_date_entry = Entry(popup, width=20)
        num_of_members_entry = Entry(popup, width=20)

        add_button = Button(popup, text='Add', command=lambda: self.__add_club(popup, name_entry.get(),
                                                                               create_date_entry.get(),
                                                                               num_of_members_entry.get()))

        name_label.grid(row=0, column=0, pady=15)
        create_date_label.grid(row=1, column=0, pady=15)
        num_of_members_label.grid(row=2, column=0, pady=15)

        name_entry.grid(row=0, column=1, pady=15)
        create_date_entry.grid(row=1, column=1, pady=15)
        num_of_members_entry.grid(row=2, column=1, pady=15)

        add_button.grid(row=3, column=0, columnspan=2, pady=5)

    def __add_club(self, master, name, create_date, num_of_members):
        regex = '^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)\d\d$'
        if name == '':
            messagebox.showerror('Error', 'Please insert a name!')
        elif len(name) < 4:
            messagebox.showerror('Error', 'The length of the name must be at least 4 characters!')
        if not re.search(regex, create_date):
            messagebox.showerror('Error', 'Wrong date or date format, please use dd.mm.yyyy format!')
        if num_of_members == '':
            messagebox.showerror('Error', 'Specify the number of members!')
        elif int(num_of_members) > 100:
            messagebox.showerror('Error', 'The maximum number of members is 100!')
        else:
            self.db.add_club(name, create_date, num_of_members)
            self.clubs_list.insert(0, name)
            master.destroy()

    def select_clubs(self):
        clubs = [*self.db.clubs.keys()]
        for club in clubs:
            self.clubs_list.insert(0, club)

    def delete_user(self):
        self.db.delete_user(self.gui.current_user)
        self.gui.current_user = ''
        self.gui.clear_labels()
        self.delete_user_button.config(state=DISABLED)

    def clear_labels(self):
        self.user_label.config(text='Current User:   ')
        self.email_label.config(text='Email:   ')
        self.summoner_name_label.config(text='Summoner Name:   ')
        self.level_label.config(text='Level:   ')
        self.rank_solo_duo_label.config(text='Rank Solo-Duo:   ')
        self.rank_flex_label.config(text='Rank Flex:   ')
        self.club_label.config(text='Club:   ')
