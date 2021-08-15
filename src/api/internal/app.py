from ninja import NinjaAPI


def get_api():
    api = NinjaAPI(title='django-ninja-pet api', auth=[], version='1.0.0')
    admin_api = NinjaAPI(title='django-ninja-pet admin api', docs_url='docs', auth=[], version='admin 1.0.0')

    return api, admin_api


ninja_api, ninja_admin_api = get_api()
