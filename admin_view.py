from dataprovider import DataProvider
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.datatables import MDDataTable
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from model import Restaurant, Menu_item, Menu, Table
from admin_controllers import RestaurantManagerController, RestaurantDatabaseManager, MenuManagerController, MenuItemManagerController, TableManagerController
from kivy.uix.popup import Popup
from kivy.core.window import Window
from enums import Item_Type

class RestaurantManagerContentPanel:
    def __init__(self):
    # Percakton qe gjendja fillestare e aplikacionit te mos jete e selektuar
        selected_row = -1
    
    restaurant_manager_controller = RestaurantManagerController()
    restaurant_database_manager = RestaurantDatabaseManager("internshippython", "postgres", "postgres123", "localhost", 5432)
    restaurant_list = restaurant_database_manager.get_restaurant_list()
    
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_restaurant_input_data_panel())
        split_layout_panel.add_widget(self._create_restaurant_management_panel())
        return split_layout_panel
    
    
    # Pamja e majt ku klienti shkruan te dhenat
    def _create_restaurant_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=10, spacing=10)
        input_data_component_panel.height = Window.height * 0.3
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = Window.width * 0.3
        
        
        
        #Restaurant Name Formatting
        #Multiline nese eshte True na ndihmon qe tekti te kete mundesi te kaloj ne rreshtin tjeter
        self.name_input = MDTextField(multiline=True, font_size='18sp', hint_text='Restaurant Name')
        input_data_component_panel.add_widget(self.name_input)
        #Restaurant Address Formatting
        self.address_input = MDTextField(multiline=False, font_size='18sp', hint_text='Restaurant Address')
        input_data_component_panel.add_widget(self.address_input)
        
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        
        return input_data_component_panel
    
    # pjesa e djathte - siperfaqja e dropdown dhe tabeles
    def _create_restaurant_management_panel(self):
        content_panel= GridLayout(cols=1, spacing=10)
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.add_widget(self.create_table())
        content_panel.size_hint_x = None
        content_panel.size_hint_y = None
        content_panel.width = Window.width * 0.7
        content_panel.height = Window.height * 0.7
        
        
        scroll_view = ScrollView()  
        scroll_view.add_widget(content_panel)  ###############1:26:43
    
        return scroll_view
        
        return content_panel
        
    def _create_buttons_component_panel(self):
        buttons_component_panel = GridLayout(rows=3, padding=10, spacing=20)
        
        add_button = Button(text='Add', size_hint=(None, None), size=(150, 40), background_color=(0,1,1,1))
        add_button.bind(on_release=self._add_restaurant)
        update_button = Button(text='Update', size_hint=(None, None), size=(150, 40), background_color=(0,1,1,1))
        update_button.bind(on_release=self._update_restaurant)
        delete_button = Button(text='Delete', size_hint=(None, None), size=(150, 40), background_color=(0,1,1,1))
        delete_button.bind(on_release=self._delete_restaurant)
        # Funksionaliteti i buttonave 
        add_button.bind(on_press= self._add_restaurant)
        update_button.bind(on_press= self._update_restaurant)
        delete_button.bind(on_press= self._delete_restaurant)
        # Pamja e buttonave
        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(update_button)
        buttons_component_panel.add_widget(delete_button)
        
        return buttons_component_panel
    
    def _create_table_panel(self):
        # Creates a panel to hold the table
        table_panel = GridLayout(cols=1, padding=10, spacing=0)
        # Creates the restaurant table
        self.restaurant_table = self.create_table
        # Adds the restaurant table to the table panel
        # Shtimi i funksioneve per check listat 
        self.restaurant_table.bind(on_check_press=self._checked)
        self.restaurant_table.bind(on_row_press=self._on_row_press)
        table_panel.add_widget(self.restaurant_table)
        return table_panel
    
    
        
    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(1, 0.1), background_color = (0,1,1,1))
        button.bind(on_release = self.show_restaurant_list)
        return button 
    
    def show_restaurant_list(self, button):        
        menu_items = []
        restaurant_list = self.restaurant_list
        #Create menu items for each restaurant in the restaurant list
        for restaurant in restaurant_list:
            menu_items.append({"viewclass": "OneLineListItem", 
                               "text": restaurant.name,
                               "on_release": lambda r=restaurant: self._update_data_table(r),
                               }
                            )
            
        self.dropdown = MDDropdownMenu(
            caller= button,
            items= menu_items,
            width_mult=5,
            max_height=dp(150),
            
        )
        self.dropdown.open()
        
        
    def create_table(self):
    
        
        table_row_data = []
        
        self.restaurant = self.restaurant_list[0]
        # Get the menus from the restaurant 
        restaurants = self.restaurant_list
           
        for restaurant in restaurants:
            table_row_data.append((restaurant.name, restaurant.address))
            
        self.restaurant_table = MDDataTable(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color_header="#7393B3",  # 7393B3
            background_color_cell="#F0FFFF",
            background_color_selected_cell="#ADD8E6",  # ADD8E6
            check=True,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("name", 150),
                ("Address", 150),
                
            ],
            row_data=table_row_data,
        )
        self.restaurant_table.bind(on_check_press = self._checked)
        self.restaurant_table.bind(on_row_press = self._on_row_press)
        return self.restaurant_table
    
    
    # funksionin checked na ndihmon me e specifiku rreshtin te cilin duam ta bejme add, update ose delete.
    
        
    def _checked(self,instance_table,current_row):
        selected_restaurant = Restaurant(
            current_row[0],current_row[1],[]
        )

        #Assign the employee's data to the input fields
        self.name_input.text = str(selected_restaurant.name)
        self.address_input.text=str(selected_restaurant.address)
 

    def _update_data_table(self, restaurant_list):
        self.restaurant_list = restaurant_list

        # Get restaurant data for the selected department
        table_row_data = []
        for restaurant in restaurant_list:
            table_row_data.append(
                (restaurant.name, restaurant.address)
            )

        # Update the restaurant table with the data
        self.restaurant_table.row_data = table_row_data

    def _on_row_press(self,instance,row):
        #Set the row index to delete when the row is pressed 
        self.selected_row = int (row.index / len(instance.column_data))
            
    def _add_restaurant(self, instance):
        # Get restaurant data form input fields 
        name = self.name_input.text
        address = self.address_input.text
        
        restaurant_data = []  
        restaurant_data.append(name)
        restaurant_data.append(address)
        
    # Ne momentin qe klikojme buttonin add te dhenat qe kemi specifikuar me kete kod fshihen ne input text field
    # dhe shtohen ne tabel
        if self._is_data_valid(restaurant_data):
            self.restaurant_manager_controller.add_restaurant(
               self.restaurant, restaurant_data
           )
            self.restaurant_table.row_data.append([name, address])
            # Fshin te dhenat ne input text fields sa her qe klikojme add
            self._clear_input_text_fields()
            # Nese te dhenat nuk jane te sakta
        else:
            # Ngritja e nje mesazhi
            popup = Popup(
                title="Invalid data",
                content= Label(text= "Provide manatory data to add a new Restaurant"),
                size_hint = (None, None),
                size=(400, 200),
            
            
            )
            popup.open
    
    
    def _update_restaurant(self, instance):
        if self.selected_row != -1:
            # Get the updated restaurant data from the input fieleds
            name = self.name_input.text
            address = self.address_input.text
            
            restaurant_data = []
            restaurant_data.append(name)
            restaurant_data.append(address) 
            
            if self._is_data_valid(restaurant_data):
                restaurant_to_remove = self.restaurant_table.row_data[self.selected_row]
                
                del self.restaurant_table.row_data[self.selected_row]
                self.restaurant_manager_controller.delete_restaurant(
                    self.restaurant, restaurant_to_remove
                )
                
                self.restaurant_manager_controller.add_restaurant(
                    self.restaurant, restaurant_data
                )
             
                self.restaurant_table.row_data.append([name, address])
                # Fshin te dhenat ne input text fields sa her qe klikojme update
                self._clear_input_text_fields()
                
            else:
                popup = Popup(
                    title="Invalid data",
                    content=Label(text="Provide mandatory data to update the Restaurant"),
                    size_hint=(None, None),
                    size=(400, 200)
                    
                )
                popup.open()
        else:
            popup=Popup(
                title="Invalid data",
                content=Label(text="Select any row to update"),
                size_hint=(None, None),
                size=(400, 200),
                
            )   
            popup.open()
            
    def _delete_restaurant(self, instance):
        if self.selected_row != -1:
            restaurant_to_remove = self.restaurant_table.row_data[self.selected_row]
            
            del self.restaurant_table.row_data[self.selected_row]
            self.restaurant_manager_controller.delete_restaurant(
                self.restaurant, restaurant_to_remove
            )
            
            self._clear_input_text_fields()
            
        else:
            popup = Popup(
                title="Invalid data",
                content=Label(text="Select any row to delete"),
                size_hint=(None, None),
                size=(400, 200),
                
            )
            popup.open()
            
    def _clear_input_text_fields(self):
        # Clear the input fields by setting their text to empty strings
        self.name_input.text = ""
        self.address_input.text = ""
        self.selected_row = -1
        
    def _is_data_valid(self, restaurant_data):
        # Check if restaurant data is valid (all fields are filled)
        return (
            restaurant_data[0] != ""
            and restaurant_data[1] != ""
        )             
        

    
    # Content Panel 2 - Menu Manager
