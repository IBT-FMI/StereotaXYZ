from stereotaxyz.skullsweep import *

data_dir = path.join(path.dirname(path.realpath(__file__)),"../../example_data")
data_file = path.join(data_dir,'skull_6465.csv')
df = load_data(data_file, ultimate_reference='bregma')
ax = draw_anatomy(df)

implant(35,'VTA',df,ax,'#56B4ED','best')
implant(45,'VTA',df,ax,'#5FCAE2','best')
implant(30,'DR',df,ax,'#EA9F00','best')
implant(40,'DR',df,ax,'#E0B910','best')

plt.savefig('basic.png')

