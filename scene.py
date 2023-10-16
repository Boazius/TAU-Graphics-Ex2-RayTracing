import numpy as np
import color
import ray
import intersection
import vector
import random


class Scene:
    MINIMUM_CON = 1.0 / 256

    # lists of stuff at the scene.
    def __init__(self, shape_list: list, material_list: list, light_point_list: list,
                 background: color.Color, rec_level, shade_rays):
        self.shape_list = shape_list
        self.material_list = material_list
        self.light_point_list = light_point_list
        self.background = background
        self.rec_lvl = rec_level
        self.shade_ray = shade_rays

    def ray_cast(self, r: ray.Ray):
        minDistanceSq = float('inf')
        closest_intersection = None
        # check every shape for intersection, find the minimal one
        for i in range(len(self.shape_list)):
            inter = self.shape_list[i].intersect(r, False)
            if inter is not None:
                vec = vector.minus(r.start_point, inter.intersection_point)
                distance_sq = vector.dot_product(vec, vec)
                if distance_sq < minDistanceSq:
                    minDistanceSq = distance_sq
                    closest_intersection = inter
        return closest_intersection

    # what is the color of a point?
    def compute_color(self, input_intersection: intersection.Intersection, rec_count, contribution):
        if (input_intersection is None) or (rec_count == self.rec_lvl) or (contribution < self.MINIMUM_CON):
            return self.background
        mat = input_intersection.material
        curr_color = color.Color(0, 0, 0)

        mul_c_bg = self.background.mult_color(mat.diffusion)
        mul_s_bg = mul_c_bg.mult_scalar_color(mat.transparency)
        curr_color = curr_color.add_color(mul_s_bg)

        inter_point = input_intersection.intersection_point
        # calculate every light_point in the list
        for light_point in self.light_point_list:
            light_direction_rev = vector.normalized(vector.minus(light_point.position, inter_point))
            light_reference_direction = vector.normalized(vector.reflect(light_direction_rev, input_intersection.normal))
            start = vector.add(inter_point, vector.multiply(light_direction_rev, 0.001))
            illumination = 1.0
            num_shade_rays = 1.0 / self.shade_ray
            shade_ray_fraction = 1.0 / self.shade_ray / self.shade_ray * light_point.shadow
            light_width_r = vector.multiply(vector.some_perpendicular(light_direction_rev), light_point.radius)
            light_width_d = vector.multiply(vector.cross_product(light_width_r, vector.normalized(light_direction_rev)),
                                          light_point.radius)
            # rayLength = None
            # for every shade ray pair:
            for i in range(self.shade_ray):
                for j in range(self.shade_ray):
                    random_up = random.random()
                    random_right = random.random()
                    vec = vector.multiply(light_width_d,
                                          ((-self.shade_ray / 2 + j + random_up - 0.5) * num_shade_rays))
                    vec2 = vector.multiply(light_width_r,
                                           ((-self.shade_ray / 2 + i + random_right - 0.5) * num_shade_rays))
                    nearest_light_point = vector.add(light_point.position, vector.add(vec, vec2))
                    # Reverse the direction of the shadow
                    shade_direction_reversed = vector.normalized(vector.minus(nearest_light_point, start))
                    ray_length = vector.vector_len(vector.minus(start, nearest_light_point))
                    light_left_in_ray = 1.0
                    for s in self.shape_list:
                        curr_ray = ray.Ray(vector.add(start, vector.multiply(shade_direction_reversed, 0.01)),
                                           shade_direction_reversed)
                        shadow_hit = s.intersect(curr_ray, True)
                        if shadow_hit is not None and vector.vector_len(
                                vector.minus(shadow_hit.intersection_point, start)) < ray_length:
                            light_left_in_ray *= s.material.transparency
                            if light_left_in_ray < 0:
                                light_left_in_ray = 0
                                break
                    illumination -= shade_ray_fraction * (1 - light_left_in_ray)

            if illumination > 0:
                # computation of diffuse light
                diffuse_color = light_point.color.mult_color(
                    mat.diffusion.mult_scalar_color(vector.dot_product(input_intersection.normal, light_direction_rev)))
                # computation of specular light
                specular_color = light_point.color.mult_color(mat.specularity.mult_scalar_color(
                    light_point.specularity * pow(abs(vector.dot_product(light_reference_direction, input_intersection.direction)),
                                                  mat.phong)))
                curr_color = curr_color.add_color(diffuse_color.add_color(specular_color).mult_scalar_color((1 - mat.transparency) * illumination))

        # now reflection color
        reflection_intersection_hit = vector.reflect(input_intersection.direction, input_intersection.normal)
        ray2 = ray.Ray(vector.add(input_intersection.intersection_point, vector.multiply(reflection_intersection_hit, 0.001)), reflection_intersection_hit)
        ray_reflection = self.ray_cast(ray2)
        reflection_color = mat.reflection.mult_color(
            self.compute_color(ray_reflection, rec_count + 1, contribution * mat.reflection.grayscale_color()))
        curr_color = curr_color.add_color(reflection_color)
        if mat.transparency > 0:
            ray_rec = ray.Ray(
                vector.add(input_intersection.intersection_point, vector.multiply(input_intersection.direction, 0.01)),
                input_intersection.direction)
            currNext = self.ray_cast(ray_rec)
            curr_color = curr_color.add_color(
                self.compute_color(currNext, rec_count + 1, contribution * mat.transparency).mult_scalar_color(mat.transparency))
        return curr_color
