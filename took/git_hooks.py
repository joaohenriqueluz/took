import os
import pkg_resources
import shutil

def init_git_hooks():
    """
    Initializes Git hooks by copying hook scripts into the .git/hooks directory.

    This function checks if the .git/hooks directory exists in the current working directory.
    If it does, it copies the predefined Git hook scripts from the package resources to this directory
    and sets their permissions to make them executable.

    Hook scripts copied:
    - pre-commit
    - post-commit
    - post-checkout
    - post-merge

    If the .git directory is not found, a message is printed and no hooks are installed.

    Raises:
        FileNotFoundError: If the hook script resource files cannot be found in the package.
    """
    git_dir = os.path.join(os.getcwd(), ".git", "hooks")
    print(git_dir)
    if not os.path.exists(git_dir):
        print("No .git directory found. Git hooks will not be installed.")
        return

    hook_files = ["pre-commit", "post-commit", "post-checkout", "post-merge"]
    for hook_name in hook_files:
        resource_name = f"resources/hooks/{hook_name}.sh"
        resource_path = pkg_resources.resource_filename('took', resource_name)
        dest_path = os.path.join(git_dir, hook_name)
        print(dest_path)
        # Copy the hook script to the .git/hooks directory
        shutil.copyfile(resource_path, dest_path)

        # Make the hook script executable
        os.chmod(dest_path, 0o775)

    print("Git hooks have been initialized.")
