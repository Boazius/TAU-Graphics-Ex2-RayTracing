import color


# material class

class Material:

    def __init__(self, diffusion: color.Color, specularity: color.Color, reflection: color.Color, phong: float,
                 transparency: float):
        self.diffusion = diffusion
        self.specularity = specularity
        self.reflection = reflection
        self.phong = phong
        self.transparency = transparency
