from typing import NamedTuple, Any


class Pair(NamedTuple):
    key: Any
    value: Any


class HashTable:

    def __init__(self, capacity):                               # СТВОРЕННЯ
        self._pairs = capacity * [None]
        self.dupl = []
        self.redone = []

    def __len__(self):
        return len(self._pairs)

    def __setitem__(self, key, value):                          # ДОДАВАННЯ
        index = self._index(key)
        # print('key,ind,val:', key, index, value)                # checkpoint 1
        if self._pairs[index] is None:
            self._pairs[index] = Pair(key, value)
        else:                                                   # КОЛЛІЗІЯ
            start = index                                       # стартова позиція пошуку
            res = 0
            index += 1
            while index < len(self) and res == 0:               # шукаємо місце в другій половині таблиці (downstairs)
                res, index = self._redo(key, index, value, 1)
            if res == 0:                                        # якщо дійшли до кінця і не знайшли місця
                index = start                                   # шукаємо місце в першій половині таблиці (upstairs)
                while index >= 0 and res == 0:
                    res, index = self._redo(key, index, value, -1)
                try:
                    res == 1
                except Exception:
                    print('No more space')                      # якщо місця немає

    def _index(self, key):                                      # INDEX
        return hash(key) % len(self)

    def _redo(self, key, index, value, a):                      # ПЕРЕВИЗНАЧЕННЯ ІНДЕКСУ ЯКЩО КОЛІЗІЯ
        if self._pairs[index] is None:
            self._pairs[index] = Pair(key, value)
            res = 1
            self.dupl.append(key)
            self.redone.append([key, index])
            # print('updated key,ind,val:', key, index, value)    # checkpoint 2
        else:
            index += a
            res = 0
        return res, index

    def __getitem__(self, key):                                     # ПОШУК
        if key in self.dupl:                                        # якщо індекс ключа не є унікальним (КОЛЛІЗІЯ)
            for i in self.redone:
                if i[0] == key:
                    index = i[1]                                    # індекс, що був перевизначений для цього ключа
                    # print('getitem key + new ind', key, index)    # checkpoint 3
                    pair = self._pairs[index]
        else:
            pair = self._pairs[self._index(key)]
            if pair is None:
                raise KeyError(key)
        return pair.value

    def __delitem__(self, key):                                     # ВИДАЛЕННЯ
        if key not in self:
            raise KeyError
        if key in self.dupl:                                        # якщо індекс ключа не є унікальним (КОЛЛІЗІЯ)
            for i in self.redone:
                if i[0] == key:
                    index = i[1]                                    # індекс, що був перевизначений для цього ключа
                    self._pairs[index] = None
        else:
            self._pairs[self._index(key)] = None

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __str__(self):                                              # To PRINT ht
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"

    @property
    def pairs(self):                                                # Only pairs, without None positions
        return {pair for pair in self._pairs if pair}

    @property
    def keys(self):
        return [pair.key for pair in self.pairs]

    @property
    def values(self):
        return [pair.value for pair in self.pairs]


if __name__ == '__main__':

    ht = HashTable(10)
    ht['a'] = 4
    ht['bb'] = 5
    ht['c'] = 6
    ht['ddd'] = 7
    ht['eee'] = 8
    ht['f'] = 9
    ht['g'] = 10

    print('\nhash table inside:', ht._pairs)
    print('ht content:', ht)

    print('\ngetting items:', 'f:', ht['f'], 'a:', ht['a'])

    del ht['a']
    del ht['f']
    print('ht content after del:', ht)
