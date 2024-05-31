from dataprovider import UserDataProvider

class LoginController:
    # implementimi i singleton pattern
    __login_controller = None
    
    # Create variable to store the logged in user
    __logged_in_user = None 
    
    @staticmethod
    def login_user(username, password):
        user_data_provider = UserDataProvider()
        user_list = user_data_provider.user_list
        for user in user_list:
            if user.username == username and user.password == password:
                # Login successfully as username and password are correct
                LoginController.get_instance().__logged_in_user = user
                
    @staticmethod
    def get_logged_in_user():
        return LoginController.get_instance().__logged_in_user
                
    @staticmethod
    def get_instance():
        if LoginController.__login_controller is None:
            LoginController.__login_controller = LoginController()
        return LoginController.__login_controller
    
    # metoda sherben ne qofte se useri klikon direkt ne log in pa shkruar username dhe pasword
    @staticmethod
    def is_string_none_or_blank(string):
        return string is None or string == ""
            
            