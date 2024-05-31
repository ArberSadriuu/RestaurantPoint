from model import Restaurant, Menu, Menu_item, Table
import psycopg2 # Me kete librari e bejme lidhjen e projektit me postgreSQL

class RestaurantManagerController:
    
    def add_restaurant(self, restaurant_data):
        # Step 1: Retrive the list of the restaurants
        restaurants = restaurant_list
        # Create a new Restaurant object with the provided data
        new_restaurant = Restaurant(restaurant_data[0], restaurant_data[1], [])
        # Add the new restaurant to the list of restaurant
        restaurants.append(new_restaurant)
        restaurant_list = restaurants
        
    def delete_restaurant(self, restaurant, restaurant_data):
        # Retrieve the restaurant list 
        restaurant_list = restaurant.restaurant_list
        
        # Iterate over the restaurant list to find the restaurant to be deleted
        for restaurant in restaurant_list:
            if restaurant.name == restaurant_data[0]:
                # Remove the restaurant from the restaurant list
                restaurant_list.remove(restaurant)
                

                
    def update_row(self, old_restaurant_data, new_restaurant_data, restaurant):
        restaurant_list = restaurant.restaurant_list
        
        for restaurant in restaurant_list:
            if restaurant.name == old_restaurant_data[0]:
                # Update the menu's data
                restaurant.name = new_restaurant_data[0]
                restaurant.address = new_restaurant_data[1]
                restaurant.menu_list = new_restaurant_data[2]   
                
                break
            
class RestaurantDatabaseManager:
    def __init__(self, dbname, user, password, host, port):
        # Lidhja me database
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()
        
        
    def create_table(self):
        # Creating restaurants table if it doesn't exist
                                        # ne kete tabel kemi vendos nga nje id te veqant per secilin restaurant qe te identifikohet me ate id, zgjatjen e emrit te restaurantit eshte 20 karaktere
        create_restaurant_table_query = "CREATE TABLE IF NOT EXISTS restaurants(id SERIAL PRIMARY KEY, name VARCHAR(20), address VARCHAR(30))"
        self.cursor.execute(create_restaurant_table_query) # ekzekutimi permes Pyetsorit
        self.conn.commit() # e bene ruajtjen e transaksioneve qe ndodhin ne data baze si ne Python(ctrl+s)
                                                                                                            # qels i huaj qe e ben lidhjen me nje tabel tjeter duke marr parasysh id e restauranteve
        create_menu_table_query = "CREATE TABLE IF NOT EXISTS menu (id SERIAL PRIMARY KEY, name VARCHAR(20), res_fk INT REFERENCES restaurants(id))"
        self.cursor.execute(create_menu_table_query)
        self.conn.commit()
        
        create_menu_item_table_query = "CREATE TABLE IF NOT EXISTS menu_item(id SERIAL PRIMARY KEY, name VARCHAR(25), price VARCHAR(8), men_fk INT REFERENCES menu(id))"
        self.cursor.execute(create_menu_item_table_query)
        self.conn.commit()
    
    # Funskioni per krijimin e nje restauranti brenda tabeles dmth shtimi i nje elementi te ri ne elementet e tjera te tabeles 
    def create_restaurant(self, restaurant_name):
        # SELECT - merret diqka nga data baza
        # Create - krijohet diqka ne data baz
        # WHERE - percakton nje kusht qe duhet plotesuar qe ne te krijojme nje transaktsion
        # INSERT - vendosim te dhena brenda ne data baz
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        res_result = self.cursor.fetchone() # me fetchone marrim vetem nje restaurant 
        
# Struktura e kontrollit shikon nëse një restaurant ekziston në bazën e të dhënave. Nëse po, printon një mesazh. Nëse nuk ekziston, shton emrin e restoranit në bazën e të dhënave
        if res_result:
            print("Restaurant already exists")
        else:
            query = f"INSERT INTO restaurants (name) VALUES ('{restaurant_name}')"
            self.cursor.execute(query)
            self.conn.commit()
            print("Restaurant created successfully")
            
    # Krijimi i elementeve(restauranteve) ne tersi brenda nje tabele
    def create_restaurants(self):
        self.create_restaurant("Peshku")
        self.create_restaurant("Ariu")
        self.create_restaurant("Hija e maleve")
        
    # Marrja e te dhenave tani nuk behet me nga dataprovider por nga databaza
    def get_restaurant_list(self):
        self.create_table()
        self.create_restaurants()
        sql = "SELECT * FROM restaurants"
        self.cursor.execute(sql)
        restaurants_names = self.cursor.fetchall() # fetchall i merr te gjitha restaurantet
        restaurant_list = []
        for row in restaurants_names:
            menu_list = self.get_data_from_table(row[1])
            restaurant_list.append(Restaurant(row[1], row[2], menu_list))
        return restaurant_list
    
