from datetime import datetime, date


class Devices:
    def __init__(self, requests):
        self.r = requests
        self.base_url = 'devices'

    def get(self, device_id):
        return self.r.get(self.r.build_url(self.base_url, device_id))

    def get_history(self, device_id, history_date):
        if isinstance(history_date, date) or isinstance(history_date, datetime):
            string_date = history_date.strftime('%Y-%m-%d')
        else:
            string_date = history_date

        return self.r.get(self.r.build_url(self.base_url, device_id, 'history', string_date))

    def get_all(self, pagination=False, pagination_token=None):
        query_params = {
            'pagination': 0 if pagination is False else 1
        }

        if pagination_token:
            query_params['pagination_token'] = pagination_token
            query_params['pagination'] = 1

        return self.r.get(self.base_url, params=query_params)

    def start_tracking(self, device_id):
        return self.r.post(self.r.build_url(self.base_url, device_id, 'start'))

    def stop_tracking(self, device_id):
        return self.r.post(self.r.build_url(self.base_url, device_id, 'stop'))

    def change_name(self, device_id, name):
        data = {
            'name': name
        }

        url = self.r.build_url(self.base_url, device_id)
        return self.r.patch(url, json=data)

    def patch_metadata(self, device_id, metadata):
        data = {
            'metadata': metadata
        }

        url = self.r.build_url(self.base_url, device_id)

        return self.r.patch(url, json=data)

    def delete(self, device_id):
        return self.r.delete(self.r.build_url(self.base_url, device_id))
