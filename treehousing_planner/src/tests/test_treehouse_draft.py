from os import path
import sys
from pathlib import Path

'''
Tests the functions used in the treehouse_layout
module with pytest.
'''
#From the treehouse_design package import the functions from 
# the treehouse_layout submodule.
from treehouse_design.treehouse_layout import get_tree_suitability
from treehouse_design.treehouse_layout import check_tree_number
from treehouse_design.treehouse_layout import get_my_tree_data
from treehouse_design.treehouse_layout import get_my_tree_variety
from treehouse_design.treehouse_layout import get_my_tree_radius
from treehouse_design.treehouse_layout import get_my_tree_diameter
from treehouse_design.treehouse_layout import calculate_diameter
from treehouse_design.treehouse_layout import calculate_radius
from treehouse_design.treehouse_layout import calculate_distance_between_tree_centers
from treehouse_design.treehouse_layout import get_xypoint_on_circle
from treehouse_design.treehouse_layout import find_tree_center_xypoint
from treehouse_design.treehouse_layout import create_circle
from treehouse_design.treehouse_layout import check_if_real_triangle
from treehouse_design.treehouse_layout import get_right_triangle_sides_from_coordinates
from treehouse_design.treehouse_layout import get_obtuse_triangle_sides_from_coordinates
from treehouse_design.treehouse_layout import use_law_of_cosines_to_find_angles
from treehouse_design.treehouse_layout import use_cosines_to_check_3_trees
from treehouse_design.treehouse_layout import convert_inches_to_feetinches
from treehouse_design.treehouse_layout import convert_feetinches_to_inches
from treehouse_design.treehouse_layout import round_num
from treehouse_design.treehouse_layout import return_required_measurments
from treehouse_design.treehouse_layout import format_req_measurements_for_ui
from treehouse_design.treehouse_layout import locate_file_in_directory
from treehouse_design.treehouse_layout import check_if_file_exists
from treehouse_design.treehouse_layout import get_number_type_from_user
from treehouse_design.treehouse_layout import get_string_from_user
from treehouse_design.treehouse_layout import get_number_of_trees_from_user
from treehouse_design.treehouse_layout import get_species_from_user
from treehouse_design.treehouse_layout import save_unique_user_data_text_file

import pytest
from pytest import approx
from unittest.mock import patch

#region method to plot trees
#------------------------------------ 3 Tests
'''
            B beta
           /\
         c/  \
         /    \a
 alpha A `     \
           b`   \
               ` \
                  C gamma
'''
@pytest.mark.parametrize('distances,bearings,expected', [
#   [A_B, A_C, B_C], [A_B, A_C, B_C]
(  #[1_2, 1_3, 2_3], [1_2, 1_3, 2_3]
    [240, 180, 180], [161, 210, 293], (True, True, True)
),
#(  #[2_1, 2_3, 1_3], [2_1, 2_3, 1_3]
   # [240, 180, 180], [240, 293, 210], (True, True, True)
#),
])

