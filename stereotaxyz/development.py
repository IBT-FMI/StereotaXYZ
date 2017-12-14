import matplotlib.pyplot as plt
from stereotaxyz import skullsweep
from stereotaxyz import plotting
from nilearn.plotting import plot_stat_map, plot_roi, plot_anat
from os import path
import matplotlib

data_dir = path.join(path.dirname(path.realpath(__file__)),"../example_data")
data_file = path.join(data_dir,'skull_6465.csv')
df = skullsweep.load_data(data_file)

