class User:
    def __init__(self, username, password, user_role):
        self.username = username
        self.password = password
        self.user_role = user_role
        
    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, username):
        self.__username = username
        
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        self.__password = password
        
    @property
    def user_role(self):
        return self.__user_role
    
    @user_role.setter
    def user_role(self, user_role):
        self.__user_role = user_role

class Restaurant:
    def __init__(self, name, address, menu_list):
        self.__name = name
        self.__address = address
        self.menu_list = menu_list
        
    #annotations/decorators na ndihmojne qe pjesen e getters dhe setters ta bejme pak me automatike
    @property
    #Metoda get
    def name(self):
        return self.__name
    
    #Metoda set
    @name.setter
    #Vlera e atributit qe ne kete rast eshte name specifikohet me value
    def name(self, value):
        self.__name = value
    
    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, value):
        self.__address = value
        
    @property
    def menu_list(self):
        return self.__menu_list
    
    @menu_list.setter
    def menu_list(self, value):
        self.__menu_list = value
        
class Menu:
    def __init__(self, name, menu_items_list):
        self.__name = name
        self.__menu_items_list = menu_items_list
        
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def menu_items_list(self):
        return self.__menu_items_list
    
    @menu_items_list.setter
    def menu_items_list(self, value):
        self.__menu_items_list = value
        
class Menu_item:
    def __init__(self, menu_item_id, menu_item_name, menu_item_price, item_type):
        self .__menu_item_id = menu_item_id
        self .__menu_item_name = menu_item_name
        self .__menu_item_price = menu_item_price
        self .__item_type = item_type
        
    @property
    def menu_item_id(self):
        return self.__menu_item_id
    @menu_item_id.setter
    def menu_item_id(self, value):
        self.__menu_item_id = value
        
    @property
    def menu_item_name(self):
        return self.__menu_item_name
    @menu_item_name.setter
    def menu_item_name(self, value):
        self.__menu_item_name = value
        
    @property
    def menu_item_price(self):
        return self.__menu_item_price
    @menu_item_price.setter
    def menu_item_price(self, value):
        self.__menu_item_price = value
        
    @property
    def item_type(self):
        return self.__item_type
    @item_type.setter
    def item_type(self, value):
        self.__item_type = value
        
        
        
class Table:
    def __init__(self, id, seats):
        self .__id = id
        self .__seats = seats
        
        
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value
        
    @property
    def seats(self):
        return self.__seats
    @seats.setter
    def seats(self, value):
        self.__seats = value
        
   