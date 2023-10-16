import numpy as np
import vector
from camera import Camera
from color import Color
from material import Material
from sphere import Sphere
from plane import Plane
from lightpoint import LightPoint
from scene import Scene
from box import Box
from ray import Ray
import time
from PIL import Image


# static saver
def save_image(width: int, image: list, file_name):
    try:
        image = np.clip(image, 0, 1)
        result = Image.fromarray(np.uint8(image * 255), mode='RGB')
        result.show()
        result.save(file_name)
    except:
        print("error occured when tried to save image in {f}".format(f=file_name))


class RayTracer:
    # ********** fields init with default values **********
    image_width = 500
    image_height = 500

    def __init__(self):
        self.camera = None
        self.scene = None

    def parseScene(self, sceneFileName):
        print("starting to parse the scene file " + sceneFileName)
        materialList = []  # of materials
        shapeList = []  # of shapes
        light_point_list = []  # of light points
        backGround = 0  # will be Color from input
        shadeRays = 0
        recLvl = 0

        # open file and read line by line
        f = open(sceneFileName)
        lineNum = 0
        for line in f:
            line = line.strip()
            lineNum += 1
            if not line or (line[0] == '#'):  # comment line skip
                continue
            else:
                code = line[0:3].lower()
                # split with whitespaces
                params = line[3:].strip().lower().split()
                if code == "cam":
                    position = np.array([float(params[0]), float(params[1]), float(params[2])])
                    lookAt = np.array([float(params[3]), float(params[4]), float(params[5])])
                    up = np.array([float(params[6]), float(params[7]), float(params[8])])
                    self.camera = Camera(position, lookAt, up, float(params[9]), float(params[10]))
                    print("Parsed camera parameters (line {l})".format(l=lineNum))
                elif code == "set":
                    backGround = Color(float(params[0]), float(params[1]), float(params[2]))
                    shadeRays = int(params[3])
                    recLvl = int(params[4])
                    print("Parsed general settings (line {l})".format(l=lineNum))
                elif code == "mtl":
                    diffuse = Color(float(params[0]), float(params[1]), float(params[2]))
                    specular = Color(float(params[3]), float(params[4]), float(params[5]))
                    reflection = Color(float(params[6]), float(params[7]), float(params[8]))
                    material = Material(diffuse, specular, reflection, float(params[9]), float(params[10]))
                    materialList.append(material)
                    print("Parsed material (line {l})".format(l=lineNum))
                elif code == "sph":
                    center = np.array([float(params[0]), float(params[1]), float(params[2])])
                    sphere = Sphere(center, float(params[3]), materialList[int(params[4]) - 1])
                    shapeList.append(sphere)
                    print("Parsed sphere (line {l})".format(l=lineNum))
                elif code == "pln":
                    currVector = np.array([float(params[0]), float(params[1]), float(params[2])])
                    plane = Plane(currVector, float(params[3]), materialList[int(params[4]) - 1])
                    shapeList.append(plane)
                    print("Parsed plane (line {l})".format(l=lineNum))
                elif code == "box":
                    center = np.array([float(params[0]), float(params[1]), float(params[2])])
                    scale = float(params[3])
                    curr_material_index = int(params[4])
                    box = Box(center, np.array([scale, scale, scale]), materialList[curr_material_index - 1])
                    shapeList.append(box)
                    print("Parsed Box (line {l})".format(l=lineNum))
                elif code == "lgt":
                    curr_light_vector = np.array([float(params[0]), float(params[1]), float(params[2])])
                    color = Color(float(params[3]), float(params[4]), float(params[5]))
                    light = LightPoint(curr_light_vector, color, float(params[6]), float(params[7]), float(params[8]))
                    light_point_list.append(light)
                    print("Parsed light (line {l})".format(l=lineNum))
                else:
                    print("ERROR: Did not recognize object: {c} (line {l})".format(c=code, l=lineNum))
        curr_scene = Scene(shapeList, materialList, light_point_list, backGround, recLvl, shadeRays)
        self.scene = curr_scene
        print("Finished parsing scene file " + sceneFileName)

    def renderScene(self, output_file_name):
        start_time = time.time()
        rgb_data = self.ray_casting_scene(self.camera, self.scene, self.image_width, self.image_height)
        save_image(self.image_width, rgb_data, output_file_name)
        end_time = time.time()
        render_time = end_time - start_time
        print("finished in " + str(render_time / 60) + " minutes")

    def ray_casting_scene(self, c: Camera, scene: Scene, width, height):
        screen_height = c.screen_width / width * height
        # first screen point
        rgb_data_size = self.image_width * self.image_height * 3
        pixel_to_the_right = vector.multiply(c.right, c.screen_width / width)
        pixel_to_down = vector.multiply(c.up, -screen_height / height)
        height_vec = vector.multiply(c.look_at, c.screen_height)
        width_vec = vector.multiply(c.right, -c.screen_width / 2)
        up_by_height_vec = vector.multiply(c.up, screen_height / 2)
        cur_screen_point = vector.add(vector.add(c.position, height_vec), vector.add(width_vec, up_by_height_vec))
        cur_screen_point = vector.add(cur_screen_point, vector.multiply(pixel_to_the_right, 0.5))
        cur_screen_point = vector.add(cur_screen_point, vector.multiply([pixel_to_down], 0.5))
        rgb_big_array = [0] * rgb_data_size

        for y in range(height):
            for x in range(width):
                rayDirection = vector.normalized(vector.minus(cur_screen_point, c.position))
                intersection = scene.ray_cast(Ray(c.position, rayDirection))
                curScreenPointColor = scene.compute_color(intersection, 0, 1)
                pixel_id = (y * self.image_height + x) * 3
                rgb_big_array[pixel_id] = curScreenPointColor.r
                rgb_big_array[pixel_id + 1] = curScreenPointColor.g
                rgb_big_array[pixel_id + 2] = curScreenPointColor.b
                cur_screen_point = vector.add(cur_screen_point, pixel_to_the_right)
            cur_screen_point = vector.minus(cur_screen_point, vector.multiply(pixel_to_the_right, width))
            cur_screen_point = vector.add(cur_screen_point, pixel_to_down)
        rgb_nparray = np.asarray(rgb_big_array)
        rgb_nparray = rgb_nparray.reshape((self.image_width, self.image_height, 3))
        return rgb_nparray
