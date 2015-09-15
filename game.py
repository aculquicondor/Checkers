class Table(object):

    def __init__(self):
        self.turn = 0
        self.tab = [[-1] * 8 for _ in xrange(8)]
        for r in xrange(3):
            for c in xrange(r & 1, 8, 2):
                self.tab[r][c] = 1
        for r in xrange(5, 8):
            for c in xrange(r & 1, 8, 2):
                self.tab[r][c] = 0

    def __call__(self, row, col):
        return self.tab[row][col]

    def valid(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def unchecked_move(self, src, dst, eat):
        self.tab[src[0]][src[1]] = -1
        self.tab[dst[0]][dst[1]] = self.turn
        if eat:
            mid = [(src[x] + dst[x]) >> 1 for x in xrange(2)]
            self.tab[mid[0]][mid[1]] = -1
        self.turn = 1 - self.turn

    def restore_move(self, src, dst, eat):
        self.turn = 1 - self.turn
        self.tab[src[0]][src[1]] = self.turn
        self.tab[dst[0]][dst[1]] = -1
        if eat:
            mid = [(src[x] + dst[x]) >> 1 for x in xrange(2)]
            self.tab[mid[0]][mid[1]] = 1 - self.turn

    def move(self, src, dst):
        if not self.valid(*src) or not self.valid(*dst) or \
                self.tab[src[0]][src[1]] != self.turn or \
                self.tab[dst[0]][dst[1]] != -1:
            return False
        diff = [abs(src[x] - dst[x]) for x in xrange(2)]
        if diff[0] != diff[1] or diff[0] not in (1, 2) or \
                ((src[0] < dst[0]) ^ self.turn):
            return False
        mid = [(src[x] + dst[x]) >> 1 for x in xrange(2)]
        if diff[0] == 2 and self.tab[mid[0]][mid[1]] != 1 - self.turn:
            return False
        self.tab[src[0]][src[1]] = -1
        self.tab[dst[0]][dst[1]] = self.turn
        if diff[0] == 2:
            self.tab[mid[0]][mid[1]] = -1
        self.turn = 1 - self.turn
        return True

    def points(self, player):
        cnt = 0
        for r in xrange(8):
            for c in xrange(r & 1, 8, 2):
                if self.tab[r][c] == player:
                    cnt += 1
                elif self.tab[r][c] != -1:
                    cnt -= 1
        return cnt

    def positions(self):
        for r in xrange(8):
            for c in xrange(r & 1, 8, 2):
                if self.tab[r][c] == self.turn:
                    yield r, c

    def moves(self, row, col):
        mvs = zip([-1, -1], [-1, 1]) if self.turn == 0 else \
            zip([1, 1], [-1, 1])
        for dr, dc in mvs:
            r, c = row + dr, col + dc
            rr, cc = r + dr, c + dc
            if not self.valid(r, c):
                continue
            if self.tab[r][c] == -1:
                yield r, c, False
            elif self.tab[r][c] == 1 - self.turn and self.valid(rr, cc) and \
                    self.tab[rr][cc] == -1:
                yield rr, cc, True