# CREATE --> INSERT
# READ --> SELECT
# UPDATE --> UPDATE
# DELETE --> DELETE

    def insert_data_for_menu(self, restaurant, data):
        # Get restaurant ID by name using a parametrized query
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant.name}'"
        self.cursor.execute(sql)
        res_result = self.cursor.fetchone()
        if res_result:
            res_id = res_result[0]
            # Insert data into the menu table using a parametrized query
            query = f"INSERT INTO public.menu (name, res_fk) VALUES ('{data[0]}','{res_id}')"
            self.cursor.execute(query)
            self.conn.commit()
        else:
            print("Restaurant not found")
            
    def delete_data_for_menu(self, condition):
        # Delete data from the menu table based on a condition
        # Query eshte nje pyetsor i ri.
        query = f"DELETE FROM menu WHERE name = '{condition[0]}'"
        self.cursor.execute(query)
        self.conn.commit()
        
    def update_data_for_menu(self, restaurant_name, condition, data):
        sql_res = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql_res)
        res_result = self.cursor.fetchone()
        
        if res_result:
            res_id = res_result[0]
            
            query = f"UPDATE public.menu SET name = '{data[0]}', res_fk = {res_id} WHERE name='{condition[0]}'"
            self.cursor.execute(query)
            self.conn.commit()
        else:
            print("Restaurant not found!")
            
    def get_data_from_table(self, restaurant):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
   
        restaurant_id = result[0]
        sql = f"SELECT * FROM menu WHERE res_fk = '{restaurant_id}'"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        
        menu_list = []
        for row in data:
            menu_list.append(Menu(row[1], []))
        self.conn.commit()
        return menu_list
        
    
    
    
# For Menu
class MenuManagerController:
    
    def add_menu(self, restaurant, menu_data):
        menus = restaurant.menu_list
        
        new_menu = Menu(menu_data[0], menu_data[1], menu_data[2])
        menus.append(new_menu)
        restaurant.menu_list = menus
        
    def delete_menu(self, restaurant, menu_name):
        menu_list = restaurant.menu_list
        
        for menu in menu_list:
            if menu.name == menu_name:
                menu_list.remove(menu)
                restaurant.menu_list = menu_list
                break
            
    def update_menu(self, old_menu_name, new_menu_data, restaurant):
        menu_list = restaurant.menu_list
        
        for menu in menu_list:
            if menu.name == old_menu_name:
                menu.name = new_menu_data[0]
                menu.address = new_menu_data[1]
                menu.menu_items_list = new_menu_data[2]    
        
        
# For menu item
class MenuItemManagerController:
    
    def add_menu_item(self, menu, menu_data):
        menu_items = menu.menu_item_list
        
        new_menu = Menu_item(menu_data[0], menu_data[1], menu_data[2], menu_data[3])
        menu_items.append(new_menu)
        menu.menu_item_list = menu_items
        
    def delete_menu_item(self, menu, menu_item_name):
        menu_item_list = menu.menu_item_list
        
        for menu_item in menu_item_list:
            if menu_item.name == menu_item_name:
                menu_item_list.remove(menu_item)
                menu.menu_item_list = menu_item_list
                break
            
    def update_menu_item(self, old_menu_item_name, new_menu_item_data, menu):
        menu_item_list = menu.menu_item_list
        
        for menu_item in menu_item_list:
            if menu_item.name == old_menu_item_name:
                menu_item.id = new_menu_item_data[0]
                menu_item.name = new_menu_item_data[1]
                menu_item.price = new_menu_item_data[2]
                menu_item.item_type = new_menu_item_data[3]
                
                
# For TABLE
class TableManagerController:
    
    def add_table(self, restaurant, table_data):
        tables = restaurant.table_list
        
        new_table = Table(table_data[0], table_data[1])
        tables.append(new_table)
        restaurant.table_list = tables
        
    def delete_table(self, restaurant, table_id):
        table_list = restaurant.table_list
        
        for table in table_list:
            if table.id == table_id:
                table_list.remove(table)
                restaurant.table_list = table_list
                break
            
    def update_table(self, old_table_id, new_table_data, restaurant):
        table_list = restaurant.table_list
        
        for table in table_list:
            if table.id == old_table_id:
                table.id = new_table_data[0]
                table.seats = new_table_data[1]
                
                