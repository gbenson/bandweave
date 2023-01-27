from pyweaving import Color, Draft
from pyweaving.render import ImageRenderer

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
    BLACK = Color((0, 0, 0))    # Black (105)
    TEAL = Color((7,82, 117))   # Dark Teal (147)
    BLUE = Color((7, 81, 155))  # Royal Blue (148)
    WASABI = Color((194, 214, 164))  # Wasabi (144)

    COLORS = [BLACK]*6 + [TEAL]*15 + [BLUE, TEAL]*8 + [BLUE]*17
    COLORS = tuple(COLORS) + tuple(reversed(COLORS))  # Mirror
    COLORS = COLORS[1:-1]  # Lose selvedges

    SCALE = 2
    LENGTH = len(COLORS) // SCALE

    # Build the pattern row-by-row (weft-by-weft)
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

    # "Turn" the draft to access it column-by-column (warp-by-warp)
    cols = tuple(reversed(list(zip(*(row.threads for row in rows)))))
    print("\n".join(("".join(is_down and "X" or "•"
                             for is_down in col))
                    for col in cols))

    # Count the shafts
    shafts = {}
    for column in cols:
        if column not in shafts:
            shafts[column] = len(shafts)

    # Create the draft
    draft = Draft(num_shafts=len(shafts))

    for column in cols:
        shaft = draft.shafts[shafts[column]]
        for __ in range(SCALE):
            color = COLORS[len(draft.warp)]
            draft.add_warp_thread(color=color, shaft=shaft)

    for row_id in range(len(rows)):
        row_shafts = set()
        for column in cols:
            if column[row_id]:
                row_shafts.add(draft.shafts[shafts[column]])
        draft.add_weft_thread(color=WASABI, shafts=row_shafts)

    # Render the image
    img = ImageRenderer(draft)
    img.save("out.png")
    img.show()

if __name__ == "__main__":
    main()
