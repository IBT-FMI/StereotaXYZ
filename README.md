# StereotaXYZ
[![Build Status](https://travis-ci.org/IBT-FMI/StereotaXYZ.svg?branch=master)](https://travis-ci.org/IBT-FMI/StereotaXYZ)

StereotaXYZ - pronounced "stereo-tack-seas" - aids in the empirical design and per-animal customization of stereotactically targeted procedures.
This is particularly relevant when performing interventions at odd angles through high skull shape variability areas (e.g. the occipital or nasal bone plates) or areas which are difficult to access e.g. due to the proximity of tough or vital tissue.

In addition to implant design functionality, StereotaXYZ ships with a plotting utility, which allows visual inspection of implant designs with.

## Usage Examples

The following examples assume that in addition to an installation for StereotaXYZ, the example data from our repository is also available on your machine.
You can make it available under the expected path of the examples, as follows:

```
cd
mkdir src
cd src
git clone https://github.com/IBT-FMI/StereotaXYZ.git
```

### 3D Auto-Sliced View with Anatomical Background

StereotaXYZ can produce volumetric data representations of all elements of interest, registered to the coordinate space of a template.
Angles can be specified in 3D - meaning that the elements of interest are not constrained to a specific YZ or XZ plane.
In this case, YZ and XZ angles have to be unambiguously specified.

This full 3D-aware visualization can be obtained from the `stereotaxyz plot3d` command line interface (internally calling the `stereotaxyz.plotting.xyz()` function).
A basic usage example of this function is:

```
stereotaxyz plot3d ~/src/stereotaxyz/example_data/skull_6465.csv DR -y 45 --save-as plot3d.png
```

Which produces the following image (incidentally, all elements here lie in the same YZ-plane, but this is not required):

![Plot 3D](http://www.chymera.eu/img/examples/stereotaxyz/plot3d.png "Plot 3D")

### 2D (Constant-X) View with Clear Grid Background

A simple 2D visualization of the elements of interest can be created with the `stereotaxyz plot2d` command line interface (internally calling the `stereotaxyz.plotting.yz()` function).
A basic usage example of this function is :

```
stereotaxyz plot2d ~/src/stereotaxyz/example_data/skull_6465.csv DR -a 45 --save-as plot2d.png
```

Which produces the following image (here, all elements are required to lie in the same YZ-plane):

![Plot 2D](http://www.chymera.eu/img/examples/stereotaxyz/plot2d.png "Plot 2D")

### Text Summary

In case no visualization is needed, the computed coordinates for reaching a defined target at a defined angle can be outputted as text.
This is done via the `stereotaxyz text` command line interface.
A basic usage example of this function is:

```
stereotaxyz text ~/src/stereotaxyz/example_data/skull_6465.csv DR -y 45
```

Which returns the following text to the terminal:

```
You have selected:

	Target: “DR”
		LeftRight(bregma): 		0.00
		PosteroAnterior(bregma): 	-4.50
		InferoSuperior(bregma): 	-3.15
	Entry Angles:
		XZ(from Posteroanterior axis): 	0°
		YZ(from Posteroanterior axis): 	45°

Given your skull points, you can best reach the target at the desired angle with:

	Icision Site:
		LeftRight(bregma): 		0.00
		PosteroAnterior(bregma): 	-7.18
		InferoSuperior(bregma): 	-0.47
	Insertion Length: 3.79mm
```

##Getting Started

To use the software, after [installing it](#installation), you will need to:

* Create a “Skullsweep” file analogous to the [example file](example_data/skull_6465.csv) distributed with the software.
* Choose a reference point (most commonly bregma) for all your measurements; lambda can also be used as a reference, but if you use it, be sure to specify lambda's cordinates relative to bregma (as we do in the example file).
* Fill in skullsweep point coordinates (best recorded by lowering a thin pipette or stylus until it makes contact with a properly restrained and positioned animal's skull).
* Enter the coordinates for any targets you might want to reach; these are best extracted from an atlas or a preliminary MRI recording of the animal.
* Run any of our [command line interfaces](#usage-examples), specifying the desired target and the desired angle of entry.

## Installation

### Gentoo Linux
StereotaXYZ is distributed with a [.gentoo](.gentoo) specification installation instruction.
If using a Gentoo system, you can simply clone this overlay, and use the associated script to install the software, and automatically handle all of its dependencies.
As root, run:

````
git clone git@github.com:IBT-FMI/StereotaXYZ.git
cd StereotaXYZ/.gentoo
./install.sh
````

Non-live versons of this package will be available for Gentoo via the [Science Overlay](https://github.com/gentoo/sci) as they are released.

### Python Package Manager (Users)
Python's `setuptools` allows you to install Python packages independently of your distribution (or operating system, even).
This approach cannot manage any of our numerous non-Python dependencies (by design) and at the moment will not even manage Python dependencies;
as such, given any other alternative, **we do not recommend this approach**:

````
git clone git@github.com:IBT-FMI/StereotaXYZ.git
cd StereotaXYZ
python setup.py install --user
````

If you are getting a `Permission denied (publickey)` error upon trying to clone, you can either:

* [Add an SSH key](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) to your GitHub account.
* Pull via the HTTPS link `git clone https://github.com/IBT-FMI/StereotaXYZ.git`.

### Python Package Manager (Developers)
Python's `setuptools` allows you to install Python packages independently of your distribution (or operating system, even);
it also allows you to install a "live" version of the package - dynamically linking back to the source code.
This permits you to test code (with real module functionality) as you develop it.
This method is sub-par for dependency management (see above notice), but - as a developer - you should be able to manually ensure that your package manager provides the needed packages.

````
git clone git@github.com:IBT-FMI/StereotaXYZ.git
cd StereotaXYZ
mkdir ~/.python_develop
echo "export PYTHONPATH=\$HOME/.python_develop:\$PYTHONPATH" >> ~/.bashrc
echo "export PATH=\$HOME/.python_develop:\$PATH" >> ~/.bashrc
source ~/.bashrc
python setup.py develop --install-dir ~/.python_develop/
````

If you are getting a `Permission denied (publickey)` error upon trying to clone, you can either:

* [Add an SSH key](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) to your GitHub account.
* Pull via the HTTPS link `git clone https://github.com/IBT-FMI/StereotaXYZ.git`.

## Dependencies:

To install the software you will need to have the following packages available on your system.

* [argh](https://github.com/neithere/argh)
* [Matplotlib](https://matplotlib.org/)
* [NiBabel](http://nipy.org/nibabel/) (optional)
* [NiLearn](http://nilearn.github.io/) (optional)
* [NumPy](http://www.numpy.org/)
* [pandas](http://pandas.pydata.org/)

This is handled automatically if you install the software via a package manager (e.g. Gentoo's Portage) - if not, you will have to ensure that these packages are available manually.
If you try to run the software without having the dependencies on your system, you will get `ImportError`s letting you know which package is missing.


