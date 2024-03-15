import os
import shutil


def list_files_in_folder(folder_path):
    """
  List all files in the specified folder.

  Args:
  - folder_path (str): The path to the folder.

  Returns:
  - files_list (list): A list of filenames in the folder.
  """
    files_list = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            files_list.append(file_name)
    return files_list


def delete_files_in_folder(folder_path):
    """
    Delete all files in the specified folder.

    Args:
    - folder_path (str): The path to the folder.

    Returns:
    - None
    """
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_path.endswith('.ppm'):
            os.remove(file_path)
            print(f"Deleted file: {file_name}")


def copy_image(image_path, destination_folder):
    """
  Copy an image file from the source path to the destination folder.

  Args:
  - image_path (str): The path to the image file.
  - destination_folder (str): The path to the destination folder.

  Returns:
  - destination_path (str): The path to the copied image file in the destination folder.
  """
    if os.path.isfile(image_path):
        image_name = os.path.basename(image_path)
        destination_path = os.path.join(destination_folder, image_name)
        shutil.copyfile(image_path, destination_path)
        print(f"Image '{image_name}' copied successfully to '{destination_folder}'.")
        return destination_path
    else:
        print("Error: The specified image path does not exist.")
        return None


def create_folder(folder_path):
    """
  Create a folder/directory at the specified path.

  Args:
  - folder_path (str): The path to the folder to be created.

  Returns:
  - None
  """
    try:
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    except OSError as error:
        print(f"Failed to create folder '{folder_path}': {error}")


def getImageSelection(path, imageStart, imageEnd):
    return list_files_in_folder(path)[imageStart:imageEnd]


def addExtrinsicImages(path):
    destinationPath = 'C:/Users/4dviz/PycharmProjects/pythonProject/lorl/S00_Demo_Session/S00_Calibration/extrinsics/'
    delete_files_in_folder(destinationPath + "ext_cam1_img")
    delete_files_in_folder(destinationPath + "ext_cam2_img")
    delete_files_in_folder(destinationPath + "ext_cam3_img")

    v = path + 'v/' + getImageSelection(path + 'v/', 0, 1)[0]
    m = path + 'm/' + getImageSelection(path + 'm/', 0, 1)[0]
    h = path + 'h/' + getImageSelection(path + 'h/', 0, 1)[0]

    copy_image(v, destinationPath + "ext_cam1_img")
    copy_image(m, destinationPath + "ext_cam2_img")
    copy_image(h, destinationPath + "ext_cam3_img")


def addIntrinsicsImages(start, end):
    destinationPath = 'C:/Users/4dviz/PycharmProjects/pythonProject/lorl/S00_Demo_Session/S00_Calibration/intrinsics/'
    delete_files_in_folder(destinationPath + "int_cam1_img")
    delete_files_in_folder(destinationPath + "int_cam2_img")
    delete_files_in_folder(destinationPath + "int_cam3_img")

    source_directory = r'C:\Users\4dviz\Videos\bch\h'  # Change this to your source directory
    target_directory = (r'C:\Users\4dviz\PycharmProjects\pythonProject\lorl\S00_Demo_Session\S00_Calibration'
                        r'\intrinsics\int_cam1_img')  # Change this to your target directory
    copy_every_n_picture(source_directory, target_directory, start, end)

    source_directory = r'C:\Users\4dviz\Videos\bch\m'  # Change this to your source directory
    target_directory = (r'C:\Users\4dviz\PycharmProjects\pythonProject\lorl\S00_Demo_Session\S00_Calibration'
                        r'\intrinsics\int_cam2_img')  # Change this to your target directory
    copy_every_n_picture(source_directory, target_directory, start, end)

    source_directory = r'C:\Users\4dviz\Videos\bch\v'  # Change this to your source directory
    target_directory = (r'C:\Users\4dviz\PycharmProjects\pythonProject\lorl\S00_Demo_Session\S00_Calibration'
                        r'\intrinsics\int_cam3_img')  # Change this to your target directory
    copy_every_n_picture(source_directory, target_directory, start, end)


def copy_every_n_picture(source_dir, target_dir, start, end, n=50):
    """
  Copies every nth picture from the source directory to the target directory.

  :param source_dir: The directory to search for pictures.
  :param target_dir: The directory where pictures will be copied.
  :param n: Copy every nth picture. Default is 100.
  """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Supported image extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ppm')

    # Initialize a counter to keep track of every nth picture
    counter = 0

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(image_extensions):
                counter += 1
                if counter % n == 0 and start < counter < end:
                    source_file_path = os.path.join(root, file)
                    target_file_path = os.path.join(target_dir, file)
                    shutil.copy2(source_file_path, target_file_path)
                    print(f"Copied {file} to {target_dir}")


def runOpenPose(cam, imageStart, imageEnd):
    # Openpose
    import subprocess

    jsonPath = ("C:/Users/4dviz/PycharmProjects/pythonProject/lorl/S00_Demo_Session/S00_P00_Participant"
                "/S00_P00_T01_BalancingTrial/pose/")

    if cam == "v":
        jsonPath += "cam1_json"
    elif cam == "m":
        jsonPath += "cam2_json"
    elif cam == "h":
        jsonPath += "cam3_json"
    else:
        return "assign cam"

    delete_files_in_folder(jsonPath)

    imagesPath = f"C:/Users/4dviz/Videos/bch/{cam}"  # change to openpose image path

    openPoseImages = list_files_in_folder(imagesPath)[imageStart:imageEnd]
    destination_folder = f"C:/Users/4dviz/Videos/openpose/{cam}"
    create_folder(destination_folder)

    for image in openPoseImages:
        copy_image(f"{imagesPath}/{image}", destination_folder)

    command = (f"C:/Users/4dviz/Bachelor050/openpose/bin/OpenPoseDemo.exe  --model_pose BODY_25B --net_resolution "
               f"1280x1024  --image_dir {destination_folder}  --write_json {jsonPath}")  # Change to openpose directory
    # Running the 'dir' command
    result = subprocess.run(command, shell=True, text=True, capture_output=True,
                            cwd="C:/Users/4dviz/Bachelor050/openpose/")

    # Printing the output
    print("Output:\n", result.stdout)
    print("Errors:\n", result.stderr)
