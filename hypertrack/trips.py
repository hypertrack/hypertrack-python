class Trips:
    def __init__(self, requests):
        self.r = requests
        self.base_url = 'trips'

    def create(self, trip_data):
        """
        Start a new trip for a device.

        :param trip_data: trip dict
        :return: trip dict
        """
        return self.r.post(self.base_url, json=trip_data)

    def complete(self, trip_id):
        """
        Complete an ongoing trip.
        The request will start the procedure and confirm a pending completion with a trips webhook.
        Until the completion is done, the trip will have the status `processing_completion`.

        :param trip_id:
        :return: None
        """
        return self.r.post(self.r.build_url(self.base_url, trip_id, 'complete'))

    def get(self, trip_id):
        """
        Get summary for a trip. Available for both ongoing and completed trips.

        :param trip_id: string trip ID
        :return: trip summary dict
        """
        return self.r.get(self.r.build_url(self.base_url, trip_id))

    def get_all(self, trip_status='completed', pagination_token=None):
        """
        Get all trips in your account. Returns ongoing trips by default.

        :param trip_status: string status active|completed|processing_completion
        :param pagination_token: string token received from previous call to request next page
        :return: dict {'data': [trips], 'links': {'pagination_token'...}}
        """
        query_params = {
            'status': trip_status
        }

        if pagination_token:
            query_params['pagination_token'] = pagination_token

        return self.r.get(self.base_url, params=query_params)

    def patch_geofence_metadata(self, trip_id, geofence_id, metadata):
        """
        Update geofence metadata for geofences in a trip. Available for both ongoing and completed trips.

        :param trip_id: string trip ID
        :param geofence_id: string geofence ID
        :param metadata: metadata dict

        :return: None
        """
        data = {
            'metadata': metadata
        }

        return self.r.patch(self.r.build_url(self.base_url, trip_id, 'geofence', geofence_id), json=data)

    def get_geofence(self, trip_id, geofence_id):
        """
        Get trip geofence

        :param trip_id: string trip ID
        :param geofence_id: string geofence ID

        :return: geofence dict
        """
        return self.r.get(self.r.build_url(self.base_url, trip_id, 'geofence', geofence_id))

    def create_geofences(self, trip_id, geofences):
        """
        Add more geofences to an ongoing trip, in addition to geofences you might have created when creating trip.

        :param trip_id: string trip ID
        :param geofences: list of geofences data

        :return: None
        """
        data = {
            'geofences': geofences
        }

        return self.r.patch(self.r.build_url(self.base_url, trip_id, 'geofence'), json=data)
