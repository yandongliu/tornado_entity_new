from tornado import gen, ioloop

@gen.coroutine
def foo():
    a = yield bar()
    print a

@gen.coroutine
def bar():
    x = koo()
    raise gen.Return(x)

def koo():
    x = 1 + 3
    import my_pdb; my_pdb.set_trace()
    return x

if __name__ == '__main__':
    ioloop.IOLoop.current().run_sync(foo)
