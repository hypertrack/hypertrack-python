from datetime import datetime, date


class Geofences:
    def __init__(self, requests):
        self.r = requests
        self.base_url = 'geofences'

    def get(self, geofence_id):
        """
        Get geofence

        :param geofence_id: string device ID
        :return: device dict
        """
        return self.r.get(self.r.build_url(self.base_url, geofence_id))


    def patch_metadata(self, geofence_id, metadata):
        """
        Update geofence metadata

        :param geofence_id: geofence ID string
        :param metadata: dict
        :return: None
        """
        data = {
            'metadata': metadata
        }

        url = self.r.build_url(self.base_url, geofence_id)

        return self.r.patch(url, json=data)

    def delete(self, geofence_id):
        """
        Delete a geofence.

        :param geofence_id: Geofence ID string
        :return: None
        """
        return self.r.delete(self.r.build_url(self.base_url, geofence_id))

    def create(self, geofences_data):
        """
        Create geofences for all your app users or for a single app user.

        :param geofences_data: geofences array of dictionaries
        :return: geofences created arary of dictionaries
        """
        return self.r.post(self.base_url, json=geofences_data)