class TestTriangulation:
    '''
        Test the tree plotting method used in the treehouse layout
        prodram module.

        Notes:
            (0, 0) center point of A, (h, k) center point of B,
            (i, j) center point of C, (e, f) center point of C

        Calls
        -----
        - get_xypoint_on_circle
        - get_triangle_sides_from_coordinates
        - check_if_real_triangle
        '''

    def test_triangulation_A_B(self, distances, bearings, expected):

        h, k = get_xypoint_on_circle(distances[0], 0, 0, bearings[0])
        i, j = get_xypoint_on_circle(distances[1], 0, 0, bearings[1])
        e, f = get_xypoint_on_circle(distances[2], h, k, bearings[2])
        
        opp, adj, hyp = get_right_triangle_sides_from_coordinates(0, 0, h, k)
        print('1_2 a_b')
        print(f'\nopp: {opp}, adj: {adj}, hyp: {distances[0]}')
        print(f'target hyp: {hyp}')
        result, percent_error = check_if_real_triangle(adj, opp, distances[0])
        assert result is expected[0]
        if expected[0] is True:
            assert 0 <= percent_error <= 5
            # this checks that the center point obtained from the
            # bearing measurement is equal to the actual center point
            # that is obtained by 
            assert hyp == approx(distances[0], abs = 3)
        if expected[0] is not True:
            assert percent_error > 5
            assert hyp != distances[0]

    def test_triangulation_A_C(self, distances, bearings, expected):

        h, k = get_xypoint_on_circle(distances[0], 0, 0, bearings[0])
        i, j = get_xypoint_on_circle(distances[1], 0, 0, bearings[1])
        e, f = get_xypoint_on_circle(distances[2], h, k, bearings[2])

        opp1, adj1, hyp1 = get_right_triangle_sides_from_coordinates(0, 0, i, j)
        print('1_3 a_c')
        print(f' opp: {opp1}, adj: {adj1}, hyp: {distances[1]}')
        print(f' target hyp: {hyp1}')

        result, percent_error = check_if_real_triangle(adj1, opp1, distances[1])
        assert result is expected[1]
        if expected[1] is True:
            assert 0 <= percent_error <= 5
            assert hyp1 == approx(distances[1], abs=3)
        if expected[1] is not True:
            assert percent_error > 5
            assert hyp1 != distances[1]

    def test_triangulation_B_C(self, distances, bearings, expected):

        h, k = get_xypoint_on_circle(distances[0], 0, 0, bearings[0])
        i, j = get_xypoint_on_circle(distances[1], 0, 0, bearings[1])
        e, f = get_xypoint_on_circle(distances[2], h, k, bearings[2])
        
        opp2, adj2, hyp2 = get_right_triangle_sides_from_coordinates(h, k, e, f)
        print('2_3 b_c')
        print(f' opp: {opp2}, adj: {adj2}, hyp: {distances[2]}')
        print(f' target hyp: {hyp2}')
        result, percent_error = check_if_real_triangle(adj2, opp2, distances[2]) 
        assert result is expected[2]
        if expected[2] is True:
            assert 0 <= percent_error <= 5
            assert hyp2 == approx(distances[2], abs=3)
            assert i == approx(e, abs=3)
            assert j == approx(f, abs=3)
        if expected[2] is not True:
            assert percent_error > 5
            assert hyp2 != distances[2]
            assert i != e
            assert j != f


@pytest.mark.parametrize('distances,bearings,expected', [
#  [A_B, A_C, B_A, B_C, C_A, C_B]
(   #[1_2, 1_3, 2_3],[1_2, 1_3, 2_1, 2_3, 3_1, 3_2]
    [240, 180, 180], [161, 210, 240, 293, 29, 114], 180
)
])

class TestClass:
    def test_inner_angles_from_distances(self, distances, bearings, expected):
        '''
        Tests if distances between trees yield inner angles with a
        sum of 180 degrees.

        This function calls the use_law_of_cosines_to_find_angles 
        function to return the acute angles (in degrees) of a triangle 
        that has side lengths equal to the distances between trees.  
        The vaules returned are converted to degrees and their sum
        is compared to the excpected sum of 180 degrees.

        '''
        assert bearings == bearings
        alpha, beta, gamma = use_law_of_cosines_to_find_angles(distances[2], 
                                                               distances[1],
                                                               distances[0])
        print('// inner_angles_from_distances //')
        print(f'alpha:{alpha}, beta:{beta}, gamma:{gamma}')
        assert (alpha + beta + gamma) == approx(expected, abs=2)

    def test_inner_angles_from_bearings(self, distances,bearings, expected):
        '''
        Tests if bearings between three trees yield inner angles with a
        sum of 180 degrees.

        This function calls the get_inner_angles_from_bearings function,
        to return the acute angles (in degrees) of a triangle that has 
        bearings equal to the bearing measurments taken between trees.  
        The sum of vaules in degrees returned is compared to the 
        excpected sum of 180 degrees.

        Reminder: Bearing = (clockwise angle from possitive y-axis)
        '''
        assert distances == distances
        angles = get_inner_angles_from_bearings(bearings[0], bearings[1], 
                                                bearings[2], bearings[3], 
                                                bearings[4], bearings[5])
        alpha, beta, gamma = angles
        print('// inner_angles_from_bearings //')
        print(f'alpha:{alpha}, beta:{beta}, gamma:{gamma}')
        sum_angles = (alpha + beta + gamma)
        print(f'Sum of angles:{sum_angles}')
        assert sum_angles == approx(expected, abs=7)

