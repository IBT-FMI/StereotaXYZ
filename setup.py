from setuptools import setup, find_packages

setup(
	name="stereotaxyz",
	version="",
	description = "Toolkit for the Empirical Design of Stereotactic Brain Implants",
	author = "Horea Christian",
	author_email = "horea.christ@yandex.com",
	url = "https://github.com/IBT-FMI/stereotaxyz",
	keywords = ["implant", "stereotactic", "lambda", "bregma", "surgery", 'mouse', 'rat'],
	classifiers = [],
	install_requires = [],
	provides = ["stereotaxyz"],
	packages = [
		"stereotaxyz",
		"stereotaxyz.skullsweep",
		],
	include_package_data=True,
	entry_points = {'console_scripts' : \
			['SAMRI = stereotaxyz.cli:main']
		}
	)
