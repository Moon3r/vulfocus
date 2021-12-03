from django.conf.urls import url
from frp.views import get_config, set_config, delete_frp


frpconfigs = [
    url(r'frp/get', get_config),
    url(r'frp/update', set_config),
    url(r'frp/delete', delete_frp),
]
