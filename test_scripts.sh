stereotaxyz text example_data/skull_6465.csv DR -y 45 &&
stereotaxyz plot2d example_data/skull_6465.csv DR -a 45 --save-as 6465_2d.png &&
stereotaxyz plot3d example_data/skull_6465.csv DR -y 45 --save-as 6465_3d.png &&
stereotaxyz text  example_data/skull_6469.csv DR -y 45 --reference "lambda skull" &&
stereotaxyz plot2d example_data/skull_6469.csv DR -a 45 --reference "bregma skull" --save-as 6469_2d.png &&
stereotaxyz plot3d example_data/skull_6469.csv DR -y 45 --reference "bregma skull" --save-as 6469_3d.png
