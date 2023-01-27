class RowFullError(Exception):
    pass

class Row:
    def __init__(self, length, *args, **kwargs):
        self.threads = []
        self.require_length = length
        try:
            self.render(*args, **kwargs)
        except RowFullError:
            pass

    def render(self, loop, start_down, lead_in=None, lead_out=None):
        if lead_in is None:
            lead_in = ()
        if lead_out is None:
            lead_out = ()
        require_to_loop = sum(loop) if lead_out else 1

        is_down = self._render(lead_in, start_down)
        for _ in range(self.require_length):  # i.e. while True
            if self.num_unfilled < require_to_loop:
                break
            is_down = self._render(loop, is_down)
        is_down = self._render(lead_out, is_down)
        assert self.num_unfilled == 0

    def _render(self, sequence, start_down, allow_incomplete=True):
        is_down = start_down
        for num_threads in sequence:
            for _ in range(num_threads):
                self.append(is_down)
            is_down = not is_down
        return is_down

    @property
    def num_unfilled(self):
        return self.require_length - len(self.threads)

    def append(self, is_down):
        if self.num_unfilled <= 0:
            raise RowFullError
        self.threads.append(is_down)

    def __str__(self):
        return "".join(is_down and "X" or "•"
                       for is_down in reversed(self.threads))

def main():
    LENGTH = 37

    a = Row(LENGTH, start_down=True, loop=(2, 1, 2, 3))
    b = Row(LENGTH,
            start_down=False,
            lead_in=(1,),
            loop=(3, 2, 1, 2))
    c = Row(LENGTH,
            start_down=False,
            lead_in=(1, 2, 2, 3),
            loop=(2, 1, 2, 3),
            lead_out=(2, 2, 1))
    d = Row(LENGTH,
            start_down=True,
            lead_in=(2, 2, 2, 1),
            loop=(2, 3, 2, 1),
            lead_out=(2, 2, 2))
    e = Row(LENGTH,
            start_down=True,
            lead_in=(1, 2, 2),
            loop=(3, 2, 2, 1),
            lead_out=(2, 2, 2))
    f = Row(LENGTH,
            start_down=False,
            lead_in=(2, 2, 2),
            loop=(1, 2, 2, 3))
    g = Row(LENGTH,
            start_down=False,
            lead_in=(2, 2, 2, 1),
            loop=(3, 2, 2, 1),
            lead_out=(2, 2, 2))
    h = Row(LENGTH,
            start_down=True,
            loop=(1, 2, 2, 3),
            lead_out=(2, 2, 1))

    rows = (a, b, c, d, h, g, f, e, d, c, b, a)
    print("\n".join(map(str, rows)))

    cols = tuple(zip(*(row.threads for row in rows)))
    print("\n".join(("".join(is_down and "X" or "•"
                             for is_down in col))
                    for col in cols))

if __name__ == "__main__":
    main()
