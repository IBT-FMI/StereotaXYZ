__author__ = "Horea Christian"

import argh
from stereotaxyz.workflows import plot2d, plot3d, text


def main():
	argh.dispatch_commands([plot2d, plot3d, text])

if __name__ == '__main__':
	main()
