# coding: utf-8
__author__ = "Horea Christian"

import argh
from stereotaxyz.workflows import plot2d, plot3d, text
from stereotaxyz.registration import register

def main():
	argh.dispatch_commands([register, plot2d, plot3d, text])

if __name__ == '__main__':
	main()
