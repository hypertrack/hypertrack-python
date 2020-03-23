import os
import unittest
from hypertrack.rest import Client
from hypertrack.exceptions import HyperTrackException

DEVICE_ID = os.getenv("HT_EXISTING_DEVICE_ID")
ACCOUNT_ID = os.getenv("HT_ACCOUNT_ID")
SECRET_KEY = os.getenv("HT_SECRET_KEY")

hypertrack = Client(ACCOUNT_ID, SECRET_KEY)


class TestDevicesAPI(unittest.TestCase):

    def test_get_device(self):
        device = hypertrack.devices.get(DEVICE_ID)
        self.assertTrue('device_id' in device)
        self.assertTrue(isinstance(device, dict))

    def test_not_existing_device(self):
        try:
            hypertrack.devices.get('AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA')
            # Should not go to the next line
            print("Devices API did not throw exception.")
            self.assertTrue(False)
        except HyperTrackException as e:
            self.assertEqual(e.status, 404)

    def test_get_all_device(self):
        devices = hypertrack.devices.get_all()
        self.assertTrue(isinstance(devices, list))

    def test_start_tracking(self):
        response = hypertrack.devices.start_tracking(DEVICE_ID)
        self.assertTrue(response is None)

    def test_stop_tracking(self):
        response = hypertrack.devices.stop_tracking(DEVICE_ID)
        self.assertTrue(response is None)

    def test_change_name(self):
        device = hypertrack.devices.get(DEVICE_ID)
        # Save initial device name
        old_name = device['device_info']['name']
        response = hypertrack.devices.change_name(DEVICE_ID, 'Test Name')
        self.assertTrue(response is None)
        device = hypertrack.devices.get(DEVICE_ID)
        self.assertEqual(device['device_info']['name'], 'Test Name')
        # Change name back
        response = hypertrack.devices.change_name(DEVICE_ID, old_name)
        self.assertTrue(response is None)
        # Check that name was changed back
        device = hypertrack.devices.get(DEVICE_ID)
        self.assertEqual(device['device_info']['name'], old_name)


class TestTripsAPI(unittest.TestCase):
    def test_get_create_complete_trip(self):
        # Create trip
        trip = hypertrack.trips.create({
            'device_id': DEVICE_ID,
            'geofences': [{
              "geometry": {
                "type": "Point",
                "coordinates": [
                  35.105761016637075,
                  47.856801319070776
                ]
              },
              "radius": 65,
              "metadata": {"id": "dec43d3c-766c-4f6a-bd78-dfe873556782"}
            }, {
              "geometry": {
                "type": "Point",
                "coordinates": [
                  35.10460766676067,
                  47.85663214471151
                ]
              },
              "radius": 55,
              "metadata": {"id": "f2e56252-53e3-4194-8d53-d946716618e7"}
            }]
        })
        self.assertEqual(trip['status'], 'active')
        self.assertEqual(len(trip['geofences']), 2)

        # Get trip geofences
        geofence_id = trip['geofences'][0]['geofence_id']
        geofence = hypertrack.trips.get_geofence(trip['trip_id'], geofence_id)
        self.assertEqual(geofence['radius'], 65)
        self.assertEqual(geofence['metadata']['id'], 'dec43d3c-766c-4f6a-bd78-dfe873556782')

        # Change geofence metadata
        hypertrack.trips.patch_geofence_metadata(trip['trip_id'], geofence_id, {'id': '123'})
        geofence = hypertrack.trips.get_geofence(trip['trip_id'], geofence_id)
        self.assertEqual(geofence['metadata']['id'], '123')

        # Complete Trip
        hypertrack.trips.complete(trip['trip_id'])

        # Get Trip
        get_trip = hypertrack.trips.get(trip['trip_id'])
        self.assertTrue(get_trip['status'] in ['completed', 'processing_completion'])

    def test_get_all_trips(self):
        trips = hypertrack.trips.get_all()
        self.assertTrue(isinstance(trips, dict))
        self.assertTrue('data' in trips)


if __name__ == '__main__':
    unittest.main()
