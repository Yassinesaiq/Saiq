import unittest
from .utils import geocode_address

class TestGeocodeAddress(unittest.TestCase):

    def test_valid_address(self):
        # Test with a valid address
        address = "1600 Amphitheatre Parkway, Mountain View, CA"
        latitude, longitude = geocode_address(address)
        self.assertIsNotNone(latitude)
        self.assertIsNotNone(longitude)

    def test_invalid_address(self):
        # Test with an invalid address
        address = "This is not a valid address"
        latitude, longitude = geocode_address(address)
        self.assertIsNone(latitude)
        self.assertIsNone(longitude)

if __name__ == '__main__':
    unittest.main()
