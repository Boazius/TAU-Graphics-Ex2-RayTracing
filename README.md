<a name="readme-top"></a>

<!-- Explanations -->
<!--
- This is a ReadMe template, cloned from https://github.com/othneildrew/Best-README-Template/
- Do a search and replace with your text editor for the following: `TAU-Graphics-Ex2-RayTracing`,`Ray Tracing Exercise`, `project_description`
- fill any TODO sections:
  - Add a logo in images/logo.png
  - fill the table of contents
  - fill the About section - with Product screenshot and tech used
-->

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Boazius/TAU-Graphics-Ex2-RayTracing">
    <img src="images/tauLogo.jpg" alt="Logo" width="200" height="200">
  </a>

<h3 align="center">Ray Tracing Exercise</h3>

  <p align="center">
    Basic ray tracer with Spheres, Cubes and planes - created as part of the TAU Graphics course
    <br />
    <a href="https://github.com/Boazius/TAU-Graphics-Ex2-RayTracing/issues">Report Bug</a>
    ·
    <a href="https://github.com/Boazius/TAU-Graphics-Ex2-RayTracing/issues">Request Feature</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project
<div align="center">
    <img src="images/pool.png" alt="Logo" width="300" height="300">
  </a>
</div>

Originally on https://github.com/nogakinor/RayTracing

### Basic Ray Tracer
This project involves the implementation of a basic ray tracer. The ray tracer simulates the propagation of light rays from an observer's eye (the camera) through a screen and into a scene containing various surfaces. The implementation calculates the intersections of rays with surfaces, determines the nearest intersection, and computes the color of the surface based on its material and lighting conditions.

<div align="center">
    <img src="images/lightingnoshadow.gif" alt="Logo" width="200" height="200">
  </a>
</div>

### Features
The ray tracer includes the following features:

#### Surfaces
- Spheres
- Infinite planes
- Cubes

#### Materials
Each surface is associated with a specific material that includes attributes such as:
- Diffuse color
- Specular color
- Phong specularity coefficient
- Reflection color
- Transparency

#### Lights
The scene is illuminated by point lights, each with attributes including position, color, specular intensity, shadow intensity, and light radius.

### Camera and General Settings
The camera is defined by parameters such as position, look-at point, up vector, screen distance, and screen width. General settings include the background color, number of shadow rays, and maximum recursion level.

### Implementation Details
The ray tracer is implemented in Python and accepts a scene file as input. The scene file contains the definition of all surfaces, materials, light sources, camera settings, and general render settings. The code is designed to run in the command line and supports the generation of images based on the provided scene description.

### Soft Shadows
The project incorporates soft shadows to simulate the effect of light sources with a certain area. The light intensity that hits the surface from the
light source will be multiplied by the number of rays that hit the surface divided
by the total number of rays we sent. For example, if we send 25 rays from the
light source and 5 of them hit the surface at the given point, the surface will
be 20% illuminated at that point. If the number of shadow rays parameter is 1
only one ray will be cast and the shadows will be hard.
The sent rays should simulate a light which has a certain area. Each light is
defined with a light radius 

