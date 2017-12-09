import matplotlib.pyplot as plt
from os import path
from stereotaxyz import plotting, skullsweep

data_dir = path.join(path.dirname(path.realpath(__file__)),"../../example_data")
data_file = path.join(data_dir,'skull_6465.csv')
df = skullsweep.load_data(data_file, ultimate_reference='bregma')

t, leftright, posteroanterior, inferosuperior, df = skullsweep.implant_by_angle('VTA', df, yz_angle=45.)
plotting.yz(df, 'VTA', [posteroanterior, inferosuperior], 45., color_projection='c', save_as='basic2d.png')
