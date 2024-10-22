import os
import shutil

def main():
    copy_src_dir_to_dest_dir("static", "public")


def copy_src_dir_to_dest_dir(src_dir, dest_dir):
    # get the current project location
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    # go back one directory to get the root directory
    curr_proj_loc = os.path.dirname(curr_dir)
    
    # delete contents of dest_dir
    full_dest_dir = os.path.join(curr_proj_loc, dest_dir)
    if os.path.exists(full_dest_dir):
        shutil.rmtree(full_dest_dir)
    
    full_src_dir = os.path.join(curr_proj_loc, src_dir)
    
    # check if src_dir exists
    if not os.path.exists(full_src_dir):
        print(f"{src_dir} does not exist")
        return
    
    # copy src_dir to dest_dir with detailed logging
    shutil.copytree(full_src_dir, full_dest_dir, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
