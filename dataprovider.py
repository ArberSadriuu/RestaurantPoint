from model import Restaurant, Menu, Menu_item, User, Table
from enums import Item_Type, UserRole

class UserDataProvider:
    def __init__(self):
        self.__user_list = []
        self._create_user_list()
        
    def _create_user_list(self):  
        user1 = User("1", "1", UserRole.ADMIN)
        user2 = User("2", "2", UserRole.FINANCIAL_MANAGER)
        user3 = User("3", "3", UserRole.WAITER)
        user4 = User("4", "4", UserRole.WAITER)
        self.__user_list.append(user1)
        self.__user_list.append(user2)
        self.__user_list.append(user3)
        self.__user_list.append(user4)
            
    @property
    def user_list(self):
        return self.__user_list
        
        
class DataProvider:
    def __init__(self):
        # create the restaurants list 
        self.__restaurants = []
        self._create_restaurant_list()
        
    def _create_restaurant_list(self):
        # Create Menu for restaurant 1
        restaurant1_menu_list = self._create_restaurant1_menus()
        restaurant1 = Restaurant("Peshku", "Deshmoret e kombit", restaurant1_menu_list)
        
        # Create Menu for restaurant 2
        restaurant2_menu_list = self._create_restaurant2_menus()
        restaurant2 = Restaurant("Ariu", "Hasan Prishtina", restaurant2_menu_list)
        
        # Create Menu for restaurant 3
        restaurant3_menu_list = self._create_restaurant3_menus()
        restaurant3 = Restaurant("Hija e maleve", "12 Qershori", restaurant3_menu_list)
        
        # Menyra 1 e shtimit.Add restaurants to the list 
        self.__restaurants.append(restaurant1)
        self.__restaurants.append(restaurant2)
        self.__restaurants.append(restaurant3)
        
        #Menyra e 2 per krijimin e nje liste
    def _create_restaurant1_menus(self):
        menu_list = []
        menu_list.append(Menu("Res1 Menu1",  self.menu_items_for_menu1()))
        menu_list.append(Menu("Res1 Menu2",  self.menu_items_for_menu2()))
        menu_list.append(Menu("Res1 Menu3",  self.menu_items_for_menu3()))
        
        return menu_list
    
    def _create_restaurant2_menus(self):
        
        menu1 = Menu("Res2 Menu1",  self.menu_items_for_menu1())
        menu2 = Menu("Res2 Menu2",  self.menu_items_for_menu2())
        menu3 = Menu("Res2 Menu3",  self.menu_items_for_menu3())
        menu4 = Menu("Res2 Menu4",  self.menu_items_for_menu1())
        
        menu_list = [menu1, menu2, menu3, menu4]
        return menu_list 
    
    def _create_restaurant3_menus(self):
        menu1 = Menu("Res3 Menu1",  self.menu_items_for_menu1())
        menu2 = Menu("Res3 Menu2",  self.menu_items_for_menu2())
        menu3 = Menu("Res3 Menu3",  self.menu_items_for_menu3())
        menu4 = Menu("Res3 Menu4",  self.menu_items_for_menu3())
        
        menu_list = [menu1, menu2, menu3, menu4]
        return menu_list
    
    # Menyra e 3 
    def menu_items_for_menu1(self):
        menu_items = [ 
            Menu_item(1,"Burger", 2.0, Item_Type.MEAL),
            Menu_item(2,"Pizza", 8.00,  Item_Type.MEAL),
            Menu_item(3,"Sandwich", 1.5,  Item_Type.MEAL),
            Menu_item(4,"Eggs", 5.00,  Item_Type.MEAL)
        ]
        return menu_items
    
    
    def menu_items_for_menu2(self):
        menu_items = [ 
            Menu_item(1,"Finger Chicken", 4.0,  Item_Type.MEAL),
            Menu_item(2,"Chicken Wrap", 7.00,  Item_Type.MEAL),
            Menu_item(3,"Beef Burger", 4.5,  Item_Type.MEAL),
            Menu_item(4,"Eggless Truffle", 6.00, Item_Type.MEAL)
        ]
        return menu_items
    
    def menu_items_for_menu3(self):
        menu_items = [ 
            Menu_item(1,"AntiPasto Salad", 5.0, Item_Type.MEAL),
            Menu_item(2,"Chicken Salad", 7.5, Item_Type.MEAL),
            Menu_item(3,"Chicken Prame", 4.0, Item_Type.MEAL),
            Menu_item(4,"Chicken Grilled", 9.00, Item_Type.MEAL)
        ]
        return menu_items
    
    def table_for_restaurant1(self):
        table = [
            Table(1,"4 Seats"),
            Table(2,"3 Seats"),
            Table(3,"4 Seats"),
            Table(4,"2 Seats")
        ]
        return table
    
    def table_for_restaurant2(self):
        table = [
            Table(1,"3 Seats"),
            Table(2,"3 Seats"),
            Table(3,"2 Seats"),
            Table(4,"5 Seats")
        ]
        return table
    
    def table_for_restaurant3(self):
        table = [
            Table(1,"2 Seats"),
            Table(2,"5 Seats"),
            Table(3,"3 Seats"),
            Table(4,"3 Seats")
        ]
        return table
    
    # thirrja e te gjitha metodave permes restaurant
    @property
    def restaurant_list(self):
        return self.__restaurants