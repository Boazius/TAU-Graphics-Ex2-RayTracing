import raytracer
import sys

# Set default width and height values
DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500


def main():
    # Initialize the RayTracer object
    ray_tracer = raytracer.RayTracer()

    # Initialize scene_file_name and output_file_name variables
    scene_file_name = ""
    output_file_name = ""

    # Check the number of arguments provided through the command line
    if len(sys.argv) < 3:
        print("Error: Insufficient arguments provided.")
        return
    elif len(sys.argv) == 3:
        scene_file_name = sys.argv[1]
        output_file_name = sys.argv[2]
    elif len(sys.argv) == 4:
        print("Error: invalid arguments provided.")
        return
    elif len(sys.argv) == 5:
        # Accept optional width and height arguments
        try:
            width = int(sys.argv[3])
            height = int(sys.argv[4])
            ray_tracer.image_width = width
            ray_tracer.image_height = height
            scene_file_name = sys.argv[1]
            output_file_name = sys.argv[2]
        except ValueError:
            print("Error: Width and height must be integer values.")
            return
    else:
        print("Error: Too many arguments provided.")
        return

    # Parse the scene from the specified file
    ray_tracer.parseScene(scene_file_name)

    # Render the scene and save the output image
    ray_tracer.renderScene(output_file_name)


if __name__ == '__main__':
    main()
