import hashlib
import multiprocessing
import nipype.interfaces.ants as ants
import os

N_PROCS=max(multiprocessing.cpu_count()-2,2)
PHASES = {
	"rigid":{
		"transforms":"Rigid",
		# 0.05 is better than 0.1
		"transform_parameters":(0.05,),
		"number_of_iterations":[20,40,60],
		"metric":"GC",
		"metric_weight":1.0,
		"radius_or_number_of_bins":1,
		"sampling_strategy":'Random',
		"sampling_percentage":0.2,
		"convergence_threshold":1.e-8,
		"convergence_window_size":10,
		"smoothing_sigmas":[2,1,0],
		"sigma_units":"vox",
		"shrink_factors":[6,2,1],
		"use_estimate_learning_rate_once":False,
		"use_histogram_matching":True,
		},
	"rigid_multimetric":{
		"transforms":"Rigid",
		"transform_parameters":(0.1,),
		"number_of_iterations":[30,50,40],
		"metric":["CC", 'GC'],
		"metric_weight":[0.5,0.5],
		"radius_or_number_of_bins":[4, 1],
		"sampling_strategy":["Random","Random"],
		"sampling_percentage":[0.2,1.],
		"convergence_threshold":1.e-8,
		"convergence_window_size":10,
		"smoothing_sigmas":[2,1,0],
		"sigma_units":"vox",
		"shrink_factors":[6,2,1],
		"use_estimate_learning_rate_once":False,
		"use_histogram_matching":True,
		},
	"affine":{
		"transforms":"Affine",
		"transform_parameters":(0.1,),
		"number_of_iterations":[200,100],
		"metric":"MI",
		"metric_weight":1,
		"radius_or_number_of_bins":8,
		"sampling_strategy":None,
		"sampling_percentage":0.3,
		"convergence_threshold":1.e-11,
		"convergence_window_size":30,
		"smoothing_sigmas":[1,0],
		"sigma_units":"vox",
		"shrink_factors":[2,1],
		"use_estimate_learning_rate_once":False,
		"use_histogram_matching":True,
		},
	"syn":{
		"transforms":"SyN",
		"transform_parameters":(0.1, 2.0, 0.2),
		"number_of_iterations":[500,250],
		"metric":"MI",
		"metric_weight":1,
		"radius_or_number_of_bins":16,
		"sampling_strategy":None,
		"sampling_percentage":0.3,
		"convergence_threshold":1.e-32,
		"convergence_window_size":30,
		"smoothing_sigmas":[1,0],
		"sigma_units":"vox",
		"shrink_factors":[1,1],
		"use_estimate_learning_rate_once":False,
		"use_histogram_matching":True,
		},
	}


