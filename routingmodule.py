__author__ = 'Allen'

import route
import Queue as Q


class RoutingModule:
    def __init__(self, node):
        ## route -> destination, firsthop, distance
        self.node = node
        self.routing_table = {self.node: route.Route(node, node, 0)}  # Key Node : Value nextHop Node
        self.link_state_cache = []  # cache of lsm ids
        # topology keeps a view of the entire network
        # use priority queue by distance
        self.topology = {}  # keyNode : (distance, destination)

    def distance(self, node):
        """
        :param node: the destination node
        :return: distance from self node to destination
        """
        return self.routing_table[node].distance

    def is_reachable(self, node):
        return node in self.routing_table.keys()

    def first_hop(self, destination_node):
        return self.routing_table[destination_node].firsthop

    def receive_message(self, ls_message):
        """
        :param ls_message: source, dest, distance,direction
        :return:
        """
        # if id(ls_message) in self.link_state_cache:
        #    return False
        self.link_state_cache.append(id(ls_message))
        # check if link state message is new or already cached
        # if link state message is "down" delete from topology
        # if cached do nothing and return
        # else we need to rebuild routing table
        # 1 . add to link state cache using source as key
        # 2 . build topology map

        source, dest, distance, direction = str(ls_message).split(" ")
        distance = float(distance)
        if direction == "down":
            # remove from topology
            i = 0
            for tuple in self.topology[source]:
                if tuple == (distance, dest):
                    del self.topology[source][i]
                    break
                i += 1

        elif source in self.topology.keys():
            if (distance, dest) in self.topology[source]:
                return
            self.topology[source].append((distance, dest))
        else:
            self.topology.setdefault(source, [])
            self.topology[source].append((distance, dest))
            # lsm(A,B,3.2,up) -> link_state_cache[ls_message.source]=(B,3.2)

            ### Topology has been updated - rebuild routing table
        self.dijkstra_paths()

    def clear_routing(self):
        self.routing_table.clear()
        self.routing_table = {self.node: route.Route(self.node, self.node, 0)}

    def is_neighbor(self, node):
        for tup in self.topology[self.node]:
            if node == tup[1]:
                return True
        return False

    def dijkstra_paths(self):

        # initialize by clearing out old routing table and adding self as confirmed route
        self.clear_routing()

        tentative = {}  # key dest : distance
        previous = {}
        ############################################################
        # Add all neighbors of source to tentative with dest as key#
        ############################################################
        if self.node not in self.topology.keys():
            return
        for node in self.topology[self.node]:
            tentative[node[1]] = node[0]
            previous[node[1]] = self.node
        ############################################################
        # Loop through the tentative list until there are none left#
        ############################################################

        while len(tentative) > 0:

            ########################################################
            # Get the node in tentative with the minimum distance  #
            # Then add to the routing table as confirmed           #
            ########################################################
            tmp = min(tentative, key=tentative.get)
            current_node = tmp
            distance = tentative[tmp]
            if previous[current_node] == self.node:
                nexthop = current_node
            else:
                nexthop = previous[current_node]
            tentative.pop(tmp)
            self.routing_table[current_node] = route.Route(current_node, nexthop, distance)
            # get new neighbors and distance
            if current_node in self.topology.keys():
                for node in self.topology[current_node]:

                    if node[1] in self.routing_table:
                        continue

                        # if self.is_neighbor((current_node)):
                        #   previous[node[1]] = current_node
                    if node[1] in tentative:
                        # need to update distance
                        current_distance = tentative[node[1]]
                        tentative[node[1]] = min(tentative[node[1]],
                                                 self.routing_table[current_node].distance + node[0])
                        if tentative[node[1]] != current_distance:
                            if previous[current_node] == self.node:
                                previous[node[1]] = current_node
                            else:
                                previous[node[1]] = previous[current_node]

                    else:
                        # node isnt in routing or tentative so add
                        tentative[node[1]] = node[0] + self.routing_table[current_node].distance
                        if previous[current_node] == self.node:
                            previous[node[1]] = current_node
                        else:
                            previous[node[1]] = previous[current_node]
