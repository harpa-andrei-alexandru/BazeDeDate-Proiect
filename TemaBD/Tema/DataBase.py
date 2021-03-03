import cx_Oracle
from datetime import datetime


class DataBase:
    def __init__(self, host, port, user, password, service):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.service = service
        self.cursor = None
        self.conn = None
        self.users = {}
        self.clubs = {}
        self.resources = {}
        self.inventories = {}
        self.champions = {}
        self.champions_owned = {}
        self.skins = {}
        self.skins_owned = {}

    def connect(self):
        conn_str = self.user + '/' + self.password + '@' + self.host \
                   + ':' + self.port + '/' + self.service
        cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_19_9")
        self.conn = cx_Oracle.connect(conn_str)
        self.cursor = self.conn.cursor()

    def get_users(self):
        self.cursor.execute("""
                SELECT * 
                FROM lol_user
                """)
        for result in self.cursor:
            details = {'user_id': result[0], 'email': result[2], 'summoner_name': result[3], 'lvl': result[4],
                       'rank_solo_duo': result[5], 'rank_flex': result[6], 'club_id': result[7]}
            self.users[result[1]] = details
            print(self.users[result[1]])

    def get_users_name(self):
        return [*self.users.keys()]

    def get_user_details(self, user_name):
        print(self.users[user_name])
        return self.users[user_name]

    def get_clubs(self):
        self.cursor.execute("""
            SELECT * 
            FROM club
        """)
        for result in self.cursor:
            details = {'club_id': result[0], 'create_date': datetime.strptime(str(result[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y'),
                       'number_of_members': result[3]}
            self.clubs[result[1]] = details

    def get_club_name(self, user_name):
        self.cursor.execute("""
            SELECT name
            FROM club
            WHERE club_id=(SELECT club_id
                            FROM lol_user
                            WHERE name='{0}')  
        """.format(user_name))
        for club in self.cursor:
            return club[0]

    def insert_user(self, name, email, sum_name, lvl, rank_s_d, rank_flex, club):
        self.cursor.execute("""
        INSERT INTO lol_user(name, email, summoner_name, lvl, rank_solo_duo, rank_flex, club_id) 
        VALUES('{0}', '{1}', '{2}', {3}, '{4}', '{5}', 
                (SELECT club_id
                FROM club 
                WHERE name='{6}'))
        """.format(name, email, sum_name, lvl, rank_s_d, rank_flex, club))
        # update the users dict
        self.__add_user(name)
        self.__create_inventory(name)
        self.__create_resources(name)

    def __add_user(self, user_name):
        self.cursor.execute("""
                        SELECT * 
                        FROM lol_user
                        WHERE name='{0}'
                        """.format(user_name))
        for result in self.cursor:
            details = {'user_id': result[0], 'email': result[2], 'summoner_name': result[3], 'lvl': result[4],
                       'rank_solo_duo': result[5], 'rank_flex': result[6], 'club_id': result[7]}
            self.users[result[1]] = details
            print(self.users[result[1]])

    def __create_inventory(self, user_name):
        self.cursor.execute("""
            INSERT INTO inventory
            VALUES(0, 0, 0, 0, 0, (SELECT user_id
                                   FROM lol_user
                                   WHERE name='{0}'))
        """.format(user_name))
        self.inventories[user_name] = {}
        self.inventories[user_name]['champion_chests'] = 0
        self.inventories[user_name]['skin_chests'] = 0
        self.inventories[user_name]['chest_keys'] = 0
        self.inventories[user_name]['key_fragments'] = 0
        self.inventories[user_name]['gemstones'] = 0

    def __create_resources(self, user_name):
        self.cursor.execute("""
                    INSERT INTO resources
                    VALUES(0, 0, 0, (SELECT user_id
                                     FROM lol_user
                                     WHERE name='{0}'))
                """.format(user_name))
        self.resources[user_name] = {}
        self.resources[user_name]['riot_points'] = 0
        self.resources[user_name]['blue_essence'] = 0
        self.resources[user_name]['orange_essence'] = 0

    def get_resources(self):
        self.cursor.execute("""
            SELECT l.name, r.riot_points, r.blue_essence, r.orange_essence
            FROM lol_user l, resources r
            WHERE l.user_id=r.user_id
        """)
        for result in self.cursor:
            temp = {'riot_points': result[1], 'blue_essence': result[2], 'orange_essence': result[3]}
            self.resources[result[0]] = temp

    def get_user_resources(self, user_name):
        return self.resources[user_name]

    def get_inventories(self):
        self.cursor.execute("""
                    SELECT l.name, i.champion_chests, i.skin_chests, i.chest_keys, 
                        i.key_fragments, i.gemstones
                    FROM lol_user l, inventory i
                    WHERE l.user_id=i.user_id
                """)
        for result in self.cursor:
            temp = {'champion_chests': result[1], 'skin_chests': result[2], 'chest_keys': result[3],
                    'key_fragments': result[4], 'gemstones': result[5]}
            self.inventories[result[0]] = temp

    def get_user_inventory(self, user_name):
        return self.inventories[user_name]

    def get_champions(self):
        self.cursor.execute("""
            SELECT * 
            FROM champion 
        """)
        for champion in self.cursor:
            details = {'champion_id': champion[0], 'price_rp': champion[2], 'price_blue_essence': champion[3],
                       'release_date': datetime.strptime(str(champion[4]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y'),
                       'health': champion[5], 'armor': champion[6], 'magic_resist': champion[7],
                       'attack_damage': champion[8]}
            self.champions[champion[1]] = details

    def get_skins(self):
        self.cursor.execute("""
            SELECT * 
            FROM skin 
        """)
        for skin in self.cursor:
            details = {'skin_id': skin[0], 'type': skin[2], 'price_orange_essence': skin[3], 'price_rp': skin[4],
                       'release_date': datetime.strptime(str(skin[5]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y'),
                       'champion_id': skin[6]}
            self.skins[skin[1]] = details

    def get_owned_champions(self, user_name):
        if user_name not in self.champions_owned:
            self.cursor.execute("""
                SELECT c.champion_name 
                FROM champion c, user_champion uc
                WHERE uc.user_id=(SELECT user_id
                                  FROM lol_user
                                  WHERE name='{0}')
                AND uc.champion_id=c.champion_id
            """.format(user_name))
            champions = []
            for champion in self.cursor:
                champions.append(champion[0])

            self.champions_owned[user_name] = champions

        return self.champions_owned[user_name]

    def get_owned_skins(self, user_name):
        if user_name not in self.skins_owned:
            self.cursor.execute("""
                SELECT s.skin_name 
                FROM skin s, user_skin us
                WHERE us.user_id=(SELECT user_id
                                  FROM lol_user
                                  WHERE name='{0}')
                AND us.skin_id=s.skin_id
            """.format(user_name))
            skins = []
            for skin in self.cursor:
                skins.append(skin[0])

            self.skins_owned[user_name] = skins

        return self.skins_owned[user_name]

    def add_champion(self, champion_name, user_name):
        self.cursor.execute("""
            INSERT INTO user_champion
            VALUES((SELECT user_id
                    FROM lol_user
                    WHERE name='{1}'),
                   (SELECT champion_id
                    FROM champion
                    WHERE champion_name='{0}'))
        """.format(champion_name, user_name))
        self.champions_owned[user_name].append(champion_name)

    def buy_champion(self, champion_name, user_name, t):
        if t == 1:
            self.cursor.execute("""
                UPDATE resources
                SET blue_essence = blue_essence - (SELECT price_blue_essence
                                                   FROM champion
                                                   WHERE champion_name='{0}')
                WHERE user_id=(SELECT user_id
                               FROM lol_user
                               WHERE name='{1}')
            """.format(champion_name, user_name))
            self.add_champion(champion_name, user_name)
            self.resources[user_name]['blue_essence'] -= int(self.champions[champion_name]['price_blue_essence'])
        elif t == 2:
            self.cursor.execute("""
                UPDATE resources
                SET riot_points = riot_points - (SELECT price_rp
                                                 FROM champion
                                                 WHERE champion_name='{0}')
                WHERE user_id=(SELECT user_id
                               FROM lol_user
                               WHERE name='{1}')
            """.format(champion_name, user_name))
            self.add_champion(champion_name, user_name)
            self.resources[user_name]['riot_points'] -= int(self.champions[champion_name]['price_rp'])

    def buy_skin(self, skin_name, user_name, t):
        if t == 1:
            self.cursor.execute("""
                UPDATE resources
                SET orange_essence = orange_essence - (SELECT price_orange_essence
                                                   FROM skin
                                                   WHERE skin_name='{0}')
                WHERE user_id=(SELECT user_id
                               FROM lol_user
                               WHERE name='{1}')
            """.format(skin_name, user_name))
            self.add_skin(skin_name, user_name)
            self.resources[user_name]['orange_essence'] -= int(self.skins[skin_name]['price_orange_essence'])
        elif t == 2:
            self.cursor.execute("""
                UPDATE resources
                SET riot_points = riot_points - (SELECT price_rp
                                                 FROM skin
                                                 WHERE skin_name='{0}')
                WHERE user_id=(SELECT user_id
                               FROM lol_user
                               WHERE name='{1}')
            """.format(skin_name, user_name))
            self.add_skin(skin_name, user_name)
            self.resources[user_name]['riot_points'] -= int(self.skins[skin_name]['price_rp'])

    def add_skin(self, skin_name, user_name):
        self.cursor.execute("""
            INSERT INTO user_skin
            VALUES((SELECT user_id
                    FROM lol_user
                    WHERE name='{0}'), {1},
                   (SELECT skin_id
                    FROM skin
                    WHERE skin_name='{2}'))
        """.format(user_name, self.skins[skin_name]['champion_id'], skin_name))
        self.skins_owned[user_name].append(skin_name)

    def update_champion(self, champion_name, health, armor, attack_damage, magic_resist):
        self.cursor.execute("""
            UPDATE champion
            SET health={0}, armor={1}, attack_damage={2}, magic_resist={3}
            WHERE champion_name='{4}'
        """.format(health, armor, attack_damage, magic_resist, champion_name))
        self.champions[champion_name]['health'] = health
        self.champions[champion_name]['armor'] = armor
        self.champions[champion_name]['attack_damage'] = attack_damage
        self.champions[champion_name]['magic_resist'] = magic_resist

    def add_new_champion(self, name, health, armor, attack, magic_resist, price_rp, price_be, release_date):
        self.cursor.execute("""
        INSERT INTO champion(champion_name, price_rp, price_blue_essence,
                             release_date, health, armor, magic_resist, attack_damage) 
        VALUES('{0}', {1}, {2}, TO_DATE('{3}', 'DD.MM.YYYY'), {4}, {5}, {6}, {7})
        """.format(name, price_rp, price_be, release_date, health, armor, magic_resist, attack))
        self.champions[name] = {'champion_id': 1, 'price_rp': price_rp, 'price_blue_essence': price_be,
                                'release_date': release_date,
                                'health': health, 'armor': armor, 'magic_resist': magic_resist,
                                'attack_damage': attack}

    def add_new_skin(self, name, skin_type, price_rp, price_oe, release_date, champion):
        self.cursor.execute("""
        INSERT INTO skin(skin_name, type, price_rp, price_orange_essence, release_date, champion_id) 
        VALUES('{0}', '{1}', {2}, {3}, TO_DATE('{4}', 'DD.MM.YYYY'), (SELECT champion_id
                                                                      FROM champion
                                                                      WHERE champion_name='{5}'))
        """.format(name, skin_type, price_rp, price_oe, release_date, champion))
        self.skins[name] = {'skin_id': 1, 'price_rp': price_rp, 'price_orange_essence': price_oe,
                            'release_date': release_date,
                            'type': skin_type, 'champion_id': self.champions[champion]['champion_id']}

    def add_chest_keys(self, amount, user_name):
        self.cursor.execute("""
            UPDATE inventory
            SET chest_keys=chest_keys + {0}
            WHERE user_id=(SELECT user_id
                           FROM lol_user
                           WHERE name='{1}')
        """.format(amount, user_name))
        self.inventories[user_name]['chest_keys'] += amount

    def add_champion_chests(self, amount, user_name):
        self.cursor.execute("""
            UPDATE inventory
            SET champion_chests=champion_chests + {0}
            WHERE user_id=(SELECT user_id
                           FROM lol_user
                           WHERE name='{1}')
        """.format(amount, user_name))
        self.inventories[user_name]['champion_chests'] += amount

    def add_skin_chests(self, amount, user_name):
        self.cursor.execute("""
            UPDATE inventory
            SET skin_chests=skin_chests + {0}
            WHERE user_id=(SELECT user_id
                           FROM lol_user
                           WHERE name='{1}')
        """.format(amount, user_name))
        self.inventories[user_name]['skin_chests'] += amount

    def add_key_fragments(self, amount, user_name):
        self.cursor.execute("""
            UPDATE inventory
            SET key_fragments=key_fragments + {0}
            WHERE user_id=(SELECT user_id
                           FROM lol_user
                           WHERE name='{1}')
        """.format(amount, user_name))
        self.inventories[user_name]['key_fragments'] += amount

    def add_gemstones(self, amount, user_name):
        self.cursor.execute("""
            UPDATE inventory
            SET gemstones=gemstones + {0}
            WHERE user_id=(SELECT user_id
                           FROM lol_user
                           WHERE name='{1}')
        """.format(amount, user_name))
        self.inventories[user_name]['gemstones'] += amount

    def add_riot_points(self, amount, user_name):
        self.cursor.execute("""
            UPDATE resources
            SET riot_points=riot_points + {0}
            WHERE user_id=(SELECT user_id
                           FROM lol_user
                           WHERE name='{1}')
        """.format(amount, user_name))
        self.resources[user_name]['riot_points'] += amount

    def add_blue_essence(self, amount, user_name):
        self.cursor.execute("""
            UPDATE resources
            SET blue_essence=blue_essence + {0}
            WHERE user_id=(SELECT user_id
                           FROM lol_user
                           WHERE name='{1}')
        """.format(amount, user_name))
        self.resources[user_name]['blue_essence'] += amount

    def add_orange_essence(self, amount, user_name):
        self.cursor.execute("""
            UPDATE resources
            SET orange_essence=orange_essence + {0}
            WHERE user_id=(SELECT user_id
                           FROM lol_user
                           WHERE name='{1}')
        """.format(amount, user_name))
        self.resources[user_name]['orange_essence'] += amount

    def add_club(self, name, create_date, num_of_members):
        self.cursor.execute("""
        INSERT INTO club(name, create_date, number_of_members)
        VALUES('{0}', TO_DATE('{1}', 'DD.MM.YYYY'), {2})
        """.format(name, create_date, num_of_members))
        self.clubs[name] = {'create_date': create_date, 'number_of_members': num_of_members}

    def delete_user(self, user_name):
        self.cursor.execute("""
            DELETE FROM resources
            WHERE user_id=(SELECT user_id
                           FROM lol_user
                           WHERE name='{0}')
        """.format(user_name))
        del self.resources[user_name]
        print('resources')

        self.cursor.execute("""
            DELETE FROM inventory
            WHERE user_id=(SELECT user_id
                           FROM lol_user
                           WHERE name='{0}')
        """.format(user_name))
        del self.inventories[user_name]
        print('inventory')

        self.cursor.execute("""
                    DELETE FROM user_champion
                    WHERE user_id=(SELECT user_id
                                   FROM lol_user
                                   WHERE name='{0}')
                """.format(user_name))
        del self.champions_owned[user_name]
        print('owned champs')

        self.cursor.execute("""
                            DELETE FROM user_skin
                            WHERE user_id=(SELECT user_id
                                           FROM lol_user
                                           WHERE name='{0}')
                        """.format(user_name))
        del self.skins_owned[user_name]
        print('owned skins')

        self.cursor.execute("""
            DELETE FROM lol_user
            WHERE user_id=(SELECT user_id
                                   FROM lol_user
                                   WHERE name='{0}')
                """.format(user_name))
        del self.users[user_name]
        print('user')

    def get_champ_name(self, skin_name):
        self.cursor.execute("""
        SELECT champion_name
        FROM champion
        WHERE champion_id=(SELECT champion_id
                           FROM skin
                           WHERE skin_name='{0}')
        """.format(skin_name))
        for name in self.cursor:
            return name[0]

    def commit(self):
        self.cursor.execute("""
            COMMIT
        """)
        print('Commit compiled')
