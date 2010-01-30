import unittest

import stubs


class TestStubs(unittest.TestCase):
  def test_stubs(self):
    self.assertTrue(stubs.all())


if __name__ == "__main__":
  unittest.main()
