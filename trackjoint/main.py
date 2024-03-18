import os
import subprocess
import toml
import fileHandler as fileHandler

def run_marker_detection(config):
    '''
    Checks the configuration to determine if marker detection should be executed.
    If so, runs the marker detection script with the configured images folder path.
    '''
    preprocessing_config = config.get('preprocessing', {})
    run_marker_detection = preprocessing_config.get('run_marker_detection', False)
    images_folder_path = preprocessing_config.get('images_folder_path', '')
    
    if run_marker_detection:
        script_path = 'Pose2Sim/MarkerDetection.py'  
        command = f'python {script_path} --folder_path "{images_folder_path}"'
        subprocess.run(command, shell=True, check=True)

def test_workflow():
  
  from Pose2Sim import Pose2Sim
  import Pose2Sim.MarkerDetection as markerDetection

  # Calibration
  config_dict = toml.load('Config.toml')
  
  markerDetection.run(config_dict)
  #Pose2Sim.test(config_dict)
  # runs the marker detection if set to true in the config
    #run_marker_detection(config_dict)

  config_dict.get("project").update({"project_dir":"."})
  Pose2Sim.calibration(config_dict)
  
  
  # Balancing trial
  project_dir = os.path.join("S00_MotionTrackingData","T00_JumpTrial")
  config_dict.get("project").update({"project_dir":project_dir})
  config_dict['filtering']['display_figures'] = False

  # Pose2Sim.poseEstimation(config_dict)
  # Pose2Sim.synchronization(config_dict)
  Pose2Sim.personAssociation(config_dict)
  Pose2Sim.triangulation(config_dict)
  Pose2Sim.filtering(config_dict)
  # Pose2Sim.kinematics(config_dict)


"""
fileHandler.runOpenPose("v",4013,4655)
fileHandler.runOpenPose("m",4013,4655)
fileHandler.runOpenPose("h",4013,4655)
"""

#fileHandler.addExtrinsicsImages("C:/Users/4dviz/Videos/bak/")
#fileHandler.addIntrinsicsImages(0,4013)
test_workflow()
