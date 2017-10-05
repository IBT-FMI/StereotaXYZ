# StereotaXYZ
[![Build Status](https://travis-ci.org/IBT-FMI/StereotaXYZ.svg?branch=master)](https://travis-ci.org/IBT-FMI/StereotaXYZ)

StereotaXYZ - pronounced "stereo-tack-seas" - aids in the empirical design or custom per-animal targeting of stereotactic procedures.
This is particularly relevant for performing interventions through high skull shape variability areas (e.g. the occipital or nasal bone plates) or areas which are difficult to access e.g. due to the proximity of tough or vital tissue.

## Installation

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

* [argh](https://github.com/neithere/argh) - in Portage as dev-python/argh
* [Matplotlib](https://matplotlib.org/) - in Portage as dev-python/matplotlib
* [NumPy](http://www.numpy.org/) - in Portage as dev-python/numpy
* [pandas](http://pandas.pydata.org/) - in Portage as dev-python/pandas
