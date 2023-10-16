
# just use np.clip?
def round_number(rgb_num):
    if rgb_num < 0:
        rgb_num = 0
    elif rgb_num > 1:
        rgb_num = 1
    return rgb_num


class Color:
    # we need to check incorrect rgb values (not in 0-1?)
    def __init__(self, r: float, g: float, b: float):
        self.r = round_number(r)
        self.g = round_number(g)
        self.b = round_number(b)

    def add_color(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def mult_color(self, other):
        return Color(self.r * other.r, self.g * other.g, self.b * other.b)

    def mult_scalar_color(self, scalar):
        return Color(self.r * scalar, self.g * scalar, self.b * scalar)

    def grayscale_color(self):
        outSum = self.r + self.g + self.b
        return outSum / 3
