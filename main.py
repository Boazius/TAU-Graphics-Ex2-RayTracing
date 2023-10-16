import raytracer
import sys


# The code should run in the command line (you need to send a directory with
# all the python code files) and accept 4 parameters. For example:
# python RayTracer.py scenes\Spheres.txt scenes\Spheres.png 500 500
# those final two are optional, default value is 500x500
def main():
    ray_tracer = raytracer.RayTracer()
    scene_file_name = ""
    output_file_name = ""

    # count expected args and throw exception
    if len(sys.argv) < 3:
        print("not enough arguments")
        return
    if len(sys.argv) == 3:
        # Default width and height are 500x500
        # width = 500
        # height = 500
        scene_file_name = sys.argv[1]
        output_file_name = sys.argv[2]
    if len(sys.argv) == 4:
        print("input 2 arguments or 4")
        return
    if len(sys.argv) == 5:
        # We got optional arguments
        width = int(sys.argv[3])
        height = int(sys.argv[4])
        ray_tracer.image_width = width
        ray_tracer.image_height = height
        scene_file_name = sys.argv[1]
        output_file_name = sys.argv[2]
    if len(sys.argv) > 5:
        print("too many arguments")
        return

    ray_tracer.parseScene(scene_file_name)
    ray_tracer.renderScene(output_file_name)


# Main Function Run
if __name__ == '__main__':
    main()
