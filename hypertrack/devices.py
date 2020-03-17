from datetime import datetime, date


class Devices:
    def __init__(self, requests):
        self.r = requests
        self.base_url = 'devices'

    def get(self, device_id):
        """
        Get live location and status of a device

        :param device_id: string device ID
        :return: device dict
        """
        return self.r.get(self.r.build_url(self.base_url, device_id))

    def get_history(self, device_id, history_date):
        """
        Get location history of device organized by activity and outage segment markers.

        :param device_id: string device ID
        :param history_date: string date in format YYYY-mm-dd or python date/datetime object
        :return: history dict
        """
        if isinstance(history_date, date) or isinstance(history_date, datetime):
            string_date = history_date.strftime('%Y-%m-%d')
        else:
            string_date = history_date

        return self.r.get(self.r.build_url(self.base_url, device_id, 'history', string_date))

    def get_account_history(self, history_date, response='blob', response_type='json', unit='km'):
        """
        Get data for all tracked devices for a specified day. Data is available for the the last 60 days.

        :param history_date: string date in format YYYY-mm-dd or python date/datetime object
        :param response: blob | file
        :param response_type: json | csv
        :param unit: km | mi

        :return: if response is blob:
        response object is a binary large object, has JSON format and returned in the response.

        If response is file:
        response object is a link to a temporary S3 bucket with JSON file and can be downloaded.
        """
        if isinstance(history_date, date) or isinstance(history_date, datetime):
            string_date = history_date.strftime('%Y-%m-%d')
        else:
            string_date = history_date

        params = {
            'response': response,
            'type': response_type,
            'unit': unit
        }

        return self.r.get(self.r.build_url(self.base_url, 'history', string_date), params=params)

    def get_all(self, pagination=False, pagination_token=None):
        """
        Get list of devices in your account (excludes deleted devices)

        :param pagination: bool flag to enable or disable pagination. False by default
        :param pagination_token: string token received from previous call to request next page
        :return: list of trips if pagination is False,
        object if pagination is True with next structure {'data': [devices], 'links': {'pagination_token'...}}
        """
        query_params = {
            'pagination': 0 if pagination is False else 1
        }

        if pagination_token:
            query_params['pagination_token'] = pagination_token
            query_params['pagination'] = 1

        return self.r.get(self.base_url, params=query_params)

    def start_tracking(self, device_id):
        """
        Start device tracking.

        :param device_id: string device ID
        :return: None
        """
        return self.r.post(self.r.build_url(self.base_url, device_id, 'start'))

    def stop_tracking(self, device_id):
        """
        Stop device tracking.

        :param device_id: string device ID
        :return: None
        """
        return self.r.post(self.r.build_url(self.base_url, device_id, 'stop'))

    def change_name(self, device_id, name):
        """
        Update device name

        :param device_id: string device ID
        :param name: new device name
        :return: None
        """
        data = {
            'name': name
        }

        url = self.r.build_url(self.base_url, device_id)
        return self.r.patch(url, json=data)

    def patch_metadata(self, device_id, metadata):
        """
        Update device metadata

        :param device_id: string device ID
        :param metadata: dict
        :return: None
        """
        data = {
            'metadata': metadata
        }

        url = self.r.build_url(self.base_url, device_id)

        return self.r.patch(url, json=data)

    def delete(self, device_id):
        """
        Delete a device. Once deleted, the device will not be able send location data again.
        Deleted devices cannot be undeleted.

        :param device_id: string device ID
        :return: None
        """
        return self.r.delete(self.r.build_url(self.base_url, device_id))
