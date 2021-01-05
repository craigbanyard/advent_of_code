from time import time


def aoc_timer(func):
    def timer(*args, **kw):
        t0 = time()
        result = func(*args, **kw)
        t1 = time() - t0
        if 'get_input' in func.__name__:
            print("-----\nData:", t1)
        elif kw.get("time") is False:
            pass
        else:
            print("-----\nTime:", t1)
        return result
    return timer


@aoc_timer
def test(x):
    return sum(range(x))


def main():
    pass


if __name__=='__main__':
    main()
