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

    def render(self, loop, start_down, lead_in=None):
        if lead_in is None:
            lead_in = ()
        is_down = self._render(lead_in, start_down)
        for _ in range(self.require_length):  # i.e. while True
            is_down = self._render(loop, is_down)

    def _render(self, sequence, start_down):
        is_down = start_down
        for num_threads in sequence:
            for _ in range(num_threads):
                self.append(is_down)
            is_down = not is_down
        return is_down

    def append(self, is_down):
        if len(self.threads) >= self.require_length:
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

    print(a)
    print(b)

if __name__ == "__main__":
    main()