# functions called in tests
def get_inner_angles_from_bearings(bearing_1_to_2, bearing_1_to_3, 
                                   bearing_2_to_1, bearing_2_to_3, 
                                   bearing_3_to_2, bearing_3_to_1):
    '''
    Find the acute angles of a triangle given the bearing 
    measurements (clockwise angle from possitive y-axis) of
    the points on the triangle. 

    Note on equivalence: 
    angle_'2(1)3' same as '3(1)2' represented by Alpha
    angle_'a(b)c' same as 'c(b)a' represented by Beta
    angle_'a(c)b' same as 'b(c)a' represented by Gamma
    '''
    # Convert bearings (clockwise angles from possitive y-axis) to inner
    # angles.
    angle_213 = abs(bearing_1_to_3 - bearing_1_to_2) # bac or A = alpha
    angle_123 = abs(bearing_2_to_3 - bearing_2_to_1) # abc or B = beta
    angle_231 = abs(bearing_3_to_2 - bearing_3_to_1) # bca or C = gamma
    return angle_213, angle_123, angle_231
    

#region check_tree_num
#---------------------------------- 1 tests
@pytest.mark.parametrize('tree_number,trees_in_file,expected', [
# Option 1
(1, 1, '...getting tree (1) data...'),
(2, 2, '...getting tree (2) data...'),
(3, 3, '...getting tree (3) data...'),
(4, 4, '...getting tree (4) data...'),
(5, 5, '...getting tree (5) data...'),
#
(1, 2, '...getting tree (1) data...'),
(1, 3, '...getting tree (1) data...'),
(1, 4, '...getting tree (1) data...'),
(1, 5, '...getting tree (1) data...'),
#
(2, 3, '...getting tree (2) data...'),
(2, 4, '...getting tree (2) data...'),
(2, 5, '...getting tree (2) data...'),
#
(3, 4, '...getting tree (3) data...'),
(3, 5, '...getting tree (3) data...'),
#
(4, 5, '...getting tree (4) data...'),
# Weird not expected cases
(4, 10, '...getting tree (4) data...'),
(3, 20, '...getting tree (3) data...'),
(9, 55, '...getting tree (9) data...'),
(56, 95, '...getting tree (56) data...'),
(2, 14, '...getting tree (2) data...'),
# Option 2
(0, 1, 'ERROR! You entered (0). \nThis tree number does not exist. '),
(0, 2, 'ERROR! You entered (0). \nThis tree number does not exist. '),
(0, 3, 'ERROR! You entered (0). \nThis tree number does not exist. '),
(0, 4, 'ERROR! You entered (0). \nThis tree number does not exist. '),
(0, 5, 'ERROR! You entered (0). \nThis tree number does not exist. '),
(-1, 1, 'ERROR! You entered (-1). \nThis tree number does not exist. '),
(-5, 2, 'ERROR! You entered (-5). \nThis tree number does not exist. '),
(-3, 3, 'ERROR! You entered (-3). \nThis tree number does not exist. '),
(-7, 4, 'ERROR! You entered (-7). \nThis tree number does not exist. '),
(0.7, 5, 'ERROR! You entered (0.7). \nThis tree number does not exist. '),
(0.999, 7, 'ERROR! You entered (0.999). \nThis tree number does not exist. '),
# Option 3
(1, 0, 'ERROR! You entered (1). \nThere are only 0 trees in the data file. '),
(2, 0, 'ERROR! You entered (2). \nThere are only 0 trees in the data file. '),
(3, 0, 'ERROR! You entered (3). \nThere are only 0 trees in the data file. '),
(4, 0, 'ERROR! You entered (4). \nThere are only 0 trees in the data file. '),
(5, 0, 'ERROR! You entered (5). \nThere are only 0 trees in the data file. '),
#
(2, 1, 'ERROR! You entered (2). \nThere are only 1 trees in the data file. '),
(3, 1, 'ERROR! You entered (3). \nThere are only 1 trees in the data file. '),
(4, 1, 'ERROR! You entered (4). \nThere are only 1 trees in the data file. '),
(5, 1, 'ERROR! You entered (5). \nThere are only 1 trees in the data file. '),
#
(3, 2, 'ERROR! You entered (3). \nThere are only 2 trees in the data file. '),
(4, 2, 'ERROR! You entered (4). \nThere are only 2 trees in the data file. '),
(5, 2, 'ERROR! You entered (5). \nThere are only 2 trees in the data file. '),
#
(4, 3, 'ERROR! You entered (4). \nThere are only 3 trees in the data file. '),
(5, 3, 'ERROR! You entered (5). \nThere are only 3 trees in the data file. '),
#
(5, 4, 'ERROR! You entered (5). \nThere are only 4 trees in the data file. '),
# Weird cases
(11, 2, 'ERROR! You entered (11). \nThere are only 2 trees in the data file. '),
(9, 5, 'ERROR! You entered (9). \nThere are only 5 trees in the data file. '),
(6, 3, 'ERROR! You entered (6). \nThere are only 3 trees in the data file. '),
(4, -1, 'ERROR! You entered (4). \nThere are only -1 trees in the data file. '),
])

