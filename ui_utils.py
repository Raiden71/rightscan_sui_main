import json
from typing import Callable
from functools import wraps

from java import jclass

noClass = jclass("ru.travelfood.simple_ui.NoSQL")
rs_settings = noClass("rs_settings")


# Класс-декоратор для удобной работы с hashMap. Также можно добавить дополнительную логику.
class HashMap:
    def __init__(self, debug: bool = False):
        self.hash_map = None
        self.debug_mode = debug

    def __call__(self, func: Callable[..., None]):
        @wraps(func)
        def wrapper(hashMap, *args, **kwargs):
            self.init(hashMap)
            func(self)
            return hashMap

        return wrapper

    def init(self, hashMap):
        self.hash_map = hashMap

    def toast(self, text, add_to_log=False):
        self.hash_map.put('toast', str(text))
        if add_to_log:
            self.error_log(text)

    def debug(self, text):
        if self.debug_mode:
            self.toast(text, add_to_log=True)

    def refresh_screen(self):
        self.hash_map.put('RefreshScreen', '')

    def run_event(self, method_name):
        self['RunEvent'] = json.dumps(self._get_event(method_name))

    def run_event_async(self, method_name):
        self['RunEvent'] = json.dumps(self._get_event(method_name, True))

    def _get_event(self, method_name, async_action=False):
        evt = [{
            'action': 'runasync' if async_action else 'run',
            'type': 'python',
            'method': method_name,
        }]
        return evt

    def error_log(self, err_data):
        try:
            err_data = json.dumps(err_data, ensure_ascii=False, indent=2)
        except:
            err_data = str(err_data)

        rs_settings.put('error_log', err_data, True)

    def __getitem__(self, item):
        return self.hash_map.get(item)

    def __setitem__(self, key, value):
        self.put(key, value)

    def get(self, item, from_json=False):
        if from_json:
            return json.loads(self.hash_map.get(item)) if self.hash_map.get(item) else None
        else:
            return self.hash_map.get(item)

    def put(self, key, value, to_json=False):
        if to_json:
            self.hash_map.put(key, json.dumps(value))
        else:
            self.hash_map.put(key, str(value))
