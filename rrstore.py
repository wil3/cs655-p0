import simpy

class RRStore(simpy.Store):

    def _do_get(self, event):
        if self.items:
            event.succeed(self.items.pop())


def test_subclassed_store():
    """
    Test the subclassed store. Specifically, test that the gets work differently.
    """
    env = simpy.Environment()
    
    LogOrig = [] # keeps track of items returned by original store
    LogNew = [] # keeps track of items returned by new store

    def put(env, store, item):
        yield store.put(item)
        yield env.timeout(1)

    def get(env, store, log):
        item = yield store.get()
        log.append(item)
        yield env.timeout(1)
    
    StoreOrig = simpy.Store(env)
    StoreNew = RRStore(env)
##    assert StoreOrig.count == 0
##    assert StoreNew.count == 0
    item1 = 1
    item2 = 2
    env.process(put(env, StoreOrig, item1))
    env.process(put(env, StoreOrig, item2))
    env.process(put(env, StoreNew, item1))
    env.process(put(env, StoreNew, item2))
    env.process(get(env, StoreOrig, LogOrig))
    env.process(get(env, StoreOrig, LogOrig))
    env.process(get(env, StoreNew, LogNew))
    env.process(get(env, StoreNew, LogNew))
    env.run()
    [origitem1, origitem2] = LogOrig
    [newitem1, newitem2] = LogNew
    print "Original store yeilds items in this order: %s, %s" % (
        str(origitem1), str(origitem2))
    print "New store yeilds items in this order: %s, %s" % (
        str(newitem1), str(newitem2))
    assert origitem1 == newitem2
    assert origitem2 == newitem1

test_subclassed_store()
