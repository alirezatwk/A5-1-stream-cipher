from keystream_gen import KeyStreamGenerator


class Encrypt:
    def __init__(self, filename, session_key):
        self.key_stream_generator = KeyStreamGenerator()
        self.key_stream_generator.set_session_key(session_key=session_key)
        # TODO: Handle when there is no file
        try:
            self.file_reader = open(filename, 'rb')
            self.file_writer = open(filename + '.enc', 'wb')
        except IOError:
            print('problem with file opening')

    def encrypt(self):
        bin_file = bytearray(self.file_reader.read())
        size = len(bin_file)
        output_bin = bytearray(size)
        for i in range(size):
            key_byte = int(self.key_stream_generator.run(output_size=8), 2)
            output_bin[i] = bin_file[i] ^ key_byte
        self.file_writer.write(output_bin)

    def __del__(self):
        self.file_reader.close()
        self.file_writer.close()


if __name__ == '__main__':
    filename = input('filename: ')
    session_key = input('session key: ')
    encrypt = Encrypt(filename=filename, session_key=session_key)
    encrypt.encrypt()
