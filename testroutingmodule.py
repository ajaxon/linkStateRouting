#
# CSCI 4760 -- unit test for link-state router
# Template provided by Dr Dan, completed by student
# 
import unittest
import route
import linkstatemsg
import routingmodule


class TestRoutingModule(unittest.TestCase):
    def test_setup(self):
        router = routingmodule.RoutingModule("A")
        self.assertTrue(router.is_reachable("A"))
        self.assertTrue(router.distance("A") == 0)
        self.assertFalse(router.is_reachable("B"))
        self.assertFalse(router.is_reachable("C"))

    def test_buildgraph(self):
        routers = [routingmodule.RoutingModule("A")]
        routers.append(routingmodule.RoutingModule("B"))
        routers.append(routingmodule.RoutingModule("C"))
        routers.append(routingmodule.RoutingModule("D"))
        routers.append(routingmodule.RoutingModule("E"))
        routers.append(routingmodule.RoutingModule("F"))
        routers.append(routingmodule.RoutingModule("G"))

        routing_messages =[]
        # partially fill in the routing table -- not in path order
        routing_messages.append(linkstatemsg.LinkStateMsg("A", "B", 3.2, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("B", "C", 0.8, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("C", "B", 0.8, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("B", "E", 1.5, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("E", "B", 1.5, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("E", "D", 4.1, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("D", "E", 4.1, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("E", "F", 1.4, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("F", "E", 1.4, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("C", "F", 7.7, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("C", "F", 7.7, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("F", "C", 7.7, "up"))
        routing_messages.append(linkstatemsg.LinkStateMsg("F", "G", 3.2, "up"))

        routing_messages.append(linkstatemsg.LinkStateMsg("B", "A", 3.2, "up"))
        for message in routing_messages:
            for router in routers:
                router.receive_message(message)

        router = routers[0]
        self.assertTrue(router.is_neighbor("B"))

        #verify partial graph
        self.assertTrue(router.distance("B") == 3.2)
        self.assertTrue(router.is_reachable("D"))
        self.assertTrue(router.distance("D") == 8.8)
        self.assertTrue(router.is_reachable("B"))
        self.assertTrue(router.first_hop("B") == "B")

        self.assertTrue(router.is_reachable("F"))
        self.assertTrue(router.distance("F") ==  6.1)
        self.assertTrue(router.distance("D") == 8.8)


        # First hops Node A
        self.assertTrue(router.first_hop("C") == "B")
        self.assertTrue(router.first_hop("D") == "B")
        self.assertTrue(router.first_hop("E") == "B")
        self.assertTrue(router.first_hop("F") == "B")
        self.assertTrue(router.first_hop("G") == "B")
        # Distances Node A
        self.assertTrue(router.distance("B") == 3.2)
        self.assertTrue(router.distance("C") == 4.0)
        self.assertTrue(router.distance("D") == 8.8)
        self.assertTrue(router.distance("E") == 4.7)
        self.assertTrue(router.distance("F") == 6.1)
        self.assertTrue(router.distance("G") == 9.3)

        #TODO: complete assertions for remaining 6 nodes

        router = routers[1]
        # First hops Node B
        self.assertTrue(router.first_hop("A") == "A")
        self.assertTrue(router.first_hop("C") == "C")
        self.assertTrue(router.first_hop("D") == "E")
        self.assertTrue(router.first_hop("E") == "E")
        self.assertTrue(router.first_hop("F") == "E")
        self.assertTrue(router.first_hop("G") == "E")
         # Distances Node B
        self.assertTrue(router.distance("A") == 3.2)
        self.assertTrue(router.distance("C") == 0.8)
        self.assertTrue(router.distance("D") == 5.6)
        self.assertTrue(router.distance("E") == 1.5)
        self.assertTrue(router.distance("F") == 2.9)
        self.assertTrue(router.distance("G") == 6.1)
        # Node C
        router = routers[2]
                # First hops Node C
        self.assertTrue(router.first_hop("A") == "B")
        self.assertTrue(router.first_hop("B") == "B")
        self.assertTrue(router.first_hop("D") == "B")
        self.assertTrue(router.first_hop("E") == "B")
        self.assertTrue(router.first_hop("F") == "B")
        self.assertTrue(router.first_hop("G") == "B")
         # Distances Node C
        self.assertTrue(router.distance("A") == 4.0)
        self.assertTrue(router.distance("B") == 0.8)
        self.assertAlmostEqual(6.4, router.distance("D"), places=7, msg=None, delta=None)
        self.assertAlmostEqual(2.3, router.distance("E"), places=7, msg=None, delta=None)
        self.assertAlmostEqual(3.7, router.distance("F"), places=7, msg=None, delta=None)
        self.assertAlmostEqual(6.9, router.distance("G"), places=7, msg=None, delta=None)

        # E
        router = routers[4]

        self.assertTrue(router.first_hop("A") == "B")
        self.assertTrue(router.first_hop("B") == "B")
        self.assertTrue(router.first_hop("D") == "D")
        self.assertTrue(router.first_hop("C") == "B")
        self.assertTrue(router.first_hop("E") == "E")
        self.assertTrue(router.first_hop("F") == "F")
        self.assertTrue(router.first_hop("G") == "F")

        self.assertAlmostEqual(4.7, router.distance("A"), places=7, msg=None, delta=None)
        self.assertAlmostEqual(1.5, router.distance("B"), places=7, msg=None, delta=None)
        self.assertAlmostEqual(4.1, router.distance("D"), places=7, msg=None, delta=None)
        self.assertAlmostEqual(0.0, router.distance("E"), places=7, msg=None, delta=None)
        self.assertAlmostEqual(1.4, router.distance("F"), places=7, msg=None, delta=None)
        self.assertAlmostEqual(4.6, router.distance("G"), places=7, msg=None, delta=None)
        self.assertAlmostEqual(2.3, router.distance("C"), places=7, msg=None, delta=None)

        router.receive_message(linkstatemsg.LinkStateMsg("E", "D", 4.1, "down"))

        self.assertFalse(router.is_reachable("D"))
        router.receive_message(linkstatemsg.LinkStateMsg("E", "D", 4.1, "up"))
        self.assertTrue(router.is_reachable("D"))
        router.receive_message(linkstatemsg.LinkStateMsg("E", "F", 1.4, "down"))
        self.assertTrue(router.is_reachable("F"))
        self.assertAlmostEqual(10.0, router.distance("F"), places=7, msg=None)
if __name__ == '__main__':
    unittest.main()

