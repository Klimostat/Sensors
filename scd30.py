import time
from machine import Pin, SoftI2C


def check_word(word: int, name: str = "value"):
    """Checks that a word is a valid two-byte value and throws otherwise.

    Parameters:
        word: integer value to check.
        name (optional): name of the variable to include in the error.
    """
    if not 0 <= word <= 0xFFFF:
        raise ValueError("{} outside valid two-byte word range: {}".format(name, word))


def crc8(word: int):
    check_word(word, "word")
    polynomial = 0x31
    rem = 0xFF
    word_bytes = int(word).to_bytes(2, "big")
    for byte in word_bytes:
        rem ^= byte
        for _ in range(8):
            if rem & 0x80:
                rem = (rem << 1) ^ polynomial
            else:
                rem = rem << 1
            rem &= 0xFF

    return rem


class SCD30:
    def __init__(self):
        self._i2c_addr = 0x61
        self.i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000)

    def _send_command(self, command: int, num_response_words: int = 1, arguments: list = []):
        check_word(command, "command")

        raw_message = list(int(command).to_bytes(2, "big"))
        for argument in arguments:
            check_word(argument, "argument")
            raw_message.append(crc8(argument))

        self.i2c.writeto(self._i2c_addr, raw_message)

        # The interface description suggests a >3ms delay between writes and
        # reads for most commands.
        time.sleep_ms(10)

        if num_response_words == 0:
            return []

        read_txn = self.i2c.readfrom(self._i2c_addr, num_response_words * 3)

        raw_response = list(read_txn)

        if len(raw_response) != 3 * num_response_words:
            print("Wrong response length: {}".format(len(raw_response)))
            print("(expected {})".format(3 * num_response_words))

        # Data is returned as a sequence of num_response_words 2-byte words
        # (big-endian), each with a CRC-8 checksum:
        # [MSB0, LSB0, CRC0, MSB1, LSB1, CRC1, ...]
        response = []
        for i in range(num_response_words):
            # word_with_crc contains [MSB, LSB, CRC] for the i-th response word
            word_with_crc = raw_response[3 * i: 3 * i + 3]
            word = int.from_bytes(word_with_crc[:2], "big")
            response_crc = word_with_crc[2]
            computed_crc = crc8(word)
            if response_crc != computed_crc:
                return None
            response.append(word)

        return response
