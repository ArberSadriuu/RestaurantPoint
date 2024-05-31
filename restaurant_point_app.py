from dataprovider import DataProvider

class RestaurantPointApp:
    def start(self):
        
        self.restaurant_list = []
        self.data_provider = DataProvider()
        self.restaurant_list = self.data_provider.restaurant_list
        
    # Loop through each restaurant
        for restaurant in self.restaurant_list:
            print("============================")
            print("List of menus in the " + restaurant.name + " restaurant" + " in " + restaurant.address + ":")
            print("============================")
            
            #Loop throught each menu in the restaurant
            for menu in restaurant.menu_list:
                print(menu.name + " me ID: " + str(menu.menu_id)) 
                print("-----------------------------")
                
                for menu_item in menu.menu_items_list:
                    # Print menu item name, price and description
                    print(str(menu_item.menu_item_id) + ", " + menu_item.menu_item_name + ", " + str(menu_item.menu_item_price)  +  ", " + menu_item.item_type.value)
                    print("------------------------------------")
                    
# Create an instance of the application and start it
restaurant_point_app = RestaurantPointApp()
restaurant_point_app.start()