from stereotaxyz.skullsweep import *

df = load_data('~/data/stereotactic/skull_6465.csv', origin='bregma')
ax = draw_anatomy(df)

implant(30,'VTA',df,ax,'#56B4E9','best')
implant(45,'VTA',df,ax,'#56B4E9','best')
implant(30,'DR',df,ax,'#E69F00','best')
implant(45,'DR',df,ax,'#E69F00','best')

plt.savefig('basic.png')

