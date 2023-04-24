# TP noté - Synthèse d'images 2022/2023

## Dependencies

- Python 3.9+
- OpenCV 4.7+
- CMake 3.21+

## How to run
- In CLion : 
    - To run the program :
      - Load CMakeLists.txt
      - Click on run to launch `synthese`
    - To run test :
      - Add a configuration to run `Google_Tests_run`


- In terminal :
    - `mkdir build && cd build`
    - `cmake ..`
    - `make`
    - `./synthese`
## Folder structure
- `.cpp` in `src/customs`
- `.h` in `include/customs`
- Script Python to resize the image in `resize_script`
- CMake at `.CMakeLists.txt`

## What is done

- Code totalement orienté objet
  -  Classe abstraite : Drawable
  - Classes pour tous les éléments nécessaires au rendu
    - Point d'intersection, Lumières, Rayons, etc.
- Plusieurs sources de lumière :
  - Spot (panneau)
  - Ponctuelle
- Rendu d'une scene 3D avec les formes suivantes :
  - Sphere
  - Plan
  - Panneau
- Ombres
- Lissage de l'image en générant plusieurs rayons par pixel : on génère une image plus grande, puis on la réduit à l'aide d'un script Python avec OpenCV

## Render examples
### Render 1
Sol bleu (plan), panneau jaune en collision avec une sphère rouge,  une lumière spot blanche.

<img height=256 src="render_example1.jpg" alt="Render example 1"></a>

### Render 2
Sol rouge (plan), sphère jaune,  une lumière ponctuelle blanche.

<img height=256 src="render_example2.jpg" alt="Render example 2"></a>

## ✍️ Authors

- [Julien Ballouard](https://forge.univ-lyon1.fr/p2006861) : p2006861
- [Farès SIONI](https://forge.univ-lyon1.fr/p1907037) : p1907037
