class Trips:
    def __init__(self, requests):
        self.r = requests
        self.base_url = 'trips'

    def create(self, trip_data):
        return self.r.post(self.base_url, json=trip_data)

    def complete(self, trip_id):
        return self.r.post(self.r.build_url(self.base_url, trip_id, 'complete'))

    def get(self, trip_id):
        return self.r.get(self.r.build_url(self.base_url, trip_id))

    def get_all(self, trip_status='completed', pagination_token=None):
        query_params = {
            'status': trip_status
        }

        if pagination_token:
            query_params['pagination_token'] = pagination_token

        return self.r.get(self.base_url, params=query_params)

    def patch_geofence_metadata(self, trip_id, geofence_id, metadata):
        data = {
            'metadata': metadata
        }

        return self.r.patch(self.r.build_url(self.base_url, trip_id, 'geofence', geofence_id), json=data)

    def get_geofence(self, trip_id, geofence_id):
        return self.r.get(self.r.build_url(self.base_url, trip_id, 'geofence', geofence_id))
