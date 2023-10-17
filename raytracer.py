
# Imports
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


# Saves the image in the disk
def save_image(width: int, image: list, file_name):
    try:
        image = np.clip(image, 0, 1)
        result = Image.fromarray((image * 255).astype(np.uint8), mode='RGB')
        result.show()
        result.save(file_name)
    except Exception as e:
        print(f"Error occurred when trying to save the image in {file_name}: {e}")


# Ray Tracer Class
class RayTracer:
    image_width = 500
    image_height = 500

    def __init__(self):
        self.camera = None
        self.scene = None

    def parse_scene(self, scene_file_name):
        print(f"starting to parse the scene file {scene_file_name}")
        material_list = []  # List of materials
        shape_list = []  # List of shapes
        light_point_list = []  # List of light points
        background = 0  # Will be Color from input
        shade_rays = 0
        rec_lvl = 0

        # Open file and read line by line
        with open(scene_file_name) as f:
            line_num = 0
            for line in f:
                line = line.strip()
                line_num += 1
                if not line or line[0] == '#':  # Comment line skip
                    continue
                else:
                    code = line[0:3].lower()
                    # Split with whitespaces
                    params = line[3:].strip().lower().split()
                    
                    # Camera line
                    if code == "cam":
                        position = np.array([float(params[0]), float(params[1]), float(params[2])])
                        look_at = np.array([float(params[3]), float(params[4]), float(params[5])])
                        up = np.array([float(params[6]), float(params[7]), float(params[8])])
                        self.camera = Camera(position, look_at, up, float(params[9]), float(params[10]))
                        print(f"Parsed camera parameters (line {line_num})")
                        
                    # Set line
                    elif code == "set":
                        background = Color(float(params[0]), float(params[1]), float(params[2]))
                        shade_rays = int(params[3])
                        rec_lvl = int(params[4])
                        print(f"Parsed general settings (line {line_num})")
                        
                    # Material line
                    elif code == "mtl":
                        diffuse = Color(float(params[0]), float(params[1]), float(params[2]))
                        specular = Color(float(params[3]), float(params[4]), float(params[5]))
                        reflection = Color(float(params[6]), float(params[7]), float(params[8]))
                        material = Material(diffuse, specular, reflection, float(params[9]), float(params[10]))
                        material_list.append(material)
                        print(f"Parsed material (line {line_num})")
                    # Sphere line
                    elif code == "sph":
                        center = np.array([float(params[0]), float(params[1]), float(params[2])])
                        sphere = Sphere(center, float(params[3]), material_list[int(params[4]) - 1])
                        shape_list.append(sphere)
                        print(f"Parsed sphere (line {line_num})")
                    # Plane line
                    elif code == "pln":
                        curr_vector = np.array([float(params[0]), float(params[1]), float(params[2])])
                        plane = Plane(curr_vector, float(params[3]), material_list[int(params[4]) - 1])
                        shape_list.append(plane)
                        print(f"Parsed plane (line {line_num})")
                    # box line
                    elif code == "box":
                        center = np.array([float(params[0]), float(params[1]), float(params[2])])
                        scale = float(params[3])
                        curr_material_index = int(params[4])
                        box = Box(center, np.array([scale, scale, scale]), material_list[curr_material_index - 1])
                        shape_list.append(box)
                        print(f"Parsed Box (line {line_num})")
                    # Light line
                    elif code == "lgt":
                        curr_light_vector = np.array([float(params[0]), float(params[1]), float(params[2])])
                        color = Color(float(params[3]), float(params[4]), float(params[5]))
                        light = LightPoint(curr_light_vector, color, float(params[6]), float(params[7]), float(params[8]))
                        light_point_list.append(light)
                        print(f"Parsed light (line {line_num})")
                    # Invalid line
                    else:
                        print(f"ERROR: Did not recognize object: {code} (line {line_num})")
        
        # Create the scene   
        curr_scene = Scene(shape_list, material_list, light_point_list, background, rec_lvl, shade_rays)
        self.scene = curr_scene
        print(f"Finished parsing scene file {scene_file_name}")

    # Renders the scene
    def render_scene(self, output_file_name):
        start_time = time.time()
        rgb_data = self.ray_casting_scene(self.camera, self.scene, self.image_width, self.image_height)
        save_image(self.image_width, rgb_data, output_file_name)
        end_time = time.time()
        render_time = end_time - start_time
        print(f"Finished in {render_time / 60} minutes")

    # Perform ray casting for the given scene and camera, producing an array of RGB values.
    def ray_casting_scene(self, c: Camera, scene: Scene, width, height):
            """
            Args:
                c (Camera): The camera used for rendering the scene.
                scene (Scene): The scene to be rendered.
                width (int): Width of the output image.
                height (int): Height of the output image.

            Returns:
                np.ndarray: A numpy array containing RGB values for the rendered scene.

            """
            # Initialize variables
            screen_height = c.screen_width / width * height
            rgb_data_size = self.image_width * self.image_height * 3
            pixel_to_the_right = vector.multiply(c.right, c.screen_width / width)
            pixel_to_down = vector.multiply(c.up, -screen_height / height)
            height_vec = vector.multiply(c.look_at, c.screen_height)
            width_vec = vector.multiply(c.right, -c.screen_width / 2)
            up_by_height_vec = vector.multiply(c.up, screen_height / 2)
            cur_screen_point = vector.add(vector.add(c.position, height_vec), vector.add(width_vec, up_by_height_vec))
            cur_screen_point = vector.add(cur_screen_point, vector.multiply([pixel_to_down], 0.5))
            image_RGB_matrix = [0] * rgb_data_size

            # Perform ray casting for each pixel
            for y in range(height):
                for x in range(width):
                    ray_direction = vector.normalized(vector.minus(cur_screen_point, c.position))
                    intersection = scene.ray_cast(Ray(c.position, ray_direction))
                    cur_screen_point_color = scene.compute_color(intersection, 0, 1)
                    pixel_id = (y * self.image_height + x) * 3
                    image_RGB_matrix[pixel_id] = cur_screen_point_color.r
                    image_RGB_matrix[pixel_id + 1] = cur_screen_point_color.g
                    image_RGB_matrix[pixel_id + 2] = cur_screen_point_color.b
                    cur_screen_point = vector.add(cur_screen_point, pixel_to_the_right)

                # Update the position for the next row
                cur_screen_point = vector.minus(cur_screen_point, vector.multiply(pixel_to_the_right, width))
                cur_screen_point = vector.add(cur_screen_point, pixel_to_down)

            # Convert the result to a numpy array
            rgb_nparray = np.asarray(image_RGB_matrix)
            rgb_nparray = rgb_nparray.reshape((self.image_width, self.image_height, 3))
            return rgb_nparray
