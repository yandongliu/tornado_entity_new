from handlers.error import ErrorHandler

development_settings = {
    # 'database.url': 'postgresql://tornado_application_user:qwerty123!@localhost:5432/tornado_application',
    'database': {
        'url': 'mysql://tornado_user:qwerty123!@localhost:3306/tornado_app',
    },
    'tornado': {
        'debug': True,
        'template_path': 'templates/',
        'default_handler_class': ErrorHandler,
    }
}

_obj = development_settings


def load():
    pass


def get(key):
    return _obj.get(key)