def mri_anatomy(anatomy,
	template="~/ni_data/templates/DSURQEc_40micron_average.nii",
	verbose=False,
	phases=['rigid'],
	phase_dictionary = PHASES,
	mask='',
	num_threads=N_PROCS,
	out_file='',
	force_rewrite=False,
	record=True,
	):

	anatomy = os.path.abspath(os.path.expanduser(anatomy))
	template = os.path.abspath(os.path.expanduser(template))
	if mask:
		mask = os.path.abspath(os.path.expanduser(mask))

	# Create unique-ish temporal directory for file registration.
	hasher = hashlib.sha256()
	blocksize = hasher.block_size
	anatomy_file = open(anatomy, "rb")
	buf = anatomy_file.read(blocksize*20)
	hasher.update(buf)
	if record:
		try:
			hasher.update(repr(phase_dictionary))
		except TypeError:
			hasher.update(repr(phase_dictionary).encode('utf-8'))

	registration_dir = hasher.hexdigest()[:16]

	workdir = '/tmp/stereotaxyz/{}'.format(registration_dir)
	try:
		os.makedirs(workdir)
	except OSError:
		if os.path.isdir(workdir):
			pass
		else:
			raise
	if out_file:
		out_file = os.path.abspath(os.path.expanduser(out_file))
	else:
		out_file = '{}/res.nii.gz'.format(workdir)

	biascorrect_out_file = '{}/n4.nii.gz'.format(workdir)

	if os.path.isfile(biascorrect_out_file) and not force_rewrite:
		if verbose:
			print('Biascorrect output found.')
	else:
		if os.path.isfile(biascorrect_out_file) and force_rewrite:
			os.remove(biascorrect_out_file)
		biascorrect = ants.N4BiasFieldCorrection()
		biascorrect.inputs.bspline_fitting_distance = 2
		biascorrect.inputs.bspline_order = 3
		biascorrect.inputs.dimension = 3
		biascorrect.inputs.input_image = anatomy
		biascorrect.inputs.n_iterations = [100,50,20,12]
		biascorrect.inputs.convergence_threshold = 1e-10
		biascorrect.inputs.output_image = biascorrect_out_file
		biascorrect.inputs.shrink_factor = 2
		biascorrect.inputs.num_threads = num_threads
		if verbose:
			biascorrect.inputs.terminal_output = 'stream'
			print('Running:\n{}'.format(biascorrect.cmdline))
		if record:
			biascorrect_record_name = biascorrect_out_file.split('.')[0]+'_command.txt'
			with open(biascorrect_record_name, "w") as text_file:
				    text_file.write(biascorrect.cmdline)
		biascorrect_res = biascorrect.run()

	if os.path.isfile(out_file) and not force_rewrite:
		pass
	else:
		if os.path.isfile(out_file) and force_rewrite:
			os.remove(out_file)
		parameters = [phase_dictionary[phase] for phase in phases]
		registration = ants.Registration()
		registration.inputs.fixed_image = template
		registration.inputs.moving_image = biascorrect_out_file
		registration.inputs.output_transform_prefix = "output_"
		registration.inputs.transforms = [i["transforms"] for i in parameters] ##
		registration.inputs.transform_parameters = [i["transform_parameters"] for i in parameters] ##
		registration.inputs.number_of_iterations = [i["number_of_iterations"] for i in parameters] #
		registration.inputs.dimension = 3
		registration.inputs.write_composite_transform = True
		registration.inputs.collapse_output_transforms = True
		registration.inputs.initial_moving_transform_com = True
		registration.inputs.metric = [i["metric"] for i in parameters]
		registration.inputs.metric_weight = [i["metric_weight"] for i in parameters]
		registration.inputs.radius_or_number_of_bins = [i["radius_or_number_of_bins"] for i in parameters]
		registration.inputs.sampling_strategy = [i["sampling_strategy"] for i in parameters]
		registration.inputs.sampling_percentage = [i["sampling_percentage"] for i in parameters]
		registration.inputs.convergence_threshold = [i["convergence_threshold"] for i in parameters]
		registration.inputs.convergence_window_size = [i["convergence_window_size"] for i in parameters]
		registration.inputs.smoothing_sigmas = [i["smoothing_sigmas"] for i in parameters]
		registration.inputs.sigma_units = [i["sigma_units"] for i in parameters]
		registration.inputs.shrink_factors = [i["shrink_factors"] for i in parameters]
		registration.inputs.use_estimate_learning_rate_once = [i["use_estimate_learning_rate_once"] for i in parameters]
		registration.inputs.use_histogram_matching = [i["use_histogram_matching"] for i in parameters]
		registration.inputs.winsorize_lower_quantile = 0.05
		registration.inputs.winsorize_upper_quantile = 0.95
		registration.inputs.args = '--float'
		if mask:
			registration.inputs.fixed_image_masks = [mask]
		registration.inputs.num_threads = num_threads
		registration.inputs.output_warped_image = out_file
		if verbose:
			registration.inputs.terminal_output = 'stream'
			print('Running:\n{}'.format(registration.cmdline))
		if record:
			registration_record_name = out_file.split('.')[0]+'_command.txt'
			with open(registration_record_name, "w") as text_file:
				    text_file.write(registration.cmdline)
		registration_res = registration.run()