### Built With
<!-- Fill the relevant technologies shields here TODO -->
[![Python][Python-shield]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
To get a local copy up and running follow these simple steps.
- clone or download the repository
- open shell in the repository folder
- verify python and pip are installed ( use ``` python --version ``` and ```pip --version```)
- install requirements using  ``` pip install -r requirements.txt ```
- copy your desired scene txt file into the folder, preferably into the input folder

now, to run the application simply type:
``` bash
python Raytracer.py
```

with the following arguments
1. An absolute / relative path to the scene text file you want to process
2. An absolute / relative path to the image png you want to create
3. (Optional) height - the output image height, defaults to 500
4. (Optional) width - the output image width, defaults to 500

so for example
``` bash
python raytracer.py "input/pool.txt", "scenes/pool200x200.png", "200", "200"
```
will run the ray tracer on pool.txt and output the pool200x200.png file.

## The Scene text file
The scenes are defined in text scene files with the following format.
Every line in the file defines a single object in the scene, and starts with a 3
letter code that identifies the object type. After the 3 letter code a list of numeric parameters is given. The parameters can be delimited by any number of
white space characters, and are parsed according to the specific order in which
they appear. Empty lines are discarded, and so are lines which begin with the
character ”#” which are used for remarks. The possible objects with their code
and list of required parameters are given below.

#### "cam" = camera settings (there will be only one per scene file)
- params[0,1,2] = position (x, y, z) of the camera
- params[3,4,5] = look-at position (x, y, z) of the camera
- params[6,7,8] = up vector (x, y, z) of the camera
- params[9] = screen distance from camera
- params[10] = screen width from camera
#### "set" = general settings for the scene (once per scene file)
- params[0,1,2] = background color (r, g, b)
- params[3] = root number of shadow rays (N 2 rays will be shot)
- params[4] = maximum number of recursions
#### "mtl" = defines a new material
- params[0,1,2] = diffuse color (r, g, b)
- params[3,4,5] = specular color (r, g, b)
- params[6,7,8] = reflection color (r, g, b)
- params[9] = phong specularity coefficient (shininess)
- params[10] = transparency value between 0 and 1
#### "sph" = defines a new sphere
- params[0,1,2] = position of the sphere center (x, y, z)
- params[3] = radius
- params[4] = material index (integer). each defined material gets an automatic material index starting from 1, 2 and so on
#### "pln" = defines a new plane
- params[0,1,2] = normal (x, y, z)
- params[3] = offset
- params[4] = material index
#### "box" = defines a new box
- params[0,1,2] = position of the box center (x, y, z)
- params[3] = scale of the box, length of each edge
- params[4] = material index
#### "lgt" = defines a new light
- params[0,1,2] = position of the light (x, y, z)
- params[3,4,5] = light color (r, g, b)
- params[6] = specular intensity
- params[7] = shadow intensity
- params[8] = light width / radius (used for soft shadows)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Prerequisites
- Python
- pip

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE.txt` for more information.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
### I can be reached at at my email: boazyakubov@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Noga Kinor for wonderful teamwork in this course
* Professor [Daniel Cohen-Or](https://www.tau.ac.il/profile/dcor) for teaching this course at TAU
* Roey Eliyahu Bar-On for instructing us on the subject at TAU

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- You can get more shields at img.shields.io , usage: [![Python][Python-shield]][Python-url] -->
[contributors-shield]: https://img.shields.io/github/contributors/Boazius/TAU-Graphics-Ex2-RayTracing.svg?style=for-the-badge
[contributors-url]: https://github.com/Boazius/TAU-Graphics-Ex2-RayTracing/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Boazius/TAU-Graphics-Ex2-RayTracing.svg?style=for-the-badge
[forks-url]: https://github.com/Boazius/TAU-Graphics-Ex2-RayTracing/network/members
[stars-shield]: https://img.shields.io/github/stars/Boazius/TAU-Graphics-Ex2-RayTracing.svg?style=for-the-badge
[stars-url]: https://github.com/Boazius/TAU-Graphics-Ex2-RayTracing/stargazers
[issues-shield]: https://img.shields.io/github/issues/Boazius/TAU-Graphics-Ex2-RayTracing.svg?style=for-the-badge
[issues-url]: https://github.com/Boazius/TAU-Graphics-Ex2-RayTracing/issues
[license-shield]: https://img.shields.io/github/license/Boazius/TAU-Graphics-Ex2-RayTracing.svg?style=for-the-badge
[license-url]: https://github.com/Boazius/TAU-Graphics-Ex2-RayTracing/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/boazyakubov
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[C-shield]: (https://img.shields.io/static/v1?style=for-the-badge&message=C&color=222222&logo=C&logoColor=A8B9CC&label=)
[CSharp-shield]: (https://img.shields.io/static/v1?style=for-the-badge&message=C+Sharp&color=512BD4&logo=C+Sharp&logoColor=FFFFFF&label=)
[CSharp-url]: (https://dotnet.microsoft.com/en-us/languages/csharp)
[Cplusplus-shield]: (https://img.shields.io/static/v1?style=for-the-badge&message=C%2B%2B&color=00599C&logo=C%2B%2B&logoColor=FFFFFF&label=)
[Cplusplus-url]: (https://cplusplus.com/)
