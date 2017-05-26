from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    # 像在models里面一样，给这个app起一个别名，用于方便显示
    verbose_name = '用户信息'
