import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'manifest'))
from validate_manifest import validate

class TestManifest(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate()['manifest_version'], '1.2.0')

if __name__ == '__main__':
    unittest.main()