def test_check_tree_number(tree_number, trees_in_file, expected):
    '''
    Test that the check_tree_number function returns the expected
    text string. 
    '''
    assert check_tree_number(tree_number, trees_in_file) == expected

#endregion


#region locate_file_in_dir
#---------------------------------- 2 tests

def locate_file_in_directory_no_exceptions(filename, file_type, folder=''):
    with patch('builtins.quit'):
        try:
            locate_file_in_directory(filename, file_type, folder)
        except Exception as excinfo:  
            pytest.fail(f"Unexpected exception raised: {excinfo}") 

def test_locate_file_in_directory_no_exceptions_raised():
    with patch('builtins.quit'):
        # TESTING FILE NAMES THAT EXIST
        # right filename, right type, In directory subfolder- missing.
        locate_file_in_directory_no_exceptions('p_exists.png', 'image')
        locate_file_in_directory_no_exceptions('t_exists.txt', 'text')
        # right filename, wrong type, In directory subfolder- missing.
        locate_file_in_directory_no_exceptions('p_exists.png', 'text')
        locate_file_in_directory_no_exceptions('t_exists.txt', 'image')
        # right filename, right type, subfolder in directory no exist.
        locate_file_in_directory_no_exceptions('t_exists.txt', 'text', 'no_exist_folder')
        locate_file_in_directory_no_exceptions('p_exists.png', 'image', 'no_exist_folder')
        # right filename, wrong type, subfolder in directory no exist.
        locate_file_in_directory_no_exceptions('t_exists.txt', 'image', 'no_exist_folder')
        locate_file_in_directory_no_exceptions('p_exists.png', 'text', 'no_exist_folder')
        # TESTING FILE NAMES THAT DO NOTEXIST
        # wrong filename, right type, In directory subfolder- missing.
        locate_file_in_directory_no_exceptions('no_p_exists.png', 'image')
        locate_file_in_directory_no_exceptions('no_t_exists.txt', 'text')
        # wrong filename, wrong type, In directory subfolder- missing.
        locate_file_in_directory_no_exceptions('no_p_exists.png', 'text')
        locate_file_in_directory_no_exceptions('no_t_exists.txt', 'image')
        # wrong filename, right type, subfolder in directory no exist.
        locate_file_in_directory_no_exceptions('no_p_exists.png', 'image', 'no_exist_folder')
        locate_file_in_directory_no_exceptions('no_t_exists.txt', 'text', 'no_exist_folder')
        # wrong filename, wrong type, subfolder in directory no exist.
        locate_file_in_directory_no_exceptions('no_p_exists.png', 'text', 'no_exist_folder')
        locate_file_in_directory_no_exceptions('no_t_exists.txt', 'image', 'no_exist_folder')
        # wrong filename, right, right subfolder directory.
        locate_file_in_directory_no_exceptions('no_exist.txt', 'text', 'program-test-files')
        locate_file_in_directory_no_exceptions('no_exist.png', 'image', 'program-test-files')
        # wrong filename, wrong type, right subfolder directory.
        locate_file_in_directory_no_exceptions('t_exists.txt', 'text', 'program-test-files')
        locate_file_in_directory_no_exceptions('p_exists.png', 'image', 'program-test-files')
        # TESTING CORRECT PARAMETERS BUT NO EXTENSIONS IN FILE
        # no filename ext, right type, right subfolder directory.
        locate_file_in_directory_no_exceptions('p_exists', 'image', 'program-test-files')
        locate_file_in_directory_no_exceptions('t_exists', 'text', 'program-test-files')
        # no filename ext, wrong type, right subfolder directory.
        locate_file_in_directory_no_exceptions('p_exists', 'text', 'program-test-files')
        locate_file_in_directory_no_exceptions('t_exists', 'image', 'program-test-files')

