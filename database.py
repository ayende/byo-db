import io
from functools import total_ordering
import os
from sortedcontainers import SortedList


class Database:
    def __init__(self, dir) -> None:
        self.keys = SortedList()
        if not os.path.exists(dir):
            os.makedirs(dir)

        self.data = open(dir + "/data", "w+b")
        self.log = open(dir + "/log", "w+b")

        while True:
            b = self.log.read(4)
            if len(b) == 0:
                break
            size = int.from_bytes(b, byteorder="little")
            key = self.log.read(size)
            pos = int.from_bytes(self.read(8), byteorder="little")
            item = _Key(key, pos)
            idx = self.keys.bisect_left(item)
            if idx < len(self.keys) and self.keys[idx].key.eq(key):
                self.keys[idx].pos = pos  # update pos
            else:
                self.keys.add(item)

    def get(self, key: bytes) -> bytes:
        idx = self.keys.bisect_left(_Key(key, 0))
        if idx > len(self.keys) or not self.keys[idx].eq(key):
            return None

        return self.read(idx)

    def read(self, idx):
        self.data.seek(self.keys[idx].pos, io.SEEK_SET)
        size = int.from_bytes(self.data.read(4), byteorder="little")
        return self.data.read(size)

    def put(self, key: bytes, value: bytes):
        idx = self.keys.bisect_left(_Key(key, 0))
        if idx < len(self.keys) and self.keys[idx].eq(key):  # update
            self.data.seek(self.keys[idx].pos, io.SEEK_CUR)
            size = int.from_bytes(self.data.read(4), byteorder="little")
            if size <= len(value):  # can fit
                self.data.seek(self.keys[idx].pos, io.SEEK_SET)
                self.data.write(len(value).to_bytes(4, byteorder="little"))
                self.data.write(value)
                return self.keys[idx].pos
            # cannot fit, need a new location
            self.keys[idx].pos = self.writeAtEnd(self.data, value, None)
            return self.keys[idx].pos

        pos = self.writeAtEnd(self.data, value, None)
        self.writeAtEnd(self.log, key, pos)
        self.keys.add(_Key(key, pos))
        return pos

    def writeAtEnd(self, file, val, offset):
        pos = file.seek(0, io.SEEK_END)
        file.write(len(val).to_bytes(4, byteorder="little"))
        file.write(val)
        if offset is not None:
            file.write(offset.to_bytes(8, byteorder="little"))

        return pos

    def iterator(self, prefix=b""):
        start = self.keys.bisect_left(_Key(prefix, 0))
        for idx in range(start, len(self.keys)):
            if not self.keys[idx].key.startswith(prefix):
                break
            yield self.keys[idx].key, self.read(idx)


@total_ordering
class _Key:
    def __init__(self, key: bytes, pos) -> None:
        self.key = key
        self.pos = pos

    def __lt__(self, other) -> bool:
        return self.key.__lt__(other.key)

    def __eq__(self, other) -> bool:
        return self.key.__eq__(other.key)

    def eq(self, key):
        return self.key.__eq__(key)
