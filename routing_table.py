#!/usr/bin/python3
from routing import *
from crypto import md5_hash

class RoutingTable:
    def __init__(self, table={}):
        self.table = table

    def __bytes__(self):
        result = bytes(0)
        for key, value in self.table.items():
            result = result + key + bytes([value]) 
        return result

    @staticmethod
    def parse(data):
        if len(data) % 17 != 0:
            raise ValueError('Incorrect size of routing table! (' + str(len(data)) + ')')

        result = RoutingTable()
        i = 0
        while i < len(data):
            result.table[data[i : i+16]] = data[i+16]
            i += 17
        return result

    # Updates the table for the router
    # @param: Router router
    # @param: tuple sender (string (md5hash), string(ipv4-address))
    def update_router(self, router, sender):
        update_table = []
        for i in self.table.keys():
            update_table.append((i, None, False, self.table[i]))

        router.update(sender, update_table)

    # Creates a RoutingTable table from a Router
    # @param: Router router
    def data_from_router(self, router):
        self.table = router.table



def testcase():
    rt = RoutingTable()
    me = md5_hash("max@mustermann.name")
    n1 = md5_hash("node1")
    n2 = md5_hash("node2")
    n3 = md5_hash("node3")
    n4 = md5_hash("node4")
    n5 = md5_hash("node5")
    r = Router(me, [(n1, "1.1.1.1"), (n2, "2.2.2.2")])

    # update from neighbor
    r.update((n1, "1.1.1.1"), [(n3, "3.3.3.3", False, 1), (n4, "4.4.4.4", False, 2)])

    # test getting data from router object
    rt.data_from_router(r)
    for key, val in rt.table.items():
        print(key, val)
    rt_bytes = rt.__bytes__()

    # update router object from routingtable
    rt_test = RoutingTable()
    rt_test.parse(rt_bytes)
    r_test = Router(me, [(n1, "1.1.1.1"), (n2, "2.2.2.2")])
    rt_test.update_router(r_test, (n5, "5.5.5.5"))
    print("\n" + "Update from " + str(n5))
    for key, val in r_test.table.items():
        print(key, val)

    # see if get_next_hop gives the right answer
    assert r_test.get_next_hop(n3) == (n5, "5.5.5.5")
    assert r_test.get_next_hop(n1) == (n1, "1.1.1.1")
    assert r_test.get_next_hop(n5) == (n5, "5.5.5.5")

    # full test
    r_me = Router(me, [(n1, "1.1.1.1"), (n2, "2.2.2.2")])
    r_me.update((n1, "1.1.1.1"), [(n3, "3.3.3.3", False, 1), (n4, "4.4.4.4", False, 1)])
    r_test = Router(me, [(n1, "1.1.1.1"), (n2, "2.2.2.2")])
    r_test_update = Router(me, [(n1, "1.1.1.1"), (n2, "2.2.2.2")])
    r_n1 = Router(n1, [(n3, "3.3.3.3"), (n4, "4.4.4.4")])
    rt_me = RoutingTable()
    rt_me.data_from_router(r_me)
    bytes_me = rt_me.__bytes__()

    rt_n1 = RoutingTable()
    rt_n1.data_from_router(r_n1)
    bytes_n1 = rt_n1.__bytes__()

    rt_test = RoutingTable()
    rt_test.data_from_router(r_test)
    rt_test.parse(bytes_n1)

    rt_test_update = RoutingTable()
    rt_test_update.parse(bytes_n1)
    rt_test_update.update_router(r_test_update, (n1, "1.1.1.1"))
    rt_test_update.data_from_router(r_test_update)
    bytes_test_update = rt_test_update.__bytes__()

    print("\n")
    for key, val in rt_me.table.items():
        print(key, val)
    print("\n")
    for key, val in rt_test_update.table.items():
        print(key, val)

    assert bytes_me == bytes_test_update


#testcase()