def test_locate_text_file(tmpdir):
    # Create a temporary test directory and file
    tmpdir.join('test.txt').write('Test file content')
    filename = 'test.txt'
    file_type = 'text'
    folder = str(tmpdir)
    output = 'text'

    result = locate_file_in_directory(filename, file_type, folder, output)
    assert result == 'Test file content'

#endregion


#region convert_in_to_ft_in
# --------------------------------- 2 tests
# Values tuple returned parameters
@pytest.mark.parametrize('inches,denominator,expected', [
    # Tests - output is ft, whole + fraction inches, returning values
    (136.25, 1, (11, 4.0, 0)),
    (136.25, 0, (11, 4.0, 0)),
    (136.25, 4, (11, 4.0, 1)), # 11ft 4 1/4in exact
    (136.25, 8, (11, 4.0, 2)),
    (136.25, 16, (11, 4.0, 4)), 
    (136.25, 32, (11, 4.0, 8)),
    # new measurement
    (285.375, 0, (23, 9.00, 0)),
    (285.375, 1, (23, 9.00, 0)),
    (285.375, 4, (23, 9.00, 2)),
    (285.375, 8, (23, 9.00, 3)), # 12ft 9 3/8in exact
    (285.375, 16, (23, 9.00, 6)),
    (285.375, 32, (23, 9.00, 12)),
    # new measurement
    (110.75, 0, (9, 2.0, 0)),
    (110.75, 1, (9, 3.0, 0)),
    (110.75, 4, (9, 2.0, 3)), # 9ft 2 3/4in exact
    (110.75, 8, (9, 2.0, 6)),
    (110.75, 16, (9, 2.0, 12)),
    (110.75, 32, (9, 2.0, 24)),
    # new measurement
    (37.625, 0, (3, 1.0, 0)), 
    (37.625, 1, (3, 2.0, 0)),
    (37.625, 4, (3, 1.0, 2)), #################
    (37.625, 8, (3, 1.0, 5)), # 3ft 1 5/8in exact
    (37.625, 16, (3, 1.0, 10)),
    (37.625, 32, (3, 1.0, 20)),
    # Tests - output is ft, whole inches, returning values
    (54, 0, (4, 6.0, 0)), # 4ft 6in exact
    (54, 1, (4, 6.0, 0)),
    (54, 4, (4, 6.0, 0)),
    (54, 8, (4, 6.0, 0)),
    (54, 16, (4, 6.0, 0)),
    (54, 32, (4, 6.0, 0)),
    # Tests - output is ft, fraction inches, returning values
    (180.8125, 0, (15, 0.0, 0)),
    (180.8125, 1, (15, 1.0, 0)),
    (180.8125, 4, (15, 0.0, 3)),
    (180.8125, 8, (15, 0.0, 7)),
    (180.8125, 16, (15, 0.0, 13)), # 15ft 13/16ths exact
    (180.8125, 32, (15, 0.0, 26)),
    # Tests - output is ft only, returning string
    (96, 0, (8, 0.0, 0)), # 8ft exact
    (96, 1, (8, 0.0, 0)),
    (96, 4, (8, 0.0, 0)),
    (96, 8, (8, 0.0, 0)),
    (96, 16, (8, 0.0, 0)),
    (96, 32, (8, 0.0, 0)),
    # new measurement
    (204, 0, (17, 0.0, 0)), # 17ft exact
    (204, 1, (17, 0.0, 0)),
    (204, 4, (17, 0.0, 0)),
    (204, 8, (17, 0.0, 0)),
    (204, 16, (17, 0.0, 0)),
    (204, 32, (17, 0.0, 0)),
    # Tests - output is whole inches + fraction inches, returning values
    (7.0754, 0, (0, 7.0, 0)), # 7 377/5000in exact
    (7.0754, 1, (0, 7.0, 0)), 
    (7.0754, 4, (0, 7.0, 0)),
    (7.0754, 8, (0, 7.0, 1)),
    (7.0754, 16, (0, 7.0, 1)),
    (7.0754, 32, (0, 7.0, 2)),
    # Tests - output is whole inches, returning values
    (6, 0, (0, 6.0, 0)), # 6in exact
    (6, 1, (0, 6.0, 0)),
    (6, 4, (0, 6.0, 0)),
    (6, 8, (0, 6.0, 0)),
    (6, 16, (0, 6.0, 0)),
    (6, 32, (0, 6.0, 0)),
    # new measurement
    (5, 0, (0, 5.0, 0)), # 5in exact
    (5, 1, (0, 5.0, 0)),
    (5, 4, (0, 5.0, 0)),
    (5, 8, (0, 5.0, 0)),
    (5, 16, (0, 5.0, 0)),
    (5, 32, (0, 5.0, 0)),
    # Tests - output is fraction inches only, returning values
    (0.25, 0, (0, 0.0, 0)), # 1/4in exact
    (0.25, 1, (0, 0.0, 0)),
    (0.25, 4, (0, 0.0, 1)),
    (0.25, 8, (0, 0.0, 2)),
    (0.25, 16, (0, 0.0, 4)),
    (0.25, 32, (0, 0.0, 8)),
    # Tests - outside scope of expected arguments, returning values
    # negative arguments
    (-32.545, 0, (-2, -8.0, 0)),
    (-32.545, 1, (-2, -7.0, 0)),
    (-32.545, 4, (-2, -8.0, -2)),
    (-32.545, 8, (-2, -8.0, -4)),
    (-32.545, 16, (-2, -8.0, -9)),
    (-32.545, 32, (-2, -8.0, -17)),
    # 0 value argument
    (0, 0, (0, 0, 0)),
    (0, 1, (0, 0, 0)),
    (0, 4, (0, 0, 0)),
    (0, 8, (0, 0, 0)),
    (0, 16, (0, 0, 0)),
    (0, 32, (0, 0, 0))
])
def test_convert_inches_to_feetinches_values(inches, denominator, 
                                             expected):
    '''
    Test the convert_inches_to_feetinches. 
    
    Specifically test values returned in a tuple by the 
    default argument p=False.
    '''
    result = convert_inches_to_feetinches(inches, denominator)
    assert result == expected
    # The function that is being tested has code to change 0 denominator to 1. 
    # Because the function does not return the denominator, 
    # I added the same code in this test function. 
    if inches == 0:
        absl = 0
    if inches < 0:
        absl = 2
    if inches > 0 and 0 <= denominator <= 2:
        absl = 1
    if inches > 0 and 2 < denominator <= 4:
        absl = 0.5
    if inches > 0 and 4 < denominator <= 8:
        absl = 0.09
    if inches > 0 and 8 < denominator <= 16:
        absl = 0.09
    if inches > 0 and 16 < denominator <= 32:
        absl = 0.02
    a, b, c = result
    print(denominator)
    if denominator <= 0:
        frc = 0
    if denominator > 0:
        frc = (c/denominator)
    assert inches == approx(
        (a*12 + b + frc), abs=absl
    )
 
