from classes.PC import PC
from classes.PC_UTILS import PC_UTILS
import math

def open_save(input_path, output_path):
    pc_data = PC()
    pc_data.open(input_path, verbose = True)
    pc_data.save(output_path, verbose = True)

def shift_rotate(input_path, output_path, shift_x, shift_y, shift_z, rotation_angle):
    pc_data = PC()
    pc_data.open(input_path, verbose = True)
    pc_data.points = PC_UTILS.shift(pc_data.points, shift_x, shift_y, shift_z)
    pc_data.points = PC_UTILS.rotate_points(pc_data.points, rotation_angle)
    pc_data.save(output_path, verbose = True)

if __name__ == "__main__" :
    input_paths = ["tree_0149.las", "tree_0149.laz", "tree_0149.pcd", "tree_0149.csv",
                "01_05.las", "01_05.laz", "01_05.pcd", "01_05.csv", "input.h5"]
    output_paths = ["output.las", "output.laz", "output.pcd", "output.csv"]

    for input_path in input_paths:
        for output_path in output_paths:
            open_save("input/" + input_path, "output/" + input_path.split(".")[-1] + "_" + output_path)
            print()
        print("------------------------------------")

    # shift_x, shift_y, shift_z = 200, 100, 50
    # rotation_angle = math.pi
    # shift_rotate(input_path, output_path_las, shift_x, shift_y, shift_z, rotation_angle)