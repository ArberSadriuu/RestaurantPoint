from enums import UserRole, UserFeatures
from admin_view import RestaurantManagerContentPanel, MenuManagerContentPanel, MenuItemManagerContentPanel, TableManagerContentPanel

class AuthorizationService:
    # Class responsible for providing user features based on user role
    
    def get_user_feature_by_user_role(self, user_role):
        
        #Returns the list of user features based on the user's role
        if user_role == UserRole.ADMIN:
            return [UserFeatures.RESTAURANT_MANAGER, UserFeatures.MENU_MANAGER, UserFeatures.MENU_ITEM_MANAGER, UserFeatures.TABLE_MANAGEMENT, UserFeatures.SIGN_OUT]
        elif user_role == UserRole.FINANCIAL_MANAGER:
            return [UserFeatures.FINANCIAL_REPORTS, UserFeatures.EXPENSE_TRACKING, UserFeatures.PAYROLLS, UserFeatures.ACCOUNTS, UserFeatures.SIGN_OUT]
        elif user_role == UserRole.WAITER:
            return [UserFeatures.TAKE_ORDERS, UserFeatures.TABLE_MANAGEMENT, UserFeatures.CUSTOMER_SERVICE, UserFeatures.BILLING, UserFeatures.SIGN_OUT]
        elif user_role is None:
            raise RuntimeError("The provided user role " + user_role + " is not supported")
        
        
class UserFeatureLabelResolver:
    # Class responsible for resolving user feature labels
    user_feature_label_dict = None
    
    @staticmethod
    def get_user_feature_label(user_feature):
        return UserFeatureLabelResolver.__get_user_feature_label_dict().get(user_feature)
        
    
    @staticmethod
    def __get_user_feature_label_dict():
        if UserFeatureLabelResolver.user_feature_label_dict is None:
            UserFeatureLabelResolver.user_feature_label_dict = {
                UserFeatures.RESTAURANT_MANAGER : "Restaurant Manager",
                UserFeatures.MENU_MANAGER : "Menu Manager",              
                UserFeatures.MENU_ITEM_MANAGER : "Menu Item Manager",
                UserFeatures.TABLE_MANAGEMENT : "Table management",
                UserFeatures.EMPLOYEES : "Employees",
                UserFeatures.FINANCIAL_REPORTS : "Financial reports",
                UserFeatures.EXPENSE_TRACKING : "Expense Tracking",
                UserFeatures.PAYROLLS : "Payrolls",
                UserFeatures.ACCOUNTS : "Accounts",
                UserFeatures.TAKE_ORDERS : "Take orders",
                UserFeatures.CUSTOMER_SERVICE : "Customer service",
                UserFeatures.BILLING : "Billing",
                UserFeatures.SIGN_OUT : "Sign out",
                
            }      
        return UserFeatureLabelResolver.user_feature_label_dict
    
    
    # Nderlidhja e pamjeve te aplikacionit behet permes kesaj classe
    # This class connects to the view file
class UserFeatureContentPanelResolver:
    user_feature_content_panel_map = None
    
    @staticmethod
    def get_user_feature_panel(user_feature):
        return UserFeatureContentPanelResolver.get_user_feature_content_panel_map().get(user_feature)
    @staticmethod
    def get_user_feature_content_panel_map():
        if UserFeatureContentPanelResolver.user_feature_content_panel_map is None:
            UserFeatureContentPanelResolver.user_feature_content_panel_map = {
                "Restaurant Manager": RestaurantManagerContentPanel(),
                "Menu Manager": MenuManagerContentPanel(),
                "Menu Item Manager": MenuItemManagerContentPanel(),
                "Table management" : TableManagerContentPanel(),
                
            }
            
        return UserFeatureContentPanelResolver.user_feature_content_panel_map
    
