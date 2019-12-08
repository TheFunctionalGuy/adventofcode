from termcolor import colored


# Solution for: https://adventofcode.com/2019/day/8
class Image:
    def __init__(self, picture_file, width: int, height: int):
        self.width = width
        self.height = height
        self.encoded_picture = [int(pixel) for line in picture_file for pixel in line.rstrip()]

    def calculate_checksum(self) -> int:
        layers = [self.get_layer(layer) for layer in
                  range(1, len(self.encoded_picture) // (self.width * self.height) + 1)]
        zero_layers = [list(filter(lambda x: x == 0, layer)) for layer in layers]

        indices = [i + 1 for i in range(len(zero_layers))]
        zipped_zero_layers = zip(indices, zero_layers)

        fewest_zero_layer = sorted(zipped_zero_layers, key=lambda x: len(x[1]))[0][0]

        number_of_ones = len(list(filter(lambda x: x == 1, self.get_layer(fewest_zero_layer))))
        number_of_twos = len(list(filter(lambda x: x == 2, self.get_layer(fewest_zero_layer))))

        return number_of_ones * number_of_twos

    def decode(self):
        pixel_map = {}
        layers = [self.get_layer(layer) for layer in
                  range(1, len(self.encoded_picture) // (self.width * self.height) + 1)]

        for layer in layers:
            for i in range(len(layer)):
                if i not in pixel_map:
                    if layer[i] == 0:
                        pixel_map[i] = 0
                    elif layer[i] == 1:
                        pixel_map[i] = 1

        decoded_image = [pixel_map[i] for i in range(self.width * self.height)]

        return decoded_image

    def render(self):
        decoded_image = self.decode()

        for y in range(self.height):
            for x in range(self.width):
                if decoded_image[y * self.width + x] == 1:
                    print(colored('\u2588', 'yellow'), end='')
                else:
                    print(colored('\u2588', 'blue'), end='')
            print()

    def get_layer(self, layer: int):
        return self.encoded_picture[self.width * self.height * (layer - 1):self.width * self.height * layer]


def process_image():
    with open('input.txt', mode='r') as picture_file:
        image = Image(picture_file, 25, 6)
        print(image.calculate_checksum())

        # Part two
        image.render()


if __name__ == '__main__':
    process_image()
