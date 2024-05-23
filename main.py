from classes.PC import PC
from classes.PC_UTILS import PC_UTILS
import math

def shift_rotate(input_path, output_path, shift_x, shift_y, shift_z, rotation_angle):
    pc_data = PC()
    pc_data.open(input_path, verbose = True) # verbose = False
    pc_data.points = PC_UTILS.shift(pc_data.points, shift_x, shift_y, shift_z)
    pc_data.points = PC_UTILS.rotate_points(pc_data.points, rotation_angle)
    pc_data.save(output_path, verbose = True) # verbose = False

if __name__ == "__main__" :
    input_path = "/Users/stella/projects/nirs2/content/01_05.las"
    output_path = "/Users/stella/projects/nirs2/content/output.csv"
    shift_x, shift_y, shift_z = 0, 0, 0
    rotation_angle = 0
    shift_rotate(input_path, output_path, shift_x, shift_y, shift_z, rotation_angle)