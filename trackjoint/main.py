import os
import toml
import fileHandler


def main_menu():
    print("1. View project parameters")
    print("2. Edit project parameters")
    print("3. Run workflow")
    print("4. Exit")

    choice = input("Enter your choice: ")

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
    with open("Config.toml", "r") as f:
        config = toml.load(f)
    print(toml.dumps(config))
    main_menu()


def edit_project_parameters():
    with open("Config.toml", "r") as f:
        config = toml.load(f)

    while True:
        print("Do you want to change: ")
        print("1. Change extrinsic")
        print("2. Change intrinsic")
        print("3. Change Both")
        print("4. exit")
        choice = input("Enter your choice: ")

        if choice == '4':
            print("Exiting...")
            break

        if choice == "1":
            config['calibration']['calculate']['extrinsics']['calculate_extrinsics'] = not \
                config['calibration']['calculate']['extrinsics']['calculate_extrinsics']
            print("Value of 'overwrite_intrinsics' changed to:",
                  config['calibration']['calculate']['extrinsics']['calculate_extrinsics'])

        elif choice == "2":
            config['calibration']['calculate']['intrinsics']['overwrite_intrinsics'] = not \
                config['calibration']['calculate']['intrinsics']['overwrite_intrinsics']
            print("Value of 'overwrite_intrinsics' changed to:",
                  config['calibration']['calculate']['extrinsics']['overwrite_intrinsics'])

        elif choice == "3":
            config['calibration']['calculate']['intrinsics']['overwrite_intrinsics'] = not \
                config['calibration']['calculate']['intrinsics']['overwrite_intrinsics']

            config['calibration']['calculate']['extrinsics']['calculate_extrinsics'] = not \
                config['calibration']['calculate']['extrinsics']['calculate_extrinsics']
            print("Value of 'overwrite_intrinsics' changed to:",
                  config['calibration']['calculate'])

        with open("Config.toml", "w") as f:
            toml.dump(config, f)


def workflow():
    from Pose2Sim import Pose2Sim

    print("1. Run OpenPose")
    print("2. Run Intrinsics")
    print("3. Run Extrinsic")
    print("4. Run All")

    choice = input("Enter your choice: ")

    if choice == "1":
        fileHandler.runOpenPose("v", 4013, 4655)
        fileHandler.runOpenPose("m", 4013, 4655)
        fileHandler.runOpenPose("h", 4013, 4655)

    elif choice == "2":
        fileHandler.addIntrinsicsImages(0, 4013)

    elif choice == "3":
        fileHandler.addExtrinsicImages(
            "C:/Users/4dviz/Videos/bak/")  # change to accordingly to where the recordings are

    elif choice == "4":
        fileHandler.runOpenPose("v", 4013, 4655)
        fileHandler.runOpenPose("m", 4013, 4655)
        fileHandler.runOpenPose("h", 4013, 4655)

        fileHandler.addIntrinsicsImages(0, 4013)

        fileHandler.addExtrinsicImages(
            "C:/Users/4dviz/Videos/bak/")  # change to accordingly to where the recordings are

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
