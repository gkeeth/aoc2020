#! /usr/bin/env python

class DoorLock(object):
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            lines = infile.readlines()
            self.card_publickey = int(lines[0])
            self.door_publickey = int(lines[1])

    def find_loop_size(self):
        """
        calculate loop sizes for the keycard and the door based on the public
        key. Return (card_loopsize, door_loopsize)
        """
        loop_counts = []
        for publickey in (self.card_publickey, self.door_publickey):
            value = 1
            subject = 7
            for n in range(100000000):
                value *= subject
                value %= 20201227
                if value == publickey:
                    loop_counts.append(n + 1)
                    break

        return tuple(loop_counts)

    def find_encryption_key(self):
        card_loopsize, door_loopsize = self.find_loop_size()
        encryption_keys = []
        for publickey, loopsize in ((self.card_publickey, door_loopsize), (self.door_publickey, card_loopsize)):
            value = 1
            subject = publickey
            for n in range(loopsize):
                value *= subject
                value %= 20201227
            encryption_keys.append(value)

        if encryption_keys[0] == encryption_keys[1]:
            return encryption_keys[0]
        else:
            print("encryption keys don't match")



if __name__ == "__main__":
    d = DoorLock("inputs/day25_test.txt")
    print(f"day25a test: {d.find_loop_size()}")
    d = DoorLock("inputs/day25.txt")
    print(f"day25a: {d.find_encryption_key()}")