# Text string parameters
@pytest.mark.parametrize('inches,denominator,p,expected', [
    # Tests - output is ft, whole + fraction inches, returning string
    (136.25, 0, True, '11 ft 4 inches'),
    (136.25, 1, True, '11 ft 4 inches'),
    (136.25, 4, True, '11 ft 4 1/4 inches'), # 11ft 4 1/4in exact
    (136.25, 8, True, '11 ft 4 2/8 inches'),
    (136.25, 16, True, '11 ft 4 4/16 inches'), 
    (136.25, 32, True, '11 ft 4 8/32 inches'),
    # new measurement
    (285.375, 0, True, '23 ft 9 inches'),
    (285.375, 1, True, '23 ft 9 inches'),
    (285.375, 4, True, '23 ft 9 2/4 inches'),
    (285.375, 8, True, '23 ft 9 3/8 inches'), # 12ft 9 3/8in exact
    (285.375, 16, True, '23 ft 9 6/16 inches'),
    (285.375, 32, True, '23 ft 9 12/32 inches'),
    # new measurement
    (110.75, 0, True, '9 ft 2 inches'),
    (110.75, 1, True, '9 ft 3 inches'),
    (110.75, 4, True, '9 ft 2 3/4 inches'), # 9ft 2 3/4in exact
    (110.75, 8, True, '9 ft 2 6/8 inches'),
    (110.75, 16, True, '9 ft 2 12/16 inches'),
    (110.75, 32, True, '9 ft 2 24/32 inches'),
    # new measurement
    (37.625, 0, True, '3 ft 1 inches'),
    (37.625, 1, True, '3 ft 2 inches'),
    (37.625, 4, True, '3 ft 1 2/4 inches'),
    (37.625, 8, True, '3 ft 1 5/8 inches'), # 3ft 1 5/8in exact
    (37.625, 16, True, '3 ft 1 10/16 inches'),
    (37.625, 32, True, '3 ft 1 20/32 inches'),
    # Tests - output is ft, whole inches, returning string
    (54, 0, True, '4 ft 6 inches'), # 4ft 6in exact
    (54, 1, True, '4 ft 6 inches'),
    (54, 4, True, '4 ft 6 inches'),
    (54, 8, True, '4 ft 6 inches'),
    (54, 16, True, '4 ft 6 inches'),
    (54, 32, True, '4 ft 6 inches'),
    # Tests - output is ft, fraction inches, returning string
    (180.8125, 0, True, '15 ft 0 inches'),
    (180.8125, 1, True, '15 ft 1 inches'),
    (180.8125, 4, True, '15 ft 3/4 inches'),
    (180.8125, 8, True, '15 ft 7/8 inches'),
    (180.8125, 16, True, '15 ft 13/16 inches'), # 15ft 13/16ths exact
    (180.8125, 32, True, '15 ft 26/32 inches'),
    # Tests - output is ft only, returning string
    (96, 0, True, '8 ft 0 inches'), # 8ft exact
    (96, 1, True, '8 ft 0 inches'),
    (96, 4, True, '8 ft 0 inches'),
    (96, 8, True, '8 ft 0 inches'),
    (96, 16, True, '8 ft 0 inches'),
    (96, 32, True, '8 ft 0 inches'),
    # new measurement
    (204, 0, True, '17 ft 0 inches'), # 17ft exact
    (204, 1, True, '17 ft 0 inches'),
    (204, 4, True, '17 ft 0 inches'),
    (204, 8, True, '17 ft 0 inches'),
    (204, 16, True, '17 ft 0 inches'),
    (204, 32, True, '17 ft 0 inches'),
    # Tests - output is whole + fraction inches, returning string
    (7.0754, 0, True, ' 7 inches'), # 7 377/5000in exact
    (7.0754, 1, True, ' 7 inches'),
    (7.0754, 4, True, ' 7 inches'),
    (7.0754, 8, True, ' 7 1/8 inches'),
    (7.0754, 16, True, ' 7 1/16 inches'),
    (7.0754, 32, True, ' 7 2/32 inches'),
    # Tests - output is whole inches, returning string
    (6, 0, True, ' 6 inches'), # 6in exact
    (6, 1, True, ' 6 inches'),
    (6, 4, True, ' 6 inches'),
    (6, 8, True, ' 6 inches'),
    (6, 16, True, ' 6 inches'),
    (6, 32, True, ' 6 inches'),
    # new measurement
    (5, 0, True, ' 5 inches'), # 5in exact
    (5, 1, True, ' 5 inches'),
    (5, 4, True, ' 5 inches'),
    (5, 8, True, ' 5 inches'),
    (5, 16, True, ' 5 inches'),
    (5, 32, True, ' 5 inches'),
    # Tests - output is fraction inches only, returning string
    (0.25, 0, True, ' 0 inches'), # 1/4in exact
    (0.25, 1, True, ' 0 inches'),
    (0.25, 4, True, ' 1/4 inches'),
    (0.25, 8, True, ' 2/8 inches'),
    (0.25, 16, True, ' 4/16 inches'),
    (0.25, 32, True, ' 8/32 inches'),
    # Tests - outside scope of expected arguments, returning string
    # negative arguments
    (-32.545, 0, True, '-2 ft -8 inches'),
    (-32.545, 1, True, '-2 ft -7 inches'),
    (-32.545, 4, True, '-2 ft -8 -2/4 inches'),
    (-32.545, 8, True, '-2 ft -8 -4/8 inches'),
    (-32.545, 16, True, '-2 ft -8 -9/16 inches'),
    (-32.545, 32, True, '-2 ft -8 -17/32 inches'),
    # 0 value argument
    (0, 0, True, ' 0 inches'),
    (0, 1, True, ' 0 inches'),
    (0, 4, True, ' 0 inches'),
    (0, 8, True, ' 0 inches'),
    (0, 16, True, ' 0 inches'),
    (0, 32, True, ' 0 inches')
])
def test_convert_inches_to_feetinches_string(inches, denominator, p,
                                             expected):
    '''
    Test the convert_inches_to_feetinches. 
    
    Specifically test measurement statements returned by the 
    argument p=True.
    '''
    result = convert_inches_to_feetinches(inches, denominator, p)
    assert result == expected

