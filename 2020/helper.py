from time import perf_counter


def aoc_timer(func):
    def timer(*args, **kw):
        t0 = perf_counter()
        result = func(*args, **kw)
        t1 = perf_counter() - t0
        if 'get_input' in func.__name__:
            print("-----\nData:", t1)
        elif kw.get("time") is False:
            pass
        else:
            print("-----\nTime:", t1)
        return result
    return timer


def main():
    pass


if __name__=='__main__':
    main()
