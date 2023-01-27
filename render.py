class RowFullError(Exception):
    pass

class Row:
    def __init__(self, length):
        self.threads = []
        self.require_length = length

    def append(self, is_down):
        if len(self.threads) >= self.require_length:
            raise RowFullError
        self.threads.append(is_down)

    def __str__(self):
        return "".join(is_down and "X" or "•"
                       for is_down in reversed(self.threads))

def main():
    a = row = Row(37)
    loop = 2, 1, 2, 3
    is_down = True

    try:
        for _ in range(100):
            for num_threads in loop:
                for _ in range(num_threads):
                    row.append(is_down)
                is_down = not is_down
    except RowFullError:
        pass
    print(row)

if __name__ == "__main__":
    main()
