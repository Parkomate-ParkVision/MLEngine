from users.db import User
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_searchable_list = [User.email]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "User"
    name_plural = "Users"
    page_size = 10
    page_size_options = [10, 20, 50, 100]
