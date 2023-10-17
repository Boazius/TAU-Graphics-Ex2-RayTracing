import numpy as np
import color
import ray
import intersection
import vector
import random


class Scene:
    """
    Class representing a scene in a 3D space.

    Attributes:
        MINIMUM_CON (float): The minimum contribution value for the scene.
        shape_list (list): A list of shapes in the scene.
        material_list (list): A list of materials in the scene.
        light_point_list (list): A list of light points in the scene.
        background (color.Color): The background color of the scene.
        rec_lvl (int): The recursion level of the scene.
        shade_ray (int): The number of shade rays in the scene.
    """

    MINIMUM_CON = 1.0 / 256

    # lists of stuff at the scene.
    def __init__(self, shape_list: list, material_list: list, light_point_list: list, background: color.Color, rec_level, shade_rays):
        """
        Initialize a Scene object with the given parameters.

        Args:
            shape_list (list): A list of shapes in the scene.
            material_list (list): A list of materials in the scene.
            light_point_list (list): A list of light points in the scene.
            background (color.Color): The background color of the scene.
            rec_level (int): The recursion level of the scene.
            shade_rays (int): The number of shade rays in the scene.
        """
        self.MINIMUM_CON = 1.0 / 256
        self.shape_list = shape_list
        self.material_list = material_list
        self.light_point_list = light_point_list
        self.background = background
        self.rec_lvl = rec_level
        self.shade_ray = shade_rays

    def ray_cast(self, r: ray.Ray):
        """
        Cast a ray in the scene and find the closest intersection.

        Args:
            r (ray.Ray): The ray to cast in the scene.

        Returns:
            intersection.Intersection or None: The closest intersection found in the scene, or None if there is no intersection.
        """
        min_distance_sq = float('inf')
        closest_intersection = None

        for shape in self.shape_list:
            inter = shape.intersect(r, False)
            if inter is not None:
                vec = vector.minus(r.start_point, inter.intersection_point)
                distance_sq = vector.dot_product(vec, vec)
                if distance_sq < min_distance_sq:
                    min_distance_sq = distance_sq
                    closest_intersection = inter

        return closest_intersection
    def compute_color(self, input_intersection: intersection.Intersection, rec_count, contribution):
        """
        Compute the color of the point based on the intersection and recursion count.

        Args:
            input_intersection (intersection.Intersection): The intersection point.
            rec_count (int): The recursion count.
            contribution (float): The contribution of the point.

        Returns:
            color.Color: The computed color of the point.
        """
        if (input_intersection is None) or (rec_count == self.rec_lvl) or (contribution < self.MINIMUM_CON):
            return self.background

        mat = input_intersection.material
        curr_color = color.Color(0, 0, 0)
        
        # Compute the base color
        mul_c_bg = self.background.mult_color(mat.diffusion)
        mul_s_bg = mul_c_bg.mult_scalar_color(mat.transparency)
        curr_color = curr_color.add_color(mul_s_bg)

        inter_point = input_intersection.intersection_point
        for light_point in self.light_point_list:
            # Calculate light direction and reference direction
            light_direction_rev = vector.normalized(vector.minus(light_point.position, inter_point))
            light_reference_direction = vector.normalized(vector.reflect(light_direction_rev, input_intersection.normal))
            start = vector.add(inter_point, vector.multiply(light_direction_rev, 0.001))
            illumination = 1.0
            num_shade_rays = 1.0 / self.shade_ray
            shade_ray_fraction = 1.0 / self.shade_ray / self.shade_ray * light_point.shadow
            light_width_r = vector.multiply(vector.some_perpendicular(light_direction_rev), light_point.radius)
            light_width_d = vector.multiply(vector.cross_product(light_width_r, vector.normalized(light_direction_rev)), light_point.radius)
            
            # Iterate over shade ray pairs
            for i in range(self.shade_ray):
                for j in range(self.shade_ray):
                    random_up = random.random()
                    random_right = random.random()
                    vec = vector.multiply(light_width_d, ((-self.shade_ray / 2 + j + random_up - 0.5) * num_shade_rays))
                    vec2 = vector.multiply(light_width_r, ((-self.shade_ray / 2 + i + random_right - 0.5) * num_shade_rays))
                    nearest_light_point = vector.add(light_point.position, vector.add(vec, vec2))
                    shade_direction_reversed = vector.normalized(vector.minus(nearest_light_point, start))
                    ray_length = vector.vector_len(vector.minus(start, nearest_light_point))
                    light_left_in_ray = 1.0
                    for s in self.shape_list:
                        curr_ray = ray.Ray(vector.add(start, vector.multiply(shade_direction_reversed, 0.01)), shade_direction_reversed)
                        shadow_hit = s.intersect(curr_ray, True)
                        if shadow_hit is not None and vector.vector_len(vector.minus(shadow_hit.intersection_point, start)) < ray_length:
                            light_left_in_ray *= s.material.transparency
                            if light_left_in_ray < 0:
                                light_left_in_ray = 0
                                break
                    illumination -= shade_ray_fraction * (1 - light_left_in_ray)

            if illumination > 0:
                # Compute diffuse and specular light
                diffuse_color = light_point.color.mult_color(mat.diffusion.mult_scalar_color(vector.dot_product(input_intersection.normal, light_direction_rev)))
                specular_color = light_point.color.mult_color(mat.specularity.mult_scalar_color(light_point.specularity * pow(abs(vector.dot_product(light_reference_direction, input_intersection.direction)), mat.phong)))
                curr_color = curr_color.add_color(diffuse_color.add_color(specular_color).mult_scalar_color((1 - mat.transparency) * illumination))

        # Compute reflection color
        reflection_intersection_hit = vector.reflect(input_intersection.direction, input_intersection.normal)
        ray2 = ray.Ray(vector.add(input_intersection.intersection_point, vector.multiply(reflection_intersection_hit, 0.001)), reflection_intersection_hit)
        ray_reflection = self.ray_cast(ray2)
        reflection_color = mat.reflection.mult_color(self.compute_color(ray_reflection, rec_count + 1, contribution * mat.reflection.grayscale_color()))
        curr_color = curr_color.add_color(reflection_color)

        if mat.transparency > 0:
            ray_rec = ray.Ray(vector.add(input_intersection.intersection_point, vector.multiply(input_intersection.direction, 0.01)), input_intersection.direction)
            currNext = self.ray_cast(ray_rec)
            curr_color = curr_color.add_color(self.compute_color(currNext, rec_count + 1, contribution * mat.transparency).mult_scalar_color(mat.transparency))
        
        return curr_color

