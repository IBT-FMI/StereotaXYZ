from stereotaxyz.skullsweep import *
import nibabel as nib
import numpy as np
import nibabel as nib
import numpy as np
from os import path

def make_nii(df_slice,
	template='/home/chymera/ni_data/templates/DSURQEc_200micron_average.nii',
	):
	"""Create a NIfTI based on a dataframe containing bregma-relative skullsweep points, and a bregma-origin template.
	"""
	template = nib.load(path.abspath(path.expanduser(template)))
	affine = template.affine
	data = np.zeros(shape=template.shape)
	for ix, point in df_slice.iterrows():
		try:
			x = point['posteroanterior']
		except KeyError:
			try:
				x = -point['anteroposterior']
			except KeyError:
				x = 0
		try:
			y = point['leftright']
		except KeyError:
			try:
				y = -point['rightleft']
			except KeyError:
				y = 0
		try:
			z = point['inferosuperior']
		except KeyError:
			try:
				z = -point['superoinferior']
			except KeyError:
				z = 0
		new_y = (-y-affine[0,3])/affine[0,0]
		new_y = int(round(new_y))
		new_x = (x-affine[1,3])/affine[1,1]
		new_x = int(round(new_x))
		new_z = (z-affine[2,3])/affine[2,2]
		new_z = int(round(new_z))
		data[new_y,new_x,new_z] = 1

	new_image = nib.Nifti1Image(data, affine=affine)
	return new_image


