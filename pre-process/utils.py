import os
import getpass
import shutil

def ensure_file_permissions(file_path):
    """
    Checks if the permissions of the given file are restricted, and if so,
    changes them to 777 (read, write, and execute for everyone).
    """
    # Get current file permissions
    current_permissions = oct(os.stat(file_path).st_mode)[-3:]

    # Check if the permissions are restricted (less than 777)
    if current_permissions != "777":
        # Set the permissions to 777 (read, write, and execute for everyone)
        os.chmod(file_path, 0o777)
        print(f"Permissions for {file_path} were restricted. Changed to 777.")
    else:
        print(f"Permissions for {file_path} are already 777.")


def ensure_folder_permissions(folder):
    if os.path.exists(folder):
        # Change ownership to the current user
        os.system(f"sudo chown -R {getpass.getuser()}:{getpass.getuser()} {folder}")
        # Ensure write permissions
        os.chmod(folder, 0o777)
        print('Permissions changed to 777.')


def delete_folder(folder):
            """Deletes a folder if it exists."""
            if os.path.exists(folder):
                shutil.rmtree(folder)         