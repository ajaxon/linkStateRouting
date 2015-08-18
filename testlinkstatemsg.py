__author__ = 'Allen'
import unittest
import linkstatemsg

class TestLinkStateMsg(unittest.TestCase):

    """Test of entity class LinkStateMsg, which represents a lsm
    """
    def test_constructor(self):
        lsm = linkstatemsg.LinkStateMsg("A", "B", 3.2, "up")
        self.assertTrue(lsm.direction == "up")
        self.assertTrue(lsm.source == "A")
        self.assertTrue(lsm.destination == "B")
        self.assertTrue(lsm.distance == 3.2)

if __name__ == '__main__':
    unittest.main()