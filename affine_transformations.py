import numpy as np
import math


def create_matrix(a1, a2, a3, a4):
    return np.array([a1, a2, a3, a4])

# translation matrix
def translate(array_v, x = 0, y = 0, z = 0):
    matrix = create_matrix([1, 0, 0, x],
                         [0, 1, 0, y],
                         [0, 0, 1, z],
                         [0, 0, 0, 1])
    vec = np.array([array_v[0], array_v[1], array_v[2]])
    vector_to_calc = np.append(vec, 1)
    result = np.dot(matrix, vector_to_calc)
    result_to_return = np.array([result[0], result[1], result[2]])

    return result_to_return

# rotation matrix
def rotate_x(array_v, angle):
    matrix = create_matrix([1, 0, 0, 0],
                         [0, math.cos(angle), -math.sin(angle), 0],
                         [0, math.sin(angle), math.cos(angle), 0],
                         [0, 0, 0, 1])
    vec = np.array([array_v[0], array_v[1], array_v[2]])
    vector_to_calc = np.append(vec, 1)
    result = np.dot(matrix, vector_to_calc)
    result_to_return = np.array([result[0], result[1], result[2]])

    return result_to_return

def rotate_y(array_v, angle):
    matrix = create_matrix([math.cos(angle), 0, math.sin(angle), 0],
                         [0, 1, 0, 0],
                         [-math.sin(angle), 0, math.cos(angle), 0],
                         [0, 0, 0, 1])

    vec = np.array([array_v[0], array_v[1], array_v[2]])
    vector_to_calc = np.append(vec, 1)
    result = np.dot(matrix, vector_to_calc)
    result_to_return = np.array([result[0], result[1], result[2]])

    return result_to_return

def rotate_z(array_v,angle):
    matrix = create_matrix([math.cos(angle), -math.sin(angle), 0, 0],
                         [math.sin(angle), math.cos(angle), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1])
    
    vec = np.array([array_v[0], array_v[1], array_v[2]])
    vector_to_calc = np.append(vec, 1)
    result = np.dot(matrix, vector_to_calc)
    result_to_return = np.array([result[0], result[1], result[2]])

    return result_to_return