#endregion


#region return_req_meas
# --------------------------------- 1 test
@pytest.mark.parametrize('number_of_trees,expected', [
     # Test cases within targets
    (
        1, ([(None, None)], 
            [(None, None)])
    ),
    (
        2, ([(1, 2)], 
            [(1, 2)])
    ),
    (
        3, ([(1, 2), (1, 3), (2, 3)],
            [(1, 2), (1, 3)])
    ),
    (
        4, ([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)],
            [(1, 2), (1, 3), (1, 4)])
    ),
    (
        5, ([(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), 
             (2, 5), (3, 4), (3, 5), (4, 5)], 
             [(1, 2), (1, 3), (1, 4), (1, 5)])
    ),
     # Test special cases
    (
        -1, (0, 0)
    ),
    (
        0, (0, 0)
    ),
    (
        6, (0, 0)
    ),
    (
        5.2, (0, 0)
    )
])
def test_return_required_measurements(number_of_trees, expected):
    '''
    Test the return_required_measurements function.
    '''
    lst_tuples = return_required_measurments(number_of_trees)
    assert lst_tuples == expected
#endregion

#region form_req_meas_for_ui
# --------------------------------- 2 tests
# normal case parmeters
@pytest.mark.parametrize('measurements,expected', [
    (
        [(None, None)],
        'None needed.'
    ),
    (
        [(1, 2)],
        ['TREE_1 to TREE_2'],
    ),
    (
        [(1, 2), (1, 3), (2, 3)],
        ['TREE_1 to TREE_2', 'TREE_1 to TREE_3', 'TREE_2 to TREE_3']
    ),
    (
        [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)],
        ['TREE_1 to TREE_2', 'TREE_1 to TREE_3', 'TREE_1 to TREE_4', 
         'TREE_2 to TREE_3', 'TREE_2 to TREE_4', 'TREE_3 to TREE_4']
    ),
    (
        [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), 
         (3, 5), (4, 5)],
        ['TREE_1 to TREE_2', 'TREE_1 to TREE_3', 'TREE_1 to TREE_4', 
         'TREE_1 to TREE_5', 'TREE_2 to TREE_3', 'TREE_2 to TREE_4',
         'TREE_2 to TREE_5', 'TREE_3 to TREE_4', 'TREE_3 to TREE_5', 
         'TREE_4 to TREE_5']
    )
])
def test_format_req_measurements_for_ui_normal_cases(measurements, expected):
    '''
    Test the format_req_measurements_for_ui function by passing
    normal arguments.
    '''
    str_lst_result = format_req_measurements_for_ui(measurements)
    print(str_lst_result)
    assert str_lst_result == expected

# special case parameters
@pytest.mark.parametrize('measurements, expected', [
    # arguments that raise and handle IndexError and TypeError
    ((None, None), 'Error: None'),
    (None, 'Error: None'),
    ([None], 'Error: None'),
    ((1, 2, 3), 'Error: None'),
    ((0, 1, 2, 3), 'Error: None'),
    ((0.7, 1.4, 2.95), 'Error: None')
])
def test_format_req_measurements_for_ui_special_cases(measurements, expected):
    '''
    Test the format_req_measurements_for_ui function by passing
    unusual/non-typical arguments.
    '''
    str_lst_result = format_req_measurements_for_ui(measurements)
    assert str_lst_result == expected

#endregion


# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])

