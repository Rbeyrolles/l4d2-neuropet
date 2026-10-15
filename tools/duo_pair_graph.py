"""Replicated two-pet coordinator for two separately rendered HUD materials.

Both materials evaluate both pets with the same deterministic noise and clock.
They export different characters, without alternating a shared draw resource.
"""
import re
from client_behavior import Program

FLOOR, TOP, SPAN = 432.0, -20.0, 96.0


class Graph(Program):
    def __init__(self):
        super().__init__()
        self.number = 0
        self.constants = {}
        self.persistent = set()

    def keep(self, name, value=0):
        if isinstance(value, (int, float)):
            value = float(value)
        key = self.var(name, value)
        self.persistent.add(key)
        return key

    def c(self, value):
        if value not in self.constants:
            self.constants[value] = self.var("c" + str(len(self.constants)), float(value))
        return self.constants[value]

    def temp(self):
        self.number += 1
        return self.var("t" + str(self.number))

    def calc(self, name, a, b=None, **args):
        dest = self.temp()
        if b is not None:
            self.op(name, a, b, dest)
        else:
            self.emit(name, srcVar1=a, resultVar=dest, **args)
        return dest

    def choose(self, a, b, yes, no):
        if yes == no:
            return yes
        if a == b:
            return yes
        dest = self.temp()
        self.select(a, b, yes, no, dest)
        return dest

    def le(self, a, b):
        return self.choose(a, b, self.c(1), self.c(0))

    def mul(self, a, b):
        return self.calc("Multiply", a, b)

    def add(self, a, b):
        return self.calc("Add", a, b)

    def sub(self, a, b):
        return self.calc("Subtract", a, b)

    def clamp(self, a, lo=0, hi=1):
        return self.calc("Clamp", a, min=lo, max=hi)

    def absolute(self, a):
        return self.calc("Abs", a)

    def is_temporary(self, key):
        # Vector outputs such as $np_translate[0] are externally observed.
        # Only numbered SSA variables are disposable compiler temporaries.
        return bool(re.fullmatch(r"\$np_t[0-9]+", key))

    def eq(self, a, number):
        delta = self.sub(a, self.c(number))
        return self.le(self.mul(delta, delta), self.c(0))

    def noise(self, time, key, salt):
        # A deterministic shared sample. Only the held phase-boundary key
        # contributes, so extra binds and frame timing cannot resample it.
        return self.calc("Frac", self.add(self.mul(key, self.c(31.731)), self.c(salt)))

    def compact(self):
        """Reuse only temporary registers, after their final instruction use."""
        self.optimize()
        temporary = {key for key in self.values if self.is_temporary(key)}
        # Do not classify persistent names such as time/target as temporaries.
        temporary -= self.persistent
        intervals = {}
        for i, item in enumerate(self.proxies):
            for label, value in item["values"].items():
                if isinstance(value, str) and value in temporary:
                    if label == "resultVar":
                        intervals.setdefault(value, [i, i])
                    else:
                        assert value in intervals, (i, value)
                        intervals[value][1] = i
        assignments, live, free, count = {}, [], [], 0
        for key, (start, finish) in sorted(intervals.items(), key=lambda item: item[1][0]):
            expired = [(end, register) for end, register in live if end < start]
            live = [(end, register) for end, register in live if end >= start]
            free.extend(register for _, register in expired)
            if free:
                register = free.pop()
            else:
                register = "$np_s" + str(count)
                count += 1
            assignments[key] = register
            live.append((finish, register))
        for key in temporary:
            del self.values[key]
        self.values.update({"$np_s" + str(i): 0.0 for i in range(count)})
        for item in self.proxies:
            item["values"] = {label: assignments.get(value, value) if isinstance(value, str) else value
                              for label, value in item["values"].items()}
        self.deduplicate_constants()
        return count

    def optimize(self):
        """Eliminate duplicate pure operations and safe, single-use copies."""
        versions, aliases, cache, output = {}, {}, {}, []
        def resolved(value):
            while isinstance(value, str) and value in aliases:
                value = aliases[value]
            return value
        for item in self.proxies:
            args = {key: resolved(value) if key != "resultVar" else value
                    for key, value in item["values"].items()}
            dest = args["resultVar"]
            inputs = tuple((key, value, versions.get(value, 0) if isinstance(value, str) else 0)
                           for key, value in sorted(args.items()) if key != "resultVar")
            key = (item["name"], inputs)
            temporary = self.is_temporary(dest)
            if temporary and item["name"] not in ("UniformNoise", "TextureTransform") and key in cache:
                aliases[dest] = cache[key]
                continue
            output.append({"name": item["name"], "values": args})
            versions[dest] = versions.get(dest, 0) + 1
            if temporary and item["name"] not in ("UniformNoise", "TextureTransform"):
                cache[key] = dest
        self.proxies = output
        changed = True
        while changed:
            changed = False
            readers = {}
            writers = {}
            for i, item in enumerate(self.proxies):
                for key, value in item["values"].items():
                    if not isinstance(value, str):
                        continue
                    if key == "resultVar":
                        writers.setdefault(value, []).append(i)
                    else:
                        readers.setdefault(value, []).append(i)
            remove = set()
            for temporary, indices in writers.items():
                if not self.is_temporary(temporary) or len(indices) != 1:
                    continue
                producer = indices[0]
                uses = readers.get(temporary, [])
                if not uses:
                    remove.add(producer)
                    changed = True
                else:
                    consumers = [i for i in uses if self.proxies[i]["name"] == "Equals"
                                 and self.proxies[i]["values"].get("srcVar1") == temporary]
                    if not consumers:
                        continue
                    consumer = consumers[0]
                    item = self.proxies[consumer]
                    destination = item["values"]["resultVar"]
                    # CFunctionProxy input slots do not accept vector components.
                    # Keep scalar temporaries scalar until their final vector copy.
                    if "[" in destination:
                        continue
                    base_destination = destination.split("[", 1)[0]
                    between = self.proxies[producer + 1:consumer]
                    if any(isinstance(value, str) and value.split("[", 1)[0] == base_destination
                           for middle in between for value in middle["values"].values()):
                        continue
                    if any(self.proxies[i]["values"]["resultVar"].split("[", 1)[0] == base_destination
                           for i in range(consumer + 1, max(uses) + 1)):
                        continue
                    self.proxies[producer]["values"]["resultVar"] = destination
                    for i in uses:
                        if i != consumer:
                            self.proxies[i]["values"] = {key: destination if key != "resultVar" and value == temporary else value
                                                        for key, value in self.proxies[i]["values"].items()}
                    remove.add(consumer)
                    changed = True
            if remove:
                self.proxies = [item for i, item in enumerate(self.proxies) if i not in remove]