class MenuManagerContentPanel():
    def __init__(self):
        
        self.menu_manager_controller = MenuManagerController()
        self.restaurant_list = DataProvider().restaurant_list
        self.restaurant = self.restaurant_list[0]
        self.restaurant_selector = None
        self.menu_selector = None
        self.selected_menu = None
        self.selected_row = -1
    
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_menu_manager_input_data_panel())
        split_layout_panel.add_widget(self._create_management_panel())
        return split_layout_panel
    
    def _create_menu_manager_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400
        
        self.menu_name_input = MDTextField( font_size = '18sp', hint_text ='Menu Name')
        input_data_component_panel.add_widget(self.menu_name_input)
        
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        
        return input_data_component_panel
        
        
    
    def _create_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.size_hint_x = None
        content_panel.width = 800
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.add_widget(self.create_table())
        
        return content_panel
    
    def _create_buttons_component_panel(self):
        button_component_panel = GridLayout(cols=3, padding=0, spacing = 10)
        add_button = Button(text='Add', size_hint=(None, None), size=(100, 40), background_color=(0,1,1,1))
        add_button.bind(on_release=self._add_menu)
        update_buton = Button(text='Update', size_hint=(None, None), size=(100, 40), background_color=(0,1,1,1))
        update_buton.bind(on_release=self._update_menu)
        delete_button = Button(text='Delete', size_hint=(None, None), size=(100, 40), background_color=(0,1,1,1))
        delete_button.bind(on_release=self._delete_menu)
        
        button_component_panel.add_widget(add_button)
        button_component_panel.add_widget(update_buton)
        button_component_panel.add_widget(delete_button)
        return button_component_panel
    
    # Restaurant selector
    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(1, 0.1), background_color = (0,1,1,1))
        button.bind(on_release = self.show_restaurant_list)
        return button 
    
    def show_restaurant_list(self, button):        
        menu_items = []
        restaurant_list = self.restaurant_list
        #Create menu items for each restaurant in the restaurant list
        for restaurant in restaurant_list:
            menu_items.append({"viewclass": "OneLineListItem", "text": restaurant.name})
            
        self.dropdown = MDDropdownMenu(
            caller= button,
            items= menu_items,
            width_mult=5,
            max_height=dp(150),
            
        )
        self.dropdown.open()


    def create_table(self, restaurant):
        table_row_data = []
        menu_list = restaurant.menu_list
        self.restaurant = self.restaurant_list[0]
        # Get the menus from the restaurant 
        menus = self.restaurant.menu_list
        # Get the task list from the first menu
        
        for menu in menus:
            table_row_data.append((menu.name,))
            
        self.menu_table = MDDataTable(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color_header="#7393B3",  # 7393B3
            background_color_cell="#F0FFFF",
            background_color_selected_cell="#ADD8E6",  # ADD8E6
            check=True,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Menu name", 150),
                
              
            ],
            row_data=table_row_data,
        )
        self.menu_table.bind(on_check_press = self._checked)
        self.menu_table.bind(on_row_press = self._on_row_press)
        return self.menu_table
    
    
    
    def _checked(self, instance_table, current_row):
        self.selected_menu = Menu(
            current_row[0], menu_items_list=[current_row[1]]
        
        )
    
    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index / len(instance.column_data))
        
    def _clear_input_text_fields(self):
        self.name_input_text = ""
        self.selected_row = -1
        
    def _is_data_valid(self, menu_data):
        return (
            menu_data[0] != ""
            and menu_data[1] != ""
        )
    
    def _add_menu(self, instance):
        name = self.menu_name_input.text
        menu_items_list = self._get_selected_menu_items_list()
        
        menu_data = [name, menu_items_list]
        
        if self._is_data_valid(menu_data):
            self.menu_manager_controller._add_menu(self.restaurant, menu_data)
            
            self.menu_table.row_data.append([name, menu_items_list.name])
            
            self._clear_input_text_fields()                
            
        else:
            self._show_error_popup("Invalid data", " Provide mandatory data to add a new Menu ")
            
    def _update_menu(self, instance):
        if self.selected_row != -1:
            name = self.menu_name_input.text
            menu_items_list = self._get_selected_menu_items_list()
            
            menu_data = [name, menu_items_list]
            
            if self._is_data_valid(menu_data):
                menu_to_remove = self.menu_table.row_data[self.selected_row]
                
                del self.menu_table.row_data[self.selected_row]
                self.menu_manager_controller._update_menu(menu_to_remove[0], menu_data, self.restaurant)
                
                self.menu_table.row_data.append([name, menu_items_list.name])
                
                self._clear_input_text_fields()
            else:
                self._show_error_popup("Invalid data", "Provide mandatory data to update the Menu")
                
        else:
            self._show_error_popup("Invalid data", "Selected any row to update")
            
            
    def _delete_menu(self, instance):
        if self.selected_row != -1:
            menu_to_remove = self.menu_table.row_data[self.selected_row]
            
            del self.menu_table.row_data[self.selected_row]
            self.menu_manager_controller._delete_menu(self.restaurant, menu_to_remove[0])
            
            self._clear_input_text_fields()
        else:
            self._show_error_popup("Invalid data", "Select any row to delete")
            
    def _show_Error_popup(self,title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.open()
        
    def update_menu_list(self, restaurant):
        self.restaurant = restaurant
        menu = []
        menus = restaurant.menu_list
        for menu in menus:
            menu.append({"viewclass": "OneLineListItem", "text": menu.name,
                               "on_release": lambda r=menu: self._update_menu_table(r)})
            
        self.show_menu_list(None)
        self.menu_selector.items = menu_items ###
        self.menu_selector.dissmiss()
        self._update_data_table(menu[0])
        
    def _update_data_table(self, menu):
        self.menu = menu
        table_row_data = []
        menu = menu.menu_list
        for menu in menu:
            table_row_data.append(
                ( menu.name)
            )
        self.menu_table.row_data = table_row_data
    
    
    # Content Panel 3 - Menu item manager
class MenuItemManagerContentPanel:
    def __init__(self):
        
        self.menu_item_manager_controller = MenuItemManagerController()
        self.restaurant_list = DataProvider().restaurant_list
        self.restaurant = self.restaurant_list[0]
        self.restaurant_selector = None
        self.menu_selector = None
        self.selected_menu_item = None
        self.selected_row = -1
        
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_menu_input_data_panel())
        split_layout_panel.add_widget(self._create_management_panel())
        return split_layout_panel
    
    def _create_menu_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400
        # ID 
        self.menu_item_id_input = MDTextField(font_size = "18sp", hint_text ="Menu item ID")
        input_data_component_panel.add_widget(self.menu_item_id_input)
        #Per MDDataTable nuk mundemi me i formatu me font_size dhe hint_text, keto behen vetem per MDTextField 
        
        # NAME
        self.menu_item_name_input = MDTextField( font_size = '18sp', hint_text ='Menu item Name')
        input_data_component_panel.add_widget(self.menu_item_name_input)
        
        # PRICE
        self.menu_item_price_input = MDTextField( font_size = '18sp', hint_text ='Menu item Price')
        input_data_component_panel.add_widget(self.menu_item_price_input)
        input_data_component_panel.add_widget(self.create_item_type_input_data_panel())
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        
        return input_data_component_panel
    
    def create_item_type_input_data_panel(self):
        self.item_type_input_panel = GridLayout(cols = 2, spacing = 20)
        self.item_type_input_panel.size_hint = (None, None)
        # Assuming there are two item types : Meal and Drink
        item_type_options = ["Meal", "Drink"]
        
        for item_type in item_type_options:
            checkbox = CheckBox(group='item_type', active = False, color=(0,0,0,1))
            checkbox_label = Label(text=item_type, color=(0,0,0,1))
            self.item_type_input_panel.add_widget(checkbox)
            self.item_type_input_panel.add_widget(checkbox_label)
        return self.item_type_input_panel
    
    def _get_selected_item_type(self):
        for index, child in enumerate(self.item_type_input_panel.children):
            if isinstance(child, CheckBox) and child.active:
                label_index = index - 1
                if label_index < len(self.item_type_input_panel.children):
                    label = self.item_type_input_panel.children[label_index]
                    item_type_text = label.text.lower()
                    return Item_Type[item_type_text.upper()]
                return None
            
    def _create_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.size_hint_x = None
        content_panel.width = 800
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.add_widget(self._create_menu_selector())
        content_panel.add_widget(self.create_table(self.restaurant_list[0].menu_list[0]))
        
        return content_panel
    
    
    
    def _create_buttons_component_panel(self):
        button_component_panel = GridLayout(cols=3, padding=0, spacing = 10)
        add_button = Button(text='Add', size_hint=(None, None), size=(100, 40), background_color=(0,1,1,1))
        add_button.bind(on_release=self._add_menu_item)
        update_buton = Button(text='Update', size_hint=(None, None), size=(100, 40), background_color=(0,1,1,1))
        update_buton.bind(on_release=self._update_menu_item)
        delete_button = Button(text='Delete', size_hint=(None, None), size=(100, 40), background_color=(0,1,1,1))
        delete_button.bind(on_release=self._delete_menu_item)
        
        button_component_panel.add_widget(add_button)
        button_component_panel.add_widget(update_buton)
        button_component_panel.add_widget(delete_button)
        return button_component_panel
    
    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(1, 0.1), background_color = (0,1,1,1))
        button.bind(on_release = self.show_restaurant_list)
        return button 
    
    def show_restaurant_list(self, button):
        menu_items = []
        restaurant_list = self.restaurant_list
        #Create menu items for each restaurant in the restaurant list
        for restaurant in restaurant_list:
            menu_items.append({"viewclass": "OneLineListItem", "text": restaurant.name,
                               "on_release": lambda restaurant=restaurant: self.update_menu_list(restaurant)})
            
        self.dropdown = MDDropdownMenu(
            caller= button,
            items= menu_items,
            width_mult=5,
            max_height=dp(150),
            
        )
        self.dropdown.open()
        
    def _create_menu_selector(self):
        button = Button(text='Select an menu', size_hint=(1, 0.1), background_color=(0,1,1,1))
        button.bind(on_release=self.show_menu_list)
        return button
    
    def show_menu_list(self, button):
        menu_items = []
        restaurant_list = self.restaurant_list
        menu_list = restaurant_list[0].menu_list
        
        for menu in menu_list:
            menu_items.append({"viewclass": "OneLineListItem", "text": menu.name,
                               "on_release": lambda m=menu: self._update_data_table(m)})
            
        self.dropdown = MDDropdownMenu(
            caller = button,
            items = menu_items,
            width_mult = 5,
            max_height=dp(150),
            
        )
        self.dropdown.open()
        
    def create_table(self, menu):
        table_row_data = []
        menu_item_list = menu.menu_item_list
        
        for menu_item in menu_item_list:
            table_row_data.append((menu_item.menu_item_id, menu_item.menu_item_name, menu_item.menu_item_price))
            
        self.menu_item_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check=True,
            use_pagination = True,
            rows_num=10,
            column_data=[
                ("Id", dp(40)),
                ("Name", dp(40)),
                ("price", dp(40)),
            ],
            row_data=table_row_data
        )
        self.menu_item_table.bind(on_check_press = self._checked)
        self.menu_item_table.bind(on_row_press = self._on_row_press)
        return self.menu_item_table
    # ADD HERE
    
    def _checked(self, instance_table, current_row):
        self.selected_menu_item = Menu_item(
            current_row[0], current_row[1], current_row[2], Item_Type[current_row[3]]
        
        )
        
        #id_input, name dhe price nuk jane te deklaruara te menu itemdata panel
        
        self.id_input.text = str(self.selected_menu_item.id)
        self.name_input.text = str(self.selected_menu_item.name)
        self.price_input.text = float(self.selected_menu_item.price)
        if self.selected_menu_item.item_type == Item_Type.MEAL:
            print("Meal")
            self.item_type_input_panel.children[1].active = True # Me 1 i jemi specifikuar Meal
        elif self.selected_menu_item.item_type == Item_Type.DRINK:
            self.item_type_input_panel.children[3].active = True # Me 2 i jemi specifikuar Drink
        
    
    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index / len(instance.column_data))
        
    def _clear_input_text_fields(self):
        self.id_input_text = ""
        self.name_input_text = ""
        self.selected_row = -1
        
    def _is_data_valid(self, menu_item_data):
        return (
            menu_item_data[0] != ""
            and menu_item_data[1] != ""
            and menu_item_data[2] != ""
            and menu_item_data[3] != ""
        )
    
    def _add_menu_item(self, instance):
        id = self.menu_item_id_input.text
        name = self.menu_item_price_input.text
        price = float(self.menu_item_price_input.text)
        item_type = self._get_selected_item_type()
        
        menu_item_data = [id, name, price, item_type]
        
        if self._is_data_valid(menu_item_data):
            self.menu_item_manager_controller._add_menu_item(self.menu, menu_item_data)
            
            self.menu_item_table.row_data.append([id, name, price, item_type.name])
            
            self._clear_input_text_fields()                
            
        else:
            self._show_error_popup("Invalid data", " Provide mandatory data to add a new Menu Item")
            
    def _update_menu_item(self, instance):
        if self.selected_row != -1:
            id = self.menu_item_id_input.text
            name = self.menu_item_name_input.text
            price = float(self.menu_item_price_input.text)
            item_type = self._get_selected_item_type()
            
            menu_item_data = [id, name, price, item_type]
            
            if self._is_data_valid(menu_item_data):
                menu_item_to_remove = self.menu_item_table.row_data[self.selected_row]
                
                del self.menu_item_table.row_data[self.selected_row]
                self.menu_item_manager_controller._update_menu_item(menu_item_to_remove[0], menu_item_data, self.menu)
                
                self.menu_item_table.row_data.append([id, name, price, item_type.name])
                
                self._clear_input_text_fields()
            else:
                self._show_error_popup("Invalid data", "Provide mandatory data to update the Menu item")
                
        else:
            self._show_error_popup("Invalid data", "Selected any row to update")
            
            
    def _delete_menu_item(self, instance):
        if self.selected_row != -1:
            menu_item_to_remove = self.menu_item_table.row_data[self.selected_row]
            
            del self.menu_item_table.row_data[self.selected_row]
            self.menu_item_manager_controller._delete_menu_item(self.menu, menu_item_to_remove[0])
            
            self._clear_input_text_fields()
        else:
            self._show_error_popup("Invalid data", "Select any row to delete")
            
    def _show_Error_popup(self,title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.open()
        
    def update_menu_list(self, restaurant):
        self.restaurant = restaurant
        menu_items = []
        menus = restaurant.menu_list
        for menu in menus:
            menu_items.append({"viewclass": "OneLineListItem", "text": menu.name,
                               "on_release": lambda m=menu: self._update_menu_item_table(m)})
            
        self.show_menu_list(None)
        self.menu_selector.items = menu_items
        self.menu_selector.dissmiss()
        self._update_data_table(menu[0])
        
    def _update_data_table(self, menu):
        self.menu = menu
        table_row_data = []
        menu_items = menu.menu_item_list
        for menu_item in menu_items:
            table_row_data.append(
                (menu_item.id, menu_item.name, menu_item.price, menu_item.item_type.value)
            )
        self.menu_item_table.row_data = table_row_data
        
# Content Panel 4 - Table Manager 
        
class TableManagerContentPanel():
    
    def __init__(self):
        
        self.restaurant_list = DataProvider().restaurant_list
        self.restaurant = self.restaurant_list[0]
        self.restaurant_selector = None
        self.menu_selector = None
        self.selected_menu_item = None
        self.selected_row = -1
        
        
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_menu_input_data_panel())
        split_layout_panel.add_widget(self._create_management_panel())
        return split_layout_panel
    
    
    def _create_menu_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400
        # Table ID 
        self.table_id_input = MDTextField(font_size = "18sp", hint_text ="Table ID")
        input_data_component_panel.add_widget(self.table_id_input)
        # Seats
        self.seats_input = MDTextField( font_size = '18sp', hint_text ='Seats')
        input_data_component_panel.add_widget(self.seats_input)
        
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        
        return input_data_component_panel
    
            
    def _create_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.size_hint_x = None
        content_panel.width = 800
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.add_widget(self.create_table(self.restaurant_list[0].table_list[0]))
        
        return content_panel
    
    def _create_buttons_component_panel(self):
        button_component_panel = GridLayout(cols=3, padding=0, spacing = 10)
        add_button = Button(text='Add', size_hint=(None, None), size=(100, 40), background_color=(0,1,1,1))
        add_button.bind(on_release=self._add_table)
        update_buton = Button(text='Update', size_hint=(None, None), size=(100, 40), background_color=(0,1,1,1))
        update_buton.bind(on_release=self._update_table)
        delete_button = Button(text='Delete', size_hint=(None, None), size=(100, 40), background_color=(0,1,1,1))
        delete_button.bind(on_release=self._delete_table)
        
        button_component_panel.add_widget(add_button)
        button_component_panel.add_widget(update_buton)
        button_component_panel.add_widget(delete_button)
        return button_component_panel
    
    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(1, 0.1), background_color = (0,1,1,1))
        button.bind(on_release = self.show_restaurant_list)
        return button 
    
    def show_restaurant_list(self, button):
        menu_items = []
        restaurant_list = self.restaurant_list
        #Create menu items for each restaurant in the restaurant list
        for restaurant in restaurant_list:
            menu_items.append({"viewclass": "OneLineListItem", "text": restaurant.name,
                               "on_release": lambda restaurant=restaurant: self.update_menu_list(restaurant)})
            
        self.dropdown = MDDropdownMenu(
            caller= button,   # Nuk e kam rregullu akoma table manager
            items= menu_items,
            width_mult=5,
            max_height=dp(150),
            
        )
        self.dropdown.open()
        
        
    def create_table(self, restaurant):
        table_row_data = []
        table_list = restaurant.table_list
        
        for table in table_list:
            table_row_data.append((table.id, table.seats))
            
        self.table_manager_table = MDDataTable(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color_header="#7393B3",  # 7393B3
            background_color_cell="#F0FFFF",
            background_color_selected_cell="#ADD8E6",  # ADD8E6
            check=True,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("ID", 150),
                ("Seats", 150),
                
              
            ],
            row_data=table_row_data,
        )
        
        self.table_manager_table.bind(on_check_press = self._checked)
        self.table_manager_table.bind(on_row_press = self._on_row_press)
        return self.table_manager_table
    
    def _checked(self, instance_table, current_row):
        self.selected_table = Table(
            current_row[0], current_row[1]
        
        )
        
        self.table_id_input.text = int(self.selected_table.id)
        self.seats_input.text = str(self.selected_table.seats)
        
    
    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index / len(instance.column_data))
        
    def _clear_input_text_fields(self):
        self.id_input_text = ""
        self.seats_input_text = ""
        self.selected_row = -1
        
    def _is_data_valid(self, table_data):
        return (
            table_data[0] != ""
            and table_data[1] != ""
        )
    
    def _add_table(self, instance):
        id = int(self.table_id_input.text)
        seats = self.seats_input.text
        
    
        
        table_manager_data = [id, seats]
        
        if self._is_data_valid(table_manager_data):
            self.table_manager_controller._add_table(self.menu, table_manager_data)# ketu mundet me qen nje gabim te menu
            
            self.table_table.row_data.append([id, seats])
            
            self._clear_input_text_fields()                
            
        else:
            self._show_error_popup("Invalid data", " Provide mandatory data to add a new Menu Item")
            
    def _update_table(self, instance):
        if self.selected_row != -1:
            id = int(self.table_id_input.text)
            seats = self.table_seats_input.text
            
            
            table_data = [id, seats]
            
            if self._is_data_valid(table_data):
                table_to_remove = self.table_table.row_data[self.selected_row]
                
                del self.table_table.row_data[self.selected_row]
                self.table_manager_controller._update_table(table_to_remove[0], table_data, self.restaurant)
                
                self.table_table.row_data.append([id, seats])
                
                self._clear_input_text_fields()
            else:
                self._show_error_popup("Invalid data", "Provide mandatory data to update the Menu item")
                
        else:
            self._show_error_popup("Invalid data", "Selected any row to update")
            
            
    def _delete_table(self, instance):
        if self.selected_row != -1:
            table_to_remove = self.table_table.row_data[self.selected_row]
            
            del self.table_table.row_data[self.selected_row]
            self.table_manager_controller._delete_table(self.restaurant, table_to_remove[0])
            
            self._clear_input_text_fields()
        else:
            self._show_error_popup("Invalid data", "Select any row to delete")
            
    def _show_Error_popup(self,title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.open()
        
    def update_table(self, restaurant):
        self.restaurant = restaurant
        tables = []
        restaurants = restaurant.table_list
        for restaurant in restaurants:
            tables.append({"viewclass": "OneLineListItem", "text": restaurant.name,
                               "on_release": lambda r=restaurant: self._update_table_table(r)})
            
        self.show_restaurant_list(None)
        self.restaurant_selector.items = tables
        self.restaurant_selector.dissmiss()
        self._update_data_table(restaurant[0])
        
    def _update_data_table(self, restaurant):
        self.restaurant = restaurant
        table_row_data = []
        tables = restaurant.table_list
        for table in tables:
            table_row_data.append(
                (table.id, table.seats)
            )
        self.table_table.row_data = table_row_data