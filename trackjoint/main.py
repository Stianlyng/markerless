import os
import toml
from trackjoint import fileHandler


def main_menu():
    print("1. View project parameters")
    print("2. Edit project parameters")
    print("3. Run workflow")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        view_project_parameters()
    elif choice == "2":
        edit_project_parameters()
    elif choice == "3":
        workflow()
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        main_menu()


def view_project_parameters():
    # Load the contents of the .toml file
    with open("Config.toml", "r") as f:
        config = toml.load(f)
    print(toml.dumps(config))


def edit_project_parameters():
    # Load the contents of the .toml file
    with open("Config.toml", "r") as f:
        config = toml.load(f)

    print("Current project parameters:")
    print(toml.dumps(config["project"]))

    parameter_to_edit = input("Enter the parameter you want to edit: ")

    if parameter_to_edit in config["project"]:
        new_value = input(f"Enter the new value for {parameter_to_edit}: ")
        config["project"][parameter_to_edit] = new_value

        # Write the modified contents back to the .toml file
        with open("Config.toml", "w") as f:
            toml.dump(config, f)

        print("Project parameter updated successfully.")
    else:
        print("Invalid parameter.")


def workflow():
    from Pose2Sim import Pose2Sim

    print("1. Run OpenPose")
    print("2. Run extrinsic")
    print("3. Run Intrinsics")
    print("4. Run All")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        fileHandler.runOpenPose("v", 4013, 4655)
        fileHandler.runOpenPose("m", 4013, 4655)
        fileHandler.runOpenPose("h", 4013, 4655)

    elif choice == "2":
        fileHandler.addIntrinsicsImages(0,4013)

    elif choice == "3":
        fileHandler.addExtrinsicsImages("C:/Users/4dviz/Videos/bak/")

    elif choice == "4":
        fileHandler.runOpenPose("v", 4013, 4655)
        fileHandler.runOpenPose("m", 4013, 4655)
        fileHandler.runOpenPose("h", 4013, 4655)

        fileHandler.addIntrinsicsImages(0, 4013)

        fileHandler.addExtrinsicsImages("C:/Users/4dviz/Videos/bak/")

    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        main_menu()

    # Calibration
    config_dict = toml.load('Config.toml')
    config_dict.get("project").update({"project_dir": "."})
    Pose2Sim.calibration(config_dict)

    # Balancing trial
    project_dir = os.path.join("S00_MotionTrackingData", "T00_JumpTrial")
    config_dict.get("project").update({"project_dir": project_dir})
    config_dict['filtering']['display_figures'] = False

    Pose2Sim.personAssociation(config_dict)
    Pose2Sim.triangulation(config_dict)
    Pose2Sim.filtering(config_dict)


if __name__ == "__main__":
    main_menu()
