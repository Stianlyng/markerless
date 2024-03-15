########################################################################################################################
##                                           README FOR IMPORTANT PARAMETERS                                          ##
########################################################################################################################

This program consists of a Config.toml file that controls most of the functions and accessibility of the program.
It's therefore important that this file is read thoroughly so that the wanted result is archived. This txt file will
therefore go through the most important variables that one need to change accordingly to the images and formats used.
To begin with, it's important to mention that missing parameters will be used from the Config.toml
file on the level above.


Variables::
    calibration_type = 'calculate' # 'convert' or 'calculate'

    You can either convert or calculate the calibration from scratch by using a checkerboard or aruco markers.
    If you use an already calibrated system such as qualisys or optitrack you can put the variable to convert.
    convert_from = 'qualisys' # 'qualisys', 'optitrack'



    Intrinsics are important variables that need to be calculated once pr camera setup
    overwrite_intrinsics = true

    will show you the intrinsic found on the image
    show_detection_intrinsics = false # true or false (lowercase)

    using a checkerboard for calculation the intrinsics, you need to state the size of the board and the square size
    intrinsics_corners_nb = [9,13] -> H, W
    intrinsics_square_size = 30 -> mm



    Calculating the extrinsic values needs to be done every session. You can either use a board placed on the ground,
    or use points with known distance and height from each other (scene).
    calculate_extrinsics = true # true or false (lowercase)

    - Board should be large enough to be detected when laid on the floor. Not recommended.
    - Scene involves manually clicking any point of know coordinates on a scene. Usually more accurate if points are spread out.

    extrinsics_method = 'board'  'board', 'scene'
    extrinsics_extension = 'ppm' any video or image extension

    if you use a board to calculate the extrinsic values, you need to set the correct values of the board
    extrinsics_corners_nb = [11,10] [H, W]
    extrinsics_square_size = 170 mm

    exentric calculation with scene need at least 5 points, but more = better.
    object_coords_3d = [[0.0,    0.0,     0.0],   # 0
                        [0.0,    0.50,     0.0],  # 1
                        [0.0,    1.0,     0.0],   # 2
                        [0.0,    1.0,     0.515], # 3
                        [0.0,    1.0,     1.002], # 4
                        [-1.50,  0.0,     0.0],   # 5
                        [-1.0,   0.0,     0.0],   # 6
                        [-0.40,  0.0,     0.0],   # 7
                        [0.405,  0.0,     0.0],   # 8
                        [1.005,  0.0,     0.0],   # 9
                        [1.505,  0.0,     0.0]]   # 10




    If you are going to use openpose, you need to set the wanted pose model when running the program code.
    - BODY_25B is the best and most accurate, but takes a lot of time and cpu.
    - BODY_25 is relatively fast and accurate and should be the default when testing and trying the code.

    pose_framework = 'openpose'
    pose_model = 'BODY_25B' #With openpose: BODY_25B, BODY_25, BODY_135, COCO, MPII,



    When the openpose is finished running, the json files are run through a filter that smoothens out the coordinates.
    for this project the bachelor group used butterworth lower pas 4dim filter.

    type = 'butterworth' # butterworth, kalman, gaussian, LOESS, median, butterworth_on_speed

If this short file didn't go through the necessary understanding and definitions, one can also visit the main page
of the original code here - https://github.com/perfanalytics/pose2sim