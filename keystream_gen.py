class KeyStreamGenerator:

    def __init__(self):
        self.lfsr = None
        self.length = [19, 22, 23]
        self.clocking_bit = [8, 10, 10]
        self.tapped_bits = [[13, 16, 17, 18], [20, 21], [7, 20, 21, 22]]
        self.clear_registers()

    def clear_registers(self):
        self.lfsr = []
        for length in self.length:
            self.lfsr.append([0] * length)

    def check_session_key(self, session_key: str):
        if len(session_key) != 64:
            raise Exception('session key must be exactly 64 bit')
        for char in session_key:
            if char == '0' or char == '1':
                continue
            raise Exception('session key must consists of 0 and 1')

    def shift_register(self, register_idx):
        for i in range(self.length[register_idx] - 1, 0, -1):
            self.lfsr[register_idx][i] = self.lfsr[register_idx][i - 1]
        self.lfsr[register_idx][0] = 0

    def clock_register(self, register_idx, input_bit):
        tapped_bits_result = 0
        for tapped_bit_idx in self.tapped_bits[register_idx]:
            tapped_bits_result ^= self.lfsr[register_idx][tapped_bit_idx]
        self.shift_register(register_idx=register_idx)
        self.lfsr[register_idx][0] = input_bit ^ tapped_bits_result

    def ignoring_irregular_clock(self, input_bit):
        self.clock_register(register_idx=0, input_bit=input_bit)
        self.clock_register(register_idx=1, input_bit=input_bit)
        self.clock_register(register_idx=2, input_bit=input_bit)

    def calculate_majority_bit(self):
        count = [0, 0]
        for i in range(3):
            count[self.lfsr[i][self.clocking_bit[i]]] += 1
        if count[0] < count[1]:
            return 1
        return 0

    def irregular_clock(self):
        majority_bit = self.calculate_majority_bit()
        result_bit = 0
        for i in range(3):
            result_bit ^= self.lfsr[i][-1]
        for i in range(3):
            if majority_bit == self.lfsr[i][self.clocking_bit[i]]:
                self.clock_register(register_idx=i, input_bit=0)
        return result_bit

    def initialization(self, session_key):
        for bit in session_key:
            self.ignoring_irregular_clock(input_bit=int(bit))

    def set_session_key(self, session_key: str):
        self.check_session_key(session_key=session_key)
        self.initialization(session_key=session_key)

    def run(self, output_size: int):
        output = []
        for i in range(output_size):
            output.append(self.irregular_clock())
        return ''.join(map(str, output))


if __name__ == '__main__':
    session_key = input('session key: ')
    output_bit_size = int(input('output bit size: '))
    key_stream_generator = KeyStreamGenerator()
    key_stream_generator.set_session_key(session_key=session_key)
    print(key_stream_generator.run(output_size=output_bit_size))
