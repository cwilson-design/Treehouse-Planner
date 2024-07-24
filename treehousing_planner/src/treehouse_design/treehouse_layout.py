'''
Treehouse Layout, a drafting tool for your treehousing endeavors
Copyright (C) 2024  Conner Wilson

A program that helps guide you through the initial steps in the planning
phase of building an amazing treehouse.

This program specifically helps you evaluate your trees, accesses
tree safety, and generates an accuretly scaled tree layout plan for 
drafting your treehouse platforms, beams, walls and posts. 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
# Import the operating system
import os
# Import the standard math library
import math
# Import the numpy library
import numpy as np
# Import the pyplot submodule from the matplotlib library
import matplotlib.pyplot as plt
# Import the image submodule from the matplotlib library
import matplotlib.image as mpimg
# Import the PdfPages class from the matplotlib.backends.backend_pdf submodule
from matplotlib.backends.backend_pdf import PdfPages
# Import the backend_inline module from the matplotlib_inline package
import matplotlib_inline.backend_inline

# Fixing random state for reproducibility
np.random.seed(19680801)

# Define the main function.
def main():
    #region Initialization

    # Initialize Matplotlib parameters.
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    matplotlib_inline.backend_inline.set_matplotlib_formats('svg', 'png')

    # Initialize DICTIONARIES
    # For the Following examples; 1 and 2 
    # are examples of what could be replaced with any two trees.

    bearings_dict = {} # 'bearing_1_to_2': bearing
    distances_bark_dict = {} # 'db_1_to_2': distance between bark of tree 1 and 2
    distances_cntrs_dict = {} # 'dc_1_to_2': distance between centers of tree 1 and 2
    plot_trees_dict = {} # tree_number: [center_point, xypoints, label, color]
    plot_distances_dict = {} # 'line_dc_1_to_2': [xypoints, label, color, linestyle]
    plot_triangulate_dict = {} # 'x_axis_1_to_2': xypoints, 'y_axis_1_to_2': xypoints
    picture_dict = {
        1: '1_tree_platform_examples.png',
        2: '2_tree_platform_examples.png',
        3: '3_tree_platform_examples.png',
        4: '4_tree_platform_examples.png',
        5: '5_tree_platform_examples.png',
    }
    # Initialize CONSTANTS
    COVER_IMG = 'the_cover.png'
    METHODS_IMG = 'platform_methods_page.png'
    DESIGN_IMG = 'platform_design_page.png'
    TREES_IMG = 'tree_line.png'
    
    CENTER_POINT_INDEX = 0 # plot_trees_dict
    TREE_XYPOINTS_INDEX = 1 # plot_trees_dict
    TREE_LABEL_INDEX = 2 # plot_trees_dict
    TREE_COLOR_INDEX = 3 # plot_trees_dict

    DISTC_XYPOINTS_INDEX = 0 # plot_distances_dict
    DISTC_LABEL_INDEX = 1 # plot_distances_dict
    DISTC_COLOR_INDEX = 2 # plot_distances_dict
    DISTC_LINESTYLE_INDEX = 3 # plot_distances_dict

    number_of_trees = 0
    tree = ''
    species_pretty = ''
    suitability = ''
    circumference = 0
    diameter = 0
    radius = 0

    # Define STATEMENTS
    species_requirement_statement = (
        '\n''  There are many different varieties of trees! Some '
        'are better for treehouses than others. \nTo build your '
        'dream treehouse to last for years of enjoyment, you must '
        'ensure that \nyour trees are the kind suitable to the '
        'loads and stresses they must bear. '
    )
    size_requirement_statement = (
        '\n''  To build a longlasting treehouse, we first need to \n'
        'determine if the species of trees are suitible to the \n'
        'loads and stresses that they would bare. \n'
    )
    arborist_statement = (
        '\n''   We highly encourage you to consult an arborist to \n'
        'evaluate the health, root soil conditions, and expected \n'
        'longevity of your trees. \n'
    )
    bearing_intro_statement = (
        '\nBearings\n'
        '--------'
        '\n''  Plotting the trees scale one to another on a layout'
        ' drawing \nrequires that we measure the bearings in degrees'
        ' of the trees. \n'
        'What is a bearing ? \n'
        '       N \n'
        ' W <-- | --> E \n'
        '       S \n'
        'A compass bearing is the clockwise angle measured between '
        'point \nand true north on a compass. For tree layout, it '
        'is to determine \nthe exact degree measure the direction '
        'of (tree a to tree b) is \nfrom the direction of north.' 
    )
    bearing_instructions_statement = (
        '\nInstructions: \n'
        '   With your compass, stand directly at Tree #1. \n'
        'You may stand in front or hold the compass at the truck. \n'
        'While keeping the compass as level as you can, point the \n'
        'marker directly at center of the second tree. Record the \n'
        'the bearing in degrees. If you have more than two trees, \n'
        'repeat this process for the remaining trees, taking all \n'
        'your bearings from Tree #1. \n'
    )
    program_close_statement = (
        '\nPlease consider a different area to build that has the \n'
        'quantity of trees you desire, or you may \nrestart the '
        'program for a different area of trees. \n'
    )
    distance_instructions_statement = (
        '\nDistances \n'
        '--------- \n'
        '   Measure and record the distance between trees '
        '(bark to bark) in feet,inches. \n'
        'Use a water level or laser ensure your measurments are \n'
        'level to one another. Take all measurments at hardware \n'
        'or deck level (hardware is installed about 1-2 feet below \n'
        'deck level). \n'
    )
    #endregion

    #region Tree #s
    #--------------
    # ==== Get general tree information from user, access trees, and 
    # store responses as data in 'my_tree_data.txt'. ====
    print()
    user_name = get_string_from_user('Please enter your first name: ')
    if (' ') in user_name:
        user_name = user_name.split(' ')[0]
    number_of_trees = 5  #get_number_of_trees_from_user()
    
    # Create a file and print a heading on the first line.
    with open('my_tree_data.txt', 'wt') as my_tree_data_file:
        print(
            'Tree #, species, suitability, circumference(inches), '
            'diameter(inches), radius(inches) ', file=my_tree_data_file
        )
    #endregion

    #region Species & Circum
    #-----------------------
    print(species_requirement_statement)
    print(size_requirement_statement)
    print(40 * '-')
    # Define `n` as 0, to be used to count the number of trees that are
    # of a variety and have a diameter that is suitable to treehouse
    # building. This is used to name the Tree number in the correct
    # order when it and it's data is added to the my_tree_data file.
    n = 0
    # Loop through the number of trees entered by the user to retreive
    # data specific to each one.
    for i in range(number_of_trees):
        # Add 1 to the starting index (0) of range in order to begin
        # labels at tree_1, instead of tree_0.
        tree = f'TREE_{i+1}'
        #
        spec_info = get_species_from_user(tree, program_close_statement)
        (suitability, species_pretty) = spec_info
        # If tree species entered is suitable, tell the user, and
        # continue to determining if it's diameter is sufficient.
        if suitability != 'unsuitable':
            print(
                f'/{species_pretty}s/ are '
                f'{suitability} trees for treehouses. '
            )
            circumference_prompt = (
                'Using a tape measure, find the '
                'circumference of the tree in inches. '
                f'\nEnter the circumference of {tree}: '
            )
            circumference = get_number_type_from_user(circumference_prompt)
            # Call the calculate_diameter function and return the
            # diameter of the current tree in inches
            diameter = calculate_diameter(circumference)
            # Call the calculate_radius function and return the
            # radius of the current tree in inches.
            radius = calculate_radius(diameter)
            # For 2 or more trees supporting a treehouse, they must
            # have a diameter of at least 8".
            # A single tree must have a diameter of at least 18" to
            # support a treehouse alone.
            # If the current tree has a sufficient diameter based on
            # these conditions:
            if (number_of_trees > 1 and diameter >= 8
                    or number_of_trees == 1 and diameter >= 18):
                # Print the diameter to the user to 2 decimal points.
                print(f'/ Diameter: {diameter:.2f} inches ')
                # Add one to the counter so that each time a tree is 
                # suitable in variety and diameter, it can be given an 
                # integer number value starting from 1.
                n = n + 1
                # At the first suitable tree, create a text file.
                # Write to it for every suitable tree that follows.
                with open('my_tree_data.txt', 'at') as my_tree_data_file:
                    # Append the tree's data to the end of the file 
                    # on a single line.
                    print(
                        f'TREE_{n}, '
                        f'{species_pretty}, '
                        f'{suitability}, '
                        f'{circumference:.2f}, '
                        f'{diameter:.2f}, '
                        f'{radius:.2f}',
                        file=my_tree_data_file
                    )
                    # Close file.
                # Create placeholders for elements in a values list in 
                # the `plot_trees_dict` dictionary.
                center_point = (0, 0)
                tree_xypoints = (0, 0)
                tree_label = 'label'
                tree_color = 'color'
                # Add the list to the dictionary with a unique key- the
                # number of the current tree. 
                plot_trees_dict[n] = [
                    center_point, tree_xypoints,
                    tree_label, tree_color
                ]
                # Print a statement to the user showing that the current
                # tree's data was saved.
                print('..Data Saved..')
            # If the total number of trees are more than 1 and the
            # diameter of the current tree is less than 8 inches, it
            # is too small. Omit it's data from being saved to file.
            elif number_of_trees > 1 and diameter < 8:
                print(
                    f'/ {tree} has a diameter of {diameter}, which '
                    'is too small to safely be used for a treehouse. '
                )
                # Remove it from the number of total trees to maintain
                # length of loop itteration.
                number_of_trees = number_of_trees - 1
            # If the total number of trees is 1 and the diameter
            # of the current tree is less than 18 inches, it
            # is too small. Omit it's data from being saved to file.
            elif number_of_trees == 1 and diameter < 18:
                print(
                    f'/ {tree} has a diameter of {diameter}, which '
                    'is too small to safely be used for a treehouse. '
                )
                break
                ### End nested if statements- number trees and diameters
            ## End if statement for suitable trees.
        # If tree species entered is NOT suitable, omit it from being
        # saved to data txt file.
        elif suitability == 'unsuitable':
            print(
                f'Sadly, / {species_pretty}s / are '
                f'{suitability.upper()} trees for treehouses. '
            )
            # Remove the tree from the number of total trees.
            number_of_trees = number_of_trees - 1
            ## End if statement for unsuitable trees.
        print(40 * '-')
        # End Loop. 
    # Having determined which of the trees entered by user are
    # suitable, of the remaining number of suitable trees,
    # do the following.
    if number_of_trees == 1:
        tree_1_diameter = get_my_tree_diameter(1)
        if tree_1_diameter < 18:
            print(
                'Because only one tree is suitable, it must have a '
                'diameter greater than 18 inches. \nIts diameter is '
                f'only {get_my_tree_diameter(1)} inches. \n'
            )
            print(program_close_statement)
            quit()
        # else continue
    elif number_of_trees == 0:
        print(
            'Unfortunetely, none of the trees you entered '
            'are suitable for treehouse building. \n'
        )
        print(program_close_statement)
        quit()
    else:
        answer = get_string_from_user(
            'Would you like to continue your treehouse '
            f'with {number_of_trees} trees?: ', 
            response_option_1='yes',
            response_option_2='no'
        )
        if answer.lower() == 'no':
            print(program_close_statement)
            quit()
        else:
            print(arborist_statement)
            ## End nested if statements.
        # End if statements.
    #endregion
    
    #region Distances & Bearings
    #---------------------------
    req = return_required_measurments(number_of_trees)
    (required_distance_measurements, required_bearings_measurements) = req

    # Display the required distance measurements 
    # returned by the function to the user.
    print('Distance measurements to take: ')
    rm = format_req_measurements_for_ui(required_distance_measurements)
    print(rm)
    # Display the required bearing measurements 
    # returned by the function to the user.
    print('Bearing measurements to take:')
    rm = format_req_measurements_for_ui(required_bearings_measurements)
    print(rm)
    # If the number of trees is greater than one, there are measurments
    # that need to be taken.
    if number_of_trees > 1:
        # -----DISTANCE-----
        # Display a message to the user about how to take proper
        # distance measurements between trees.
        print(distance_instructions_statement)
        # Define a prompt to display to user to get number data.
        feet_prompt = ('  Feet: ')
        inches_prompt = ('  Inches: ')
        # Loop through distance measurement tuples and get data 
        # from user for each required one. Then, add to dictionaries.
        
        for ta, tb in required_distance_measurements:
            print(f'Enter distance from TREE_{ta} to TREE_{tb} ')
            # Call the `get number data from user` function to loop
            # until the user enters a number (float or int) and do
            # this for both feet and inches. 
            feet = get_number_type_from_user(feet_prompt)
            inches = get_number_type_from_user(inches_prompt)
            # Convert feet+inches to inches and save to distances 
            # dictionary with a unique key. 
            db = convert_feetinches_to_inches(feet, inches)
            distances_bark_dict[f'db_{ta}_to_{tb}'] = db
            # Using the distance between barks, calculate the distance
            # between centers of ta and tb by calling the below 
            # function. Save to distances dictionary with a unique key. 
            dc = calculate_distance_between_tree_centers(ta, tb, db)
            distances_cntrs_dict[f'dc_{ta}_to_{tb}'] = dc
            # Add a list to the plot distances dictionary and
            # define a unique key. In the list, add placeholders.
            plot_distances_dict[f'line_dc_{ta}_to_{tb}'] = [
                (0, 0),  # distance_xypoints (placeholders)
                'label',  # distance_label (placeholders)
                'color',  # distance_color (placeholders)
                'linestyle'  # distance_linestyle (placeholders)
            ]
            # End loop.
            
        # -----BEARINGS-----
        print(bearing_intro_statement)
        print(bearing_instructions_statement)
        
        bearing_prompt = (
                f'Enter bearing from TREE_{ta} to TREE_{tb} in degrees: '
            )
        # Loop through bearing measurement tuples and get data 
        # from user for each required one. Then, add to dictionary.
        
        for ta, tb in required_bearings_measurements:
            # Call the `get number data from user` function to loop
            # until the user enters a number (float or int).
            degrees = get_number_type_from_user(bearing_prompt.format(ta=ta, tb=tb))
            # Save to bearings dictionary with unique key.
            bearings_dict[f'bearing_{ta}_to_{tb}'] = degrees
            
        # End if statement.
    #endregion

    #region Tree 1 graph
    #-------------------
    # Display a title statement to the user.
    print('/////// RENDERING TREE 1 ////////')
    # // Create a circl of tree 1 on a cartesian plane //
    # by calling the create_circle function and passing
    # (0,0) as it's center point on the grid. 
    # Label the circle with it's diameter in inches and variety.
    tr1_lbl = (
        f'TREE_1 {get_my_tree_variety(1)} '
        f'{get_my_tree_diameter(1)}" '
    )
    xpoints1, ypoints1 = create_circle(1, (0, 0))
    # In the plot trees dictionary, replace the placeholder elements
    # with plot characteristics for tree 1 circle. 
    plot_trees_dict[1][TREE_XYPOINTS_INDEX] = (xpoints1, ypoints1)
    plot_trees_dict[1][TREE_LABEL_INDEX] = tr1_lbl
    plot_trees_dict[1][TREE_COLOR_INDEX] = 'red'
    # Display a message that the tree was plotted succesfully
    print()
    print('tree 1 rendered successfully ')
    print('-' * 40)
    print()
    #endregion

    #region Trees & Dist graphs
    #--------------------------
    # ==== Create remaining trees as Circles & distances from 
    # tree 1 to each tree as Lines on a cartesian plane ====
    # Define a starting point to be used on the grid which represents
    # the relative point at which the bearing measurements were taken.
    starting_point = (0, 0)
    # Make a list containing 4 colors, which will be itterated through
    # to give each tree plotted a new color.
    # Note: Tree 1 color is assigned seperatly. This list contains
    # 4 colors because the maximum num of trees is 5.
    tree_line_colors = ['b', 'g', 'y', 'm']
    # Begin a loop through the range of the total number of trees in
    # the data set - 1. Because tree 1 has previously been plotted, the 
    # next tree number and remaining are one less than the range of 
    # tree numbers. This means that if there is only 1 tree to work with, 
    # range is 0 and the code in loop does not begin.
    for tree in range(number_of_trees-1):
        # Skip tree 1 (skip index 0 and 1), to start at tree 2 for the
        # first itteration. Then for remaining, next = previous + 1.
        tree_current = (tree + 2)
        # Define a variable that gets an element (color) from the
        # tree_line_colors list for each loop. This will be used as 
        # color of the cirlce on the plot.
        tree_color = tree_line_colors[tree]
        # Display a title statement to the user.
        print(f'/////// RENDERING TREE {tree_current} //////')
        print()
        # Extract distance and bearing measurements from their
        # dictionaries, respectively.
        distanceb = distances_bark_dict[f'db_1_to_{tree_current}']
        bearing = bearings_dict[f'bearing_1_to_{tree_current}']
        # Find the center point of the current tree on the grid
        # by calling the find_tree_center_xy_point function and 
        # return it as center_pnt; by passing the...
        # , center point of tree 1 as the starting_point
        # , tree number 1 as the starting_tree
        # , distance between the barks of current tree and tree 1
        #   as distanceb
        # , and the bearing from tree 1 to current tree
        #   as bearing.
        center_pnt = find_tree_center_xypoint(
            starting_point, 1, tree_current, distanceb, bearing
        )
        # // Create the <current tree> as a circle on a cartesian plane.
        # Define a label to be used in the figure/graph legend.
        tr_lbl = (
            f'TREE_{tree_current} '
            f'{get_my_tree_variety(tree_current)} '
            f'{get_my_tree_diameter(tree_current)}" '
        )
        # Call the create circle function to get an array of xypoints.
        tr_xpoints, tr_ypoints = create_circle(tree_current, center_pnt)
        # Pack arrays into a tuple to preserve line length.
        tr_xy_points = (tr_xpoints, tr_ypoints)
        # In plot trees dictionary, replace the default center point
        # (0, 0) in values list with the current tree's correct center
        # as a tuple (x, y).
        # In the plot trees dictionary, replace the placeholder elements
        # with characteristics for the tree circle plot.
        if tree_current in plot_trees_dict:
            plot_trees_dict[tree_current][CENTER_POINT_INDEX] = center_pnt
            plot_trees_dict[tree_current][TREE_XYPOINTS_INDEX] = tr_xy_points
            plot_trees_dict[tree_current][TREE_LABEL_INDEX] = tr_lbl
            plot_trees_dict[tree_current][TREE_COLOR_INDEX] = tree_color
        else:
            print(f'Error: Tree {tree_current} not found in plot_trees_dict.')
        # Unpack the coordinate tuples of the current and 1st
        # tree's center points.
        x2, y2 = center_pnt
        x1, y1 = starting_point
        # // Create the distance between <Tree 1> and <current tree>
        # as a line. //
        # Generate an array of points representing distance and
        # direction between the center of the current tree and
        # the center of tree 1.
        d1_xpoints = np.array([0, x2])
        d1_ypoints = np.array([0, y2])
        d1_xy_points = (d1_xpoints, d1_ypoints)
        # Get the appropriate distance measurement from bark of 
        # the current tree to bark of tree 1 to be used as a label in 
        # the figure/graph legend.
        inches_db_1 = distances_bark_dict[f'db_1_to_{tree_current}']
        str_db_1 = convert_inches_to_feetinches(inches_db_1, 8, True)
        d1_label = f'Distance T1 to T{tree_current}: {str_db_1}'
        # Store the following unique dictionary key in a variable to 
        # preserve line length.
        key = f'line_dc_1_to_{tree_current}'
        # In the plot distances dictionary, add characteristics to the 
        # plot line: distance between center of tree 1 and current tree.
        plot_distances_dict[key][DISTC_XYPOINTS_INDEX] = d1_xy_points
        plot_distances_dict[key][DISTC_LABEL_INDEX] = d1_label
        plot_distances_dict[key][DISTC_COLOR_INDEX] = 'blue'
        plot_distances_dict[key][DISTC_LINESTYLE_INDEX] = 'dashed'
        # // Create a line representing x-axis of the distance line.
        # (adjacent side of right triangle) //
        ad_xpoints = np.array([0, x2])
        ad_ypoints = np.array([y2, y2])
        ad_xy_points = (ad_xpoints, ad_ypoints)
        # In plot triangulate dictionary, add the above xypoints with
        # a unique key.
        plot_triangulate_dict[f'x_axis_1_to_{tree_current}'] = ad_xy_points
        # // Create a line representing y-axis of the distance line 
        # (opposite side of right triange) //
        op_xpoints = np.array([0, 0])
        op_ypoints = np.array([0, y2])
        op_xy_points = (op_xpoints, op_ypoints)
        # In plot triangulate dictionary, add the above xypoints with
        # a unique key.
        plot_triangulate_dict[f'y_axis_1_to_{tree_current}'] = op_xy_points
        
        #region Initial triangulation
        # // Check triangulation //
        # Use the pythagoream therorem to determine if the lengths of
        # above xy lines create a real right triangle. This verifies
        # that distance and bearing measurements entered produce
        # an accurate scaled layout. (opposite, adjacent, hypotenuse)
        hyp = distances_cntrs_dict[f'dc_1_to_{tree_current}']
        opp, adj, hyp1 = get_right_triangle_sides_from_coordinates(x1, y1, 
                                                                   x2, y2)
        print(f' Program note~ Target hyp: {hyp1} ')
        # Note: hyp1 is the length of the theoretical hypotenuse that
        # makes a real right triangle with given opp and adj sides.
        # hyp1 is not used elsewhere in module. It could be used for
        # troubleshooting a future error in the plotting of trees.
        # Print a program note to the user displaying the sides.
        print(f' Program note~ opp: {opp}, adj: {adj}, hyp: {hyp}')
        # Call the check_if_real_triangle_function to test
        # triangulation.
        acceptance, percent_error = check_if_real_triangle(adj, opp, hyp)
        if acceptance is True:
            print()
        if acceptance is not True:
            print(
                f'The plot of Trees {ta} and {tb} on the grid may be ' 
                'slightly out of scale \ndue to inaccuracies in ' 
                'the distance or bearing measurements taken. \n '
                'please consider retaking your measurements. '
            )
        print()
        print(f'tree {tree_current} rendered successfully. ')
        print('-' * 40)
        print()
        # End loop.
    #endregion

    #region Remain Dist graphs
    #-------------------------
    # ==== Create the distances between all the trees greater than 1 as
    # lines on a cartesian plane. =====
    # -- the lines representing the distances between remaining 
    # trees `ta` to `tb`, given that lines tree_1 to tree_n,... have 
    # been created previously. --
    # Start counter at 0.
    counter = 0
    #
    for ta, tb in required_distance_measurements:
        # If there are only 2 trees or less, their distances have
        # already been plotted. Break out of loop.
        if len(required_distance_measurements) == 1:
            break
        # Create a counter that increases by one each loop.
        counter = counter + 1
        # When the counter reaches the distance measurements that
        # have not been plotted from the required_measurements list,
        if counter > number_of_trees-1:
            # Generate an array of points representing distance and
            # direction between the center of the previous tree and
            # the center of the current tree.
            x2, y2 = plot_trees_dict[tb][CENTER_POINT_INDEX]
            x1, y1 = plot_trees_dict[ta][CENTER_POINT_INDEX]
            # Create a plot label for the distance line by accessing
            # distance between barks from the dictionary. Call the
            # convert_feetinches_to_inches function and pass True for
            # `p` parameter to return a clean, readable string.
            inches_db = distances_bark_dict[f'db_{ta}_to_{tb}']
            str_db = convert_inches_to_feetinches(inches_db, 8, True)
            # Generate an array of points representing the distance
            # and direction between the center of tree `ta` and the
            # center of tree `tb`. Plot line created by the array
            # of xy points with dashed format and add a legend label.
            d_xpoints = np.array([x1, x2])
            d_ypoints = np.array([y1, y2])
            d_xy_points = (d_xpoints, d_ypoints)
            # In the plot distances dictionary, add plot characteristics
            # to the distance line between center of tree a and b.
            key_ab = f'line_dc_{ta}_to_{tb}'
            plot_distances_dict[key_ab][DISTC_XYPOINTS_INDEX] = d_xy_points
            plot_distances_dict[key_ab][DISTC_COLOR_INDEX] = 'blue'
            plot_distances_dict[key_ab][DISTC_LABEL_INDEX] = (
                f'Distance T{ta} to T{tb}: {str_db}'
            )
            plot_distances_dict[key_ab][DISTC_LINESTYLE_INDEX] = 'dashed'
        # Continue looping through the tuples in required distance
        # measurements list until reaching distances that have not yet
        # been created.
        if counter < number_of_trees-1:
            continue
        # End loop.
    #endregion

    #region triangulation
    print('\n.....Checking final layout accuracy.....\n')
    if number_of_trees == 3:
        use_cosines_to_check_3_trees(plot_trees_dict[1][CENTER_POINT_INDEX],
                                     plot_trees_dict[2][CENTER_POINT_INDEX],
                                     plot_trees_dict[3][CENTER_POINT_INDEX],
                                     1, 2, 3)
    if number_of_trees == 4:
        use_cosines_to_check_3_trees(plot_trees_dict[1][CENTER_POINT_INDEX],
                                    plot_trees_dict[2][CENTER_POINT_INDEX],
                                    plot_trees_dict[3][CENTER_POINT_INDEX],
                                    1, 2, 3)
        use_cosines_to_check_3_trees(plot_trees_dict[2][CENTER_POINT_INDEX],
                                    plot_trees_dict[3][CENTER_POINT_INDEX],
                                    plot_trees_dict[4][CENTER_POINT_INDEX],
                                    2, 3, 4)
    if number_of_trees == 5:
        use_cosines_to_check_3_trees(plot_trees_dict[1][CENTER_POINT_INDEX],
                                    plot_trees_dict[2][CENTER_POINT_INDEX],
                                    plot_trees_dict[3][CENTER_POINT_INDEX],
                                    1, 2, 3)
        use_cosines_to_check_3_trees(plot_trees_dict[2][CENTER_POINT_INDEX],
                                    plot_trees_dict[3][CENTER_POINT_INDEX],
                                    plot_trees_dict[4][CENTER_POINT_INDEX],
                                    2, 3, 4)
        use_cosines_to_check_3_trees(plot_trees_dict[3][CENTER_POINT_INDEX],
                                    plot_trees_dict[4][CENTER_POINT_INDEX],
                                    plot_trees_dict[5][CENTER_POINT_INDEX],
                                    3, 4, 5)     
    #endregion

    #region Save Data
    #----------------
    # Call the function to 
    print()
    save_unique_user_data_text_file(user_name, 'my_tree_data.txt')
    print()
    # 
    print('...Saving Tree Layout PDF....')
    filename = (f'{user_name.lower()}s_tree_layout.pdf')
    # Call the check_if_filename_exists function to prevent saving on
    # top of an already existing filename in the directory.
    while check_if_file_exists(filename) is True:
        filename = input("\nPlease enter a unique name "
                         "(without '.pdf') to save file as: ")
    # Make sure that the saved file has a .pdf extension of else it will
    # be corrupted and unreadable. 
    if '.' in filename:
        if filename.rsplit('.',1)[-1] == 'pdf':
            pass
    if '.' not in filename:
        filename = (f'{filename}.pdf')

    fig1_title = (f"{user_name.capitalize()}'s Tree Layout | Distances ")
    fig2_title = (f"{user_name.capitalize()}'s Tree Layout | Plan ")
    # Create the PdfPages object to which to save the pages:
    # The with statement makes sure that the PdfPages object is 
    # closed properly at the end of the block, even if an Exception 
    # occurs.
    with PdfPages(filename) as pdf:
        #region Plot/fig Tree Data

        # ===== Page 4 - Tree Data =====
        page_2_layout = [
            ['A'],
            ['B'],
            ['C']
        ]
        fig, ax = plt.subplot_mosaic(page_2_layout, figsize=(9.5, 7.5))
        # - Data row A -
        tree_data_txt = locate_file_in_directory(
                filename='my_tree_data.txt', file_type='text', output='text'
            )
        ax['A'].text(0.05, 0.5, tree_data_txt, fontsize=12, va='top', 
                     ha='left', bbox=dict(facecolor='green', alpha=0.5))
        ax['A'].axis('off')
        # - Platform Examples row B -
        file_path = locate_file_in_directory(
                        filename=picture_dict[number_of_trees], 
                        file_type='image', 
                        folder='layout_images'
                    )
        image = plt.imread(file_path)
        ax['B'].imshow(image)
        ax['B'].axis('off')
        ax['B'].set_title(
            f'{'\nExample Platform Designs':>25}{'.' * 100} \n'
            'common ways to layout beams and platforms, '
            'with several combinations of beams and posts.\n ',
            loc='left', 
            style='italic',
            fontsize=10
        )
        # - Tree Image row C -
        file_path = locate_file_in_directory(
                        filename=TREES_IMG, 
                        file_type='image', 
                        folder='layout_images'
                    )
        image = plt.imread(file_path)
        ax['C'].imshow(image)
        ax['C'].axis('off')
        plt.tight_layout()
        fig.suptitle("Your Trees' Data", fontsize=24)
        pdf.savefig(fig)
        plt.close
        #endregion

        #region Plot/fig Layout 1

        # ===== Page 5 - Tree Layout with Distances =====
        # Tree layout diagram that includes distances between trees.
        fig, ax = plt.subplots(figsize=(10, 7.5))
        fig1_title = (f"{user_name.capitalize()}'s Tree Layout | Distances ")
        # Plot the tree circles :
        for key, value in plot_trees_dict.items():
            xpoints, ypoints = value[TREE_XYPOINTS_INDEX]
            plt.plot(
                xpoints, ypoints,
                color=value[TREE_COLOR_INDEX],
                label=value[TREE_LABEL_INDEX]
            )
        # Plot the distances between trees :
        for key, value in plot_distances_dict.items():
            xpoints, ypoints = value[DISTC_XYPOINTS_INDEX]
            plt.plot(
                xpoints, ypoints,
                color=value[DISTC_COLOR_INDEX],
                label=value[DISTC_LABEL_INDEX],
                linestyle=value[DISTC_LINESTYLE_INDEX]
            )
        # Plot the triangulation lines :
        for key, value in plot_triangulate_dict.items():
            xpoints, ypoints = value
            plt.plot(
                xpoints, ypoints,
                color='black',
                linestyle='dotted'
            )
        plt.rcParams['text.usetex'] = False
        ax.grid(axis='both')
        # set the number of ticks for the x and y axis
        ax.tick_params(axis='x', rotation=80)
        ax.set_xticks(range(-1200, 1200, 6))
        ax.set_yticks(range(-1200, 1200, 6))
        for label in ax.xaxis.get_ticklabels()[::2]:
            label.set_visible(False)
        for label in ax.yaxis.get_ticklabels()[::2]:
            label.set_visible(False)
        ax.annotate(
            'N', xy=(-54, 5), xytext=(-54, -12), fontsize=18,
            ha='center', va='center',
            arrowprops=dict(facecolor='black', arrowstyle='->', 
                            linewidth=4, mutation_scale=20)
        )
        # set the y and x axis data pixels equal to prevent distortion
        ax.axis('equal')
        ax.set_title(label=fig1_title, loc="center")
        # Set the legend location to the center left outside the graph
        # by using the bbox_to_anchor function.
        ax.legend(loc='center left', fontsize=10) #,bbox_to_anchor=(1, 0.5)
        # Use a tight layout to preserve defined margins.
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close()

        #endregion
        
        #region Plot/fig Layout 2
        #------------------------
        # ===== Page 6 - Tree Layout trees only =====
        # Tree layout diagram that only includes trees. Used for
        # laying out treehouse beams, hardware, floor plan, etc.
        fig2_title = (f"{user_name.capitalize()}'s Tree Layout | Plan ")
        fig, ax = plt.subplots(figsize=(10, 7.5))
        for key, value in plot_trees_dict.items():
            xpoints, ypoints = value[TREE_XYPOINTS_INDEX]
            ax.plot(
                xpoints, ypoints,
                color=value[TREE_COLOR_INDEX],
                label=value[TREE_LABEL_INDEX]
            )
        plt.rcParams['text.usetex'] = False
        ax.grid(axis='both')
        # set the number of ticks for the x and y axis
        ax.tick_params(axis='x', rotation=80)
        ax.set_xticks(range(-1200, 1200, 6))
        ax.set_yticks(range(-1200, 1200, 6))
        for label in ax.xaxis.get_ticklabels()[::2]:
            label.set_visible(False)
        for label in ax.yaxis.get_ticklabels()[::2]:
            label.set_visible(False)
        ax.annotate(
            'N', xy=(-54, 5), xytext=(-54, -12), fontsize=18,
            ha='center', va='center',
            arrowprops=dict(facecolor='black', arrowstyle='->', 
                            linewidth=4, mutation_scale=20)
        )
        # set the y and x axis data pixels equal to prevent distortion
        ax.axis('equal')
        ax.set_title(label=fig2_title, loc="center")
        # Set the legend location to the center left outside the graph
        # by using the bbox_to_anchor function.
        ax.legend(loc='center left', fontsize=10) #,bbox_to_anchor=(1, 0.5)
        # Use a tight layout to preserve defined margins.
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close
        #endregion

    # PDF close
    print(f'\n...Tree Layout PDF saved as {filename}....')
    
    #plt.show()
# End main.


#region Functions- access files (6)
#------------------------------
# Access tree_species_data
def get_tree_suitability(species):
    '''
    Read the tree_species data file and check suitability of a given 
    species. 

    Parameters
    ----------
    species : str
        the species of the tree to check

    Returns
    -------
    None, None
    or
    suitability and species : tuple(str, str)

    See Also
    --------
    locate_file_in_directory
    '''
    species = species.lower().strip().replace(' ', '')
    file = locate_file_in_directory('tree_species.txt', file_type='text') 
    try:
        with open('tree_species.txt') as tree_species_file:
            # Iterates through each line in dataset
            # next(tree_species_file)
            for line in tree_species_file:
                clean_line = line.strip()
                squished_line = clean_line.replace(' ', '')
                items_with_spaces = clean_line.split(',')
                items_no_spaces = squished_line.split(',')
                # Defining at what index each item is
                variety_with_spaces = items_with_spaces[0]
                variety = items_no_spaces[0].lower()
                suitability = items_no_spaces[1]
                #
                if species in variety:
                    return (suitability, variety_with_spaces)
                # End loop.
            if species not in variety:
                return (None, None)
            # Close file.
        # End try statement.
    except IndexError as index_error:
        stmt = 'indexerror'
        print("IndexError: The file 'tree_species.txt' has been corrupted")
        return stmt
    # End function.

# Access my_tree_data
def check_tree_number(tree_number, trees_in_file):
    '''
    Compare the tree number to the number of trees in the data file.
    '''
    if tree_number > trees_in_file and tree_number != 0:
        stmt = (
            f'ERROR! '
            f'You entered ({tree_number}). \nThere are only '
            f'{trees_in_file} trees in the data file. '
            )
        return stmt
    if tree_number < 1:
        stmt = (
            f'ERROR! '
            f'You entered ({tree_number}). \n'
            f'This tree number does not exist. '
            )
        return stmt
    if tree_number <= trees_in_file:
        stmt = (f'...getting tree ({tree_number}) data...')
        return stmt
    
def get_my_tree_data(tree_number: int):
    '''
    Read the my_tree_data file and return the list of a given tree's
    attributes. 

    See Also
    --------
    check_tree_number
    
    '''
    try:
        with open('my_tree_data.txt') as my_tree_data_file:
            trees_in_file = len(my_tree_data_file.readlines())-1

        statement = check_tree_number(tree_number, trees_in_file)

        with open('my_tree_data.txt') as my_tree_data_file:
            next(my_tree_data_file)
            # Iterate through each line in dataset.
            for line in my_tree_data_file:
                items = line.strip().split(', ')
                tree_str_splt_from_num = items[0].split('_')

                tree_num_in_data = int(tree_str_splt_from_num[1])
                variety = items[1]
                suitability = items[2]
                circum = float(items[3])
                diameter = float(items[4])
                radius = float(items[5])
    
                if 'ERROR!' in statement:
                    print(statement)
                    return None
                
                if tree_number == tree_num_in_data:
                    print(statement)
                    data = [
                        tree_num_in_data, 
                        variety, suitability, 
                        circum, diameter, radius
                    ]
                    return data
                # End loop.
            # Close file.
        # End try statement.
    except IndexError as index_error:
        print(
            "\nIndexError: An error occured when trying to read "
            "the 'my_tree_data' file. \nIt is possible that there "
            "are unintended extra lines. Please delete the file \n"
            "from your system and reboot the program. \n"
        )
        quit()
    except FileNotFoundError as file_not_found:
        print(
            f"\nFileNotFound Error: The file 'my_tree_data.txt' could not " \
            "The program was trying to extract information from file. "
            "\nPlease ensure it has not been moved to a different " \
            "directory, or deleted. \n"
        )
    # End function.

def get_my_tree_variety(tree_number: int):
    '''
    See Also
    --------
    - get_my_tree_data 
        - check_tree_number
    
    '''
    data = get_my_tree_data(tree_number)
    if data is None:
        variety = 0
    if data is not None:
        variety = data[1]
    return variety

def get_my_tree_radius(tree_number: int):
    '''
    See Also
    --------
    - get_my_tree_data 
        - check_tree_number
    
    '''
    data = get_my_tree_data(tree_number)
    if data is None:
        return 0
    if data is not None:
        radius = data[5]
        return radius
    return None

def get_my_tree_diameter(tree_number: int):
    '''
    See Also
    --------
    - get_my_tree_data 
        - check_tree_number
    
    '''
    data = get_my_tree_data(tree_number)
    if data is None:
        return 0
    if data is not None:
        diameter = data[4]
        return diameter
    return None

#endregion


#region Functions- Geometry (11)
#--------------------------
# Simple Math functions
def calculate_diameter(circumference):
    '''
    Get the diameter of a circle from it's circumference.
    '''
    diameter = circumference / math.pi
    return diameter

def calculate_radius(diameter):
    '''
    Get the radius of a circle from it's diameter.
    '''
    radius = diameter / 2
    return radius

# Creating Trees Functions
def calculate_distance_between_tree_centers(tree_a, tree_b, distance_bark):
    '''
    Find the distance between the centers of two trees.
    '''
    r_a = get_my_tree_radius(tree_a)
    r_b = get_my_tree_radius(tree_b)
    dc_a_to_b = r_a + distance_bark + r_b
    return dc_a_to_b

def get_xypoint_on_circle(r, h, k, degrees):
    '''
    Return an xypoint on a circle at its radius at a given degree.
    '''
    radians = (degrees) * (math.pi / 180)
    y = r * math.cos(radians) + k
    x = r * math.sin(radians) + h
    return (x, y)

def find_tree_center_xypoint(
        starting_coordinates: tuple,
        starting_tree: int, tree_to_plot: int,
        distance_bark: float, bearing
    ):
    ''' 
    Find the center coordintates (x, y) of a tree(circle).

    This function uses the bearing angle measured from the 
    starting_tree to the tree_to_plot.
    *Calls calculate_distance_between_tree_centers.
    *Calls get_xypoint_on_circle.
    Where h = starting x point and k = starting y point, this
    function assumes North is a line x = h with direction y >= k

    Parameters
    ----------
    starting_coordinates : (h, k). These are the coordinates
        from which the bearing was taken. Typically (0, 0) since
        starting_tree is generally plotted with center of (0, 0).
    starting_tree : Tree whos center point is the
            starting_coordinates. Passes tree # from my_tree_data
            as the value.
    bearing : Bearing in degrees.
    distance : distance in inches from bark to bark

    Return
    ------
    Point: tuple

    - get_xypoint_on_circle 
    - calculate_distance_between_tree_centers 
        - get_my_tree_radius 
            - get_my_tree_data 
                - check_tree_number

    '''
    # unpack tuple from first parameter
    h, k = starting_coordinates
    #
    distance_between_centers = calculate_distance_between_tree_centers(
                                    starting_tree,
                                    tree_to_plot,
                                    distance_bark
                                )
    # Pass distance between centers as radius(r) of circle.
    # Pass starting coordinates as (h, k).
    # Pass bearing in degrees as degrees.
    (x, y) = get_xypoint_on_circle(distance_between_centers, h, k, bearing)
    center_point = (x, y)
    # print('    RETURN center_point \n')
    return center_point

def create_circle(tree_number: int, center_point: tuple):
    '''
    Generate an array of xypoints for a circle with a defined radius. 

    Equation for a circle
    (x − h) ** 2 + (y − k) ** 2 = r ** 2

    See Also
    --------
    - get_xypoint_on_circle
    - get_my_tree_radius
        - get_my_tree_data
            - check_tree_number
    '''
    # ------- SOLVE for x and y --------
    h, k = center_point
    r = get_my_tree_radius(tree_number)
    #
    xvalues = []
    yvalues = []
    for degree in range(0, 360 + 1):
        (x, y) = get_xypoint_on_circle(r, h, k, degree)
        xvalues.append(x)
        yvalues.append(y)
        # print(f'{degree}: {x},{y}')
    xpoints = np.array(xvalues)
    ypoints = np.array(yvalues)
    # print('    RETURN: circle_coordinates \n')
    return (xpoints, ypoints)

# Checking Triangulation, trigonomic functions
def check_if_real_triangle(adj, opp, hyp):
    '''
    Test that 3 connected lengths form a right triangle. 

    This function uses the equation for a right triangle to
    ensure that 3 side lengths(adjacent, opposite, hypotenuse) 
    make a right triangle.  
    '''
    # acceptable error margin of 2% to 5% for surveying. 
    low_end_tolerance = 2
    max_tolerance = 5
    percentage_error = (abs(hyp**2 - (adj**2 + opp**2)) 
                        / hyp**2 ) * 100
    
    if percentage_error < low_end_tolerance:
        print(f' Program note~ triangulates a perfect right triangle! ')
        print(f'\nThe measurements have a {percentage_error:.2f}% '
              'error, which falls \nwithin the acceptable error '
              'tolerance of 2% to 5%. ')
        return True, percentage_error

    if low_end_tolerance <= percentage_error <= max_tolerance:
        print(' Program note~ triangulation is acceptable. \n')
        print(f'\nThe measurements have a {percentage_error:.2f}% '
              'error, which falls within the acceptable error '
              'tolerance of 2% to 5%. ')
        return True, percentage_error
    
    if  percentage_error > max_tolerance:
        print(f'\nThe measurements have a {percentage_error:.2f}% '
              'error, which DOES NOT fall \nwithin the acceptable '
              'error tolerance of 2% to 5%. ')
        return False, percentage_error

def get_right_triangle_sides_from_coordinates(x1, y1, x2, y2):
    '''
    Use the distance between two points formula to calculate the length
    of the sides of a right triangle. 
    
    For (X1, Y1) (X2, Y2),
    D = math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2).

       (x1,y1)
         |\
         | \
         |  \
         |   \
         |____\
    (x1,y2)   (x2,y2)

    Opposite side of triangle is distance between (x1, y1) (x1, y2)
    Adjacent side of triangle is distance between (x2, y2) (x1, y2)
    Hypotenuse of triangle is distance between (x1, y1) (x2, y2)

    Parameters:
        x1 : x-value of first point (x1, y1)
        y1 : y-value of first point (x1, y1)
        x2 : x-value of second point (x2, y2)
        y2 : y-value of second point (x2, y2)

    Returns:
        opp, adj, hyp: tuple(float, float, float)
            Length of opposite side, adjacent side, and hypotenuse. 
    '''
    opp = math.sqrt((x1 - x1)**2 + (y2 - y1)**2)
    adj = math.sqrt((x2 - x1)**2 + (y2 - y2)**2)
    hyp = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return opp, adj, hyp

def get_obtuse_triangle_sides_from_coordinates(x1, y1, x2, y2, x3, y3):
    '''
    Use the distance between two points formula to calculate the length
    of the sides 1_2, 1_3, 2_3 of an obtuse triangle. 

    For (X1, Y1) (X2, Y2),
    D = math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2).
    side 1_2: distance between (x1, y1) (x2, y2)
    side 1_3: distance between (x1, y1) (x3, y3)
    side 2_3: distance between (x2, y2) (x3, y3)

    Parameters:
        x1 : x-value of first point (x1, y1)
        y1 : y-value of first point (x1, y1)
        x2 : x-value of second point (x2, y2)
        y2 : y-value of second point (x2, y2)
        x3 : x-value of third point (x3, y3)
        y3 : y-value of third point (x3, y3)

    Returns:
        side lengths : tuple(float, float, float)
            The length of side a, length of side b, length of side c.
    '''
    s_1_2 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    s_1_3 = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)
    s_2_3 = math.sqrt((x3 - x2)**2 + (y3 - y2)**2)
    return s_1_2, s_1_3, s_2_3

def use_law_of_cosines_to_find_angles(a, b, c, angle=''):
    '''
    Find inner angles alpha, beta, gamma given sides a, b, c of an
    oblique triangle.

    a**2 == b**2 + c**2 - (2*b*c)*math.cos(alpha)
    b**2 == a**2 + c**2 - (2*a*c)*math.cos(beta)
    c**2 == a**2 + b**2 - (2*a*b)*math.cos(gamma)
    math.cos(alpha) == (b**2 + c**2 - a**2) / (2*b*c)
    math.cos(beta) == (a**2 + c**2 - b**2) / (2*a*c)
    math.cos(gamma) == (a**2 + b**2 - c**2) / (2*a*b)

    Parameters:
        a: side a (oppisite to angle alpha)
        b: side b (opposite to angle beta)
        c: side c (opposite to angle gamma)
        angle: 'alpha' 'beta' or 'gamma'. Default is '' which.
    Returns:
        alpha in degrees: float
            if angle is 'alpha'
        beta in degrees: float
            if angle is 'beta'
        gamma in degrees: float
            if angle is 'gamma'
        (alpha, beta, gamma) in degrees: tuple(float, float, float)
            if angle is default ''.
    '''
    angle_alpha = math.acos((b**2 + c**2 - a**2) / (2*b*c))
    angle_beta = math.acos((a**2 + c**2 - b**2) / (2*a*c))
    angle_gamma = math.acos((a**2 + b**2 - c**2) / (2*a*b))
    #
    angle_alpha = math.degrees(angle_alpha)
    angle_beta = math.degrees(angle_beta)         
    angle_gamma = math.degrees(angle_gamma)
    if angle.lower() == 'alpha':
        return angle_alpha
    if angle.lower() == 'beta':
        return angle_beta
    if angle.lower() == 'gamma':
        return angle_gamma
    else:
        return angle_alpha, angle_beta, angle_gamma   

def use_cosines_to_check_3_trees(tree_a_center_point:tuple, 
                                 tree_b_center_point:tuple,
                                 tree_c_center_point:tuple, 
                                 tree_a:int, tree_b:int, tree_c:int):
    '''
    Test if distances between 3 xypoints yield inner angles with a
    sum of 180 degrees.

    This function calls the use_law_of_cosines_to_find_angles 
    function to return the acute angles (in degrees) of a triangle 
    that has side lengths equal to the distances between trees.  
    The vaules returned are converted to degrees and their sum
    is compared to the excpected sum of 180 degrees.
    The distances in this case are the distances bewteen the xy points
    marking the center of the trees.
    '''
    x1, y1 = tree_a_center_point
    x2, y2 = tree_b_center_point
    x3, y3 = tree_c_center_point
    s_a, s_b, s_c = get_obtuse_triangle_sides_from_coordinates(x1, y1, 
                                                               x2, y2, 
                                                               x3, y3)
    alpha, beta, gamma = use_law_of_cosines_to_find_angles(s_a, s_b, s_c)
    angle_sum = alpha + beta + gamma
    if angle_sum < 170 or angle_sum > 190:
        print('Program Note ~ upon checking all of the measurements, '
              'one the bearings between three trees may be inaccurate '
              'to plus or minus a few degrees. ')
    if 170 < angle_sum < 190:
        print(f'..Trees {tree_a} > {tree_b} > {tree_c} '
              'create an ideal layout')
    
#endregion


#region Functions- Convert (3)
#-------------------------
def convert_inches_to_feetinches(inches: float, d: int, p=False):
    '''
    Convert inches to feet and inches.

    This function converts inches to feet inches by converting to
    feet, then using math.modf() to parse the decimal value from the 
    integer value, then converting the decimal value to more percise units,
    and continues this process to get a percision of a fraction of inches.

    Because the denominator can be specified, if it's percision is 
    less than the that of the inches argument after conversion, then
    the fractional inches returned, if any, will be off.

    Parameters
    ----------
    inches : float
        Inches to be converted.
    d : int
        Denominator value of inch fraction. The desired percision. 
    p : bool, default False, meaning function returns (int, float, int).
        If True, then function returns values in a sentance str instead.

    Returns
    -------
    ft_int : int
        Whole number feet.
    int_in : int
        Whole number inches.
    inch_numerator : int
        Whole number inches, the numerator of inch an fraction
        where d is denominator.
    or
    print_stmt : str
        Statement containing ft, inches, and inches fraction.

    1. When all values are not 0, print all values.
        '7 ft' + ' ' + '6 ' + '3/4 ' + 'inches' is '7 ft 6 3/4 inches'
    2. When fractional inches is 0 and int inches is not 0,
        '7 ft' + ' ' + '6 ' +   ''   + 'inches' is '7 ft 6 inches'
    3. When fractional inches is not 0 and int inches is 0.
        '7 ft' + ' ' +  ''  + '3/4 ' + 'inches' is '7 ft 3/4 inches'
    4. When 0 feet, don't print feet.
        ''  + ' ' + '6 ' + '3/4 ' + 'inches' is ' 6 3/4 inches'
    
    See Also
    --------
    round_num : Round a number to a number of decimal points.
    convert_feetinches_to_nches: convert a measurement in feet and
                                    inches to feet.
   
    Examples
    --------
    import math

    >>> my_ans = convert_inches_to_feetinches(435.75, 8)
    >>> print(my_ans)
    (33, 3, 6)

    With the ``p`` parameter, we can change what is returned

    >>> my_ans = convert_inches_to_feetinches(435.75, 8, True)
    >>> print(my_ans)
    36 ft 3 6/8 inches
    '''
    # Convert to feet as a floating number.
    feet = inches / 12
    # Seperate fractional and integer parts of feet.
    ft_frct, ft_int = math.modf(feet)
    # Convert fractional part of feet to inches
    inch = ft_frct * 12
    # Seperate fractional and integer parts of inches.
    inch_frct, inch_int = math.modf(inch)
    # Calculate and round the numerator of the fractional part of 
    # inches to the denominator. Call round_num(). If 0.5, round up.
    inch_numerator = round_num((inch_frct * d))
    # Verify units are target number types. 
    ft_int = int(ft_int)
    inch_int = int(inch_int)
    inch_numerator = int(inch_numerator)
    # Define feet and fractional inches strings for a printed statement.
    inch_fraction_prnt = f'{inch_numerator}/{d} '
    feet_prnt = f'{ft_int} ft'
    # For both cases numerator = 0 or numerator = denominator,
    # dont print fractional inches string. 
    # However, only when the numerator is not 0 in above cases, does 
    # the fractional inches = 1 inch. In this case, add 1 inch to 
    # int inches, and redefine the numerator as 0. 
    if abs(inch_numerator) == abs(d) or abs(inch_numerator) == 0:
        inch_fraction_prnt = ''
        if abs(inch_numerator) > 0:
            inch_numerator = 0
            inch_int = inch_int + 1
    # Now define the inches string to be used in a printed statement.
    inch_prnt = f'{inch_int} '
    # Handle cases not yet handled for how a statement is displayed:
    # When there is 0 feet, don't print feet.
    if ft_int == 0:
        feet_prnt = ''
    # When there are fractional inches and 0 int inches, 
    # don't print int inches.
    if inch_fraction_prnt != '' and inch_int == 0:
        inch_prnt = ''
    # If the p parameter is true, return a measurement statement.
    if p is True:
        ftin_str = (
            f'{feet_prnt} {inch_prnt}{inch_fraction_prnt}inches'
        )
        return ftin_str
    # If the p parameter is False, return a tuple of values.
    if p is False:
        return ft_int, inch_int, inch_numerator

def convert_feetinches_to_inches(feet: int, inches: float):
    '''
    Convert a measurement of feet and inches to inches.

    Parameters
    ----------
    feet: int
        The part of the measurement in feet.
    inches: float
        The part of the measurement in inches.

    Returns
    -------
    float
        The measurement in inches.

    See Also
    --------
    convert_inches_to_feet_inches : convert inches to feet and inches.

    '''
    converted_inchs = feet * 12
    total_inches = converted_inchs + inches
    return total_inches

def round_num(n, decimals=0):
    '''
    Return a rounded number.

    This function address the common error of python's
    standard round() function. Numbers are rounded up to
    next whole value if value is at half.

    Parameters
    ----------
    n : int or float
        Number to be rounded.
    decimals : int
        Decimals to round to.

    Returns
    -------
    int or float
        The number rounded to the decimal point
    '''
    multiplier = 10**decimals
    return math.floor(n * multiplier + 0.5) / multiplier

#endregion


#region Functions- Measures (2)
#--------------------------
def return_required_measurments(number_of_trees: int):
    '''
    Return measurements required based on the number of trees.

    Returns a tuple with two elements:
    1. Distance measurements:
        - List of tuples (tree_number_a, tree_number_b) representing 
        distances between tree barks.
        - Tuple containing None if no measurements are needed.
        - Integer 0 if number_of_trees is invalid.
    2. Bearing measurements:
        - List of tuples (tree_number_a, tree_number_b) representing 
        bearings between tree barks.
        - Tuple containing None if no bearings are needed.
        - Integer 0 if number_of_trees is invalid.
    
    Parameters
    ----------
    number_of_trees : int
        The number of trees in the building area a of future treehouse.
        
    Returns
    -------
    tuple
        Distance and bearing measurements.
    
    See Also
    --------
    format_req_measurements_for_ui : Return formated strings for ui.

    '''
    # Create tuples (tree_number_a, tree_number_b) that represent
    # required measurments between (a, b).
    # ======= 1 trees (0 measurements) ======
    if number_of_trees == 1:
        required_distance_measurements = [(None, None)]
        required_bearings_measurements = [(None, None)]
    # ======= 2 trees (1 measurement) =======
    if number_of_trees == 2:
        required_distance_measurements = [(1, 2)]
        required_bearings_measurements = [(1, 2)]
    # ======= 3 trees (3 measurements) ======
    if number_of_trees == 3:
        required_distance_measurements = [
            (1, 2), (1, 3), (2, 3)
        ]
        required_bearings_measurements = [
            (1, 2), (1, 3)
        ]
    # ======= 4 trees (6 measurements) ======
    if number_of_trees == 4:
        required_distance_measurements = [
            (1, 2), (1, 3), (1, 4),
            (2, 3), (2, 4),
            (3, 4)
        ]
        required_bearings_measurements = [
            (1, 2), (1, 3), (1, 4)
        ]
    # ======= 5 trees (10 measurements) =====
    if number_of_trees == 5:
        required_distance_measurements = [
            (1, 2), (1, 3), (1, 4), (1, 5),
            (2, 3), (2, 4), (2, 5),
            (3, 4), (3, 5),
            (4, 5)
        ]
        required_bearings_measurements = [
            (1, 2), (1, 3), (1, 4), (1, 5)
        ]
    if 1 > number_of_trees or number_of_trees > 5:
        print("\nError: Invalid argument for parameter `number_of_trees'. " 
              f"Must be between 1 and 5. \n{number_of_trees} is not valid. ")
        required_distance_measurements = 0
        required_bearings_measurements = 0
    return (required_distance_measurements, required_bearings_measurements)

def format_req_measurements_for_ui(measurements):
    '''
    Format the measurements returned by return_required_measurments.
   
    This function puts the measurments the user needs to take in 
    messages to display to them. 

    Parameters
    ----------
    measurements : list[tuple(tree number, tree number)]
        Distance or Bearing measurements.

    Returns
    -------
    prnt : list of str, str, or str
        List containing statements for each measurement,
        a statement saying no measurements are needed,
        or a statement saying that an error occured. 

    See Also
    --------
    return_required_measurments : Return bearing and distance
                                    measurements for user to take.
    '''
    try:
        prnt = []
        for ta, tb in measurements:
            if ta is None or tb is None:
                prnt = 'None needed.'
                break
            else:
                prnt.append(f'TREE_{ta} to TREE_{tb}')
    # These errors handle the exceptions that occur when the va
    except IndexError as index_err:
        prnt = 'Error: None'
    except TypeError as type_err:
        prnt = 'Error: None'
    return prnt

#endregion


#region Functions- OS/files (2)
#--------------------------

def locate_file_in_directory(filename, file_type, folder='', output=''):
    '''
    Return the path of a text or image file in the directory. 
    '''
    # Get the current working directory and the current directory where
    # file.py is located.
    cwd = os.getcwd()
    py_directory = os.path.dirname(__file__)
    # If the file is located directly in the directory,
    # join it to the directory path.
    if folder == '':
        file_path = os.path.join(py_directory, filename)
    # If the file is located in a folder within the directory,
    # join it and the file to the directory path.
    if folder != '':
        folder_file = f'{folder}/{filename}'
        file_path = os.path.join(py_directory, folder_file)
    # Seperate the suffix(extenstion) from the file name, if available.
    if '.' in filename:
        file_suffix = file_path.rsplit('.', 1)[-1]
        io_uni_stmt = f"\n'{file_suffix}' is not a valid {file_type} file.\n"
    if '.' not in filename:
        io_uni_stmt = 'Note: The file extension could not be retrieved'
    try:
        # === File type is text ===
        if file_type == 'text':
            # Try to read the text file.
            with open(file_path, 'r') as file:
                text_content = file.read()
            if output == 'text':
                return text_content
            elif output == 'path' or output == '':
                return file_path
            else:
                print('\nInvalid argument for parameter `output`')
        # === File type is image ===
        if file_type == 'image':
            # Try to read the image file.
            img = mpimg.imread(file_path)
            if output == 'text':
                print(
                    f'\nInvalid argument `text` for parameter '
                    '`output` of image type file. '
                )
                return file_path
            elif output == 'path' or output == '':
                return file_path
            else:
                print('\nInvalid argument for parameter `output`')
        # === File type is not text or image ===
        else:
            print('Invalid file type parameter. Must be `image` or `text`. ')
            # End if statements.
        # End try statement.
    except FileNotFoundError as file_not_found:
        print(
            f"\nFileNotFound Error: The file '{filename}' could not "
            "be found.\nPlease ensure it has not been moved to a different "
            "directory, or deleted. \n"
            f"\nCurrent working direcory: {cwd} \n"
            f"Directory where `.py` is located: {py_directory}"
        )
        quit()
    except IOError as image_err:
        print(
            f"IO Error: Unable to open '{filename}'. "
            f"\npath: {file_path}\n "
            f"\n{io_uni_stmt}"
        )
        quit()
    except UnicodeDecodeError as txt_err:
        print(
            f"\nUnicodeDecode Error: Unable to open '{filename}'. "
            f"\npath: {file_path}\n "
            f"\n{io_uni_stmt}"
        )
        quit()
    except SyntaxError as syntax_err:
        print(f'\nSyntaxError: not a valid image file. May be corrupt. '
              f'\n{file_path}')

def check_if_file_exists(filename):
    '''
    Return if a given file name exists.
    '''
    py_directory = os.path.dirname(__file__)

    # Specify path of file
    fpath = f'{py_directory}/{filename}'
    # Check whether the specified 
    # path exists or not 
    isExist = os.path.exists(fpath) 

    if isExist is True:
        print(f'\n{filename} already exists! \n{fpath}')
    if isExist is False:
        pass
    return isExist

#endregion


#region Functions- UI (2)
#--------------------
def get_number_type_from_user(input_prompt):
    '''
    Get a number from the user.

    Parameters
    ----------
    input_prompt : str
        The prompt that asks the user for a number.

    Returns
    -------
    number : float
        The number entered by the user. 
    '''
    while True:
        try:
            text = input(f'{input_prompt}')
            number = float(text)
            break
        except ValueError as value_str_to_float_error:
            print(f"\nError: Invalid Number Entry. "
                  f"'{text}' is not a number. ")
    return number

def get_string_from_user(input_prompt, response_option_1=None, 
                         response_option_2=None):
    '''
    Get a text string from the user.

    Parameters
    ----------
    input_prompt : str
        The prompt that asks the user for a string value.
    response_option_1 : str, default None
        An optional argument in cases where you want to specify only
        a certain response is an acceptable one.
    response_option_2 : str, default None
        A a second optional argument in cases where you want to specify 
        only a certain response is an acceptable one.

    Returns
    -------
    text : str
        The text string entered by the user. 
    '''
    # Define 'response_option' as 'opt' to preserve line space.
    opt1 = response_option_1
    opt2 = response_option_2
    while True:
        text = input(f'{input_prompt}')
        try:
            number = float(text)
            print(f"\nError: Invalid Text Entry. '{number}' "
                  "You entered a number. ")
        except ValueError as value_str_to_float_error:
            pass
        finally:
            # If no response arguments were passed:
            if (opt1 is None) and (opt2 is None):
                break
            elif ((opt1 is not None) and (opt2 is not None)
                    and (text == opt1 or text == opt2)):
                break
            # If two response arguments were passed and input is not either:
            elif ((opt1 is not None) and (opt2 is not None)
                    and (text != opt1 or text != opt2)):
                print(f"\nInvalid Entry: must be '{opt1}' or '{opt2}' ")
            # If a single argument was passed as option 1:
            elif (opt2 is None and opt1 is not None and text != opt1):
                raise ValueError(
                    f"\nError in 'get_string_from_user': single arg '{opt1}' "
                    f"\n,'response_opts' must have two arguments or none. "
                )
            # If a single argument was passed as option 2:
            elif (opt1 is None and opt2 is not None and text != opt2):
                raise ValueError(
                    f"\nError in 'get_string_from_user': single arg '{opt2}' "
                    f"\n,'response_opts' must have two arguments or none. "
                )
            # End try except finaly
        # End while loop
    return text

#endregion


# region Funcs- UI specific (3)
#------------------------------
def get_number_of_trees_from_user():
    '''
    Get the number of trees in the building site 
    of the future treehouse. 
    '''
    ans = ''
    while True:
        try:
            print()
            number_words = ['zero', 'one', 'two', 'three', 'four']
            number_of_trees = input(
                'How many trees are in the build area? (min 1, max 5): '
            )
            if number_of_trees.lower() in number_words:
                i = number_words.index(number_of_trees)
                num_ans = input(f'Did you mean..{i}..?(yes/no) ')
                if num_ans.lower() == 'yes':
                    number_of_trees = i
                    break
                if num_ans.lower() == 'no':
                    print('\nPlease restart the program and try again. ')
                    quit()
            elif int(number_of_trees) > 5:
                print('The number of trees entered exceeds the limit.')
                ans = input(
                    'Would you like to try again with fewer trees? '
                    '(yes/no/exit): '
                )
            elif int(number_of_trees) <= 0:
                print('The number of trees must be 1 or greater.')
                ans = input(
                    'Would you like to try again with more trees? '
                    '(yes/no/exit): '
                )
            else:
                number_of_trees = int(number_of_trees)
                break
        except ValueError as value_error:
            print('Error: Invalid Entry. Input must be an integer number. ') 

    if ans.lower() == 'no' or ans.lower == 'exit':
        quit()
    if ans.lower() == 'yes':
        pass
    return number_of_trees

def get_species_from_user(tree, program_close_statement):
    '''
    Get the species of a tree from the user and validate it.

    Parameters
    ----------
    tree : int
        The number corresponding to the tree in the group of trees.
    program_close_statement : str
        A statement to display to the user when they would like to
        exit the running program. 

    Returns
    -------
    suitability : str
        The suitability of the species of tree for a treehouse.
    species_pretty: str
        The full species name of the tree, in uppercase and with 
        appropriate spacing.

    See Also
    --------
    get_string_from_user
    get_tree_suitability
        locate_file_in_directory

    Notes
    -----
    get_string_from_user is not called in the case of asking user for
    the species because the code handles ANY input from the user that 
    is outside of the text strings contained in the tree_species file.
    '''
    #reenter_species = ''
    #preference = ''
    while True:
        species = input(f'\nWhat is the species of {tree}?: ')
        suitability, species_pretty = get_tree_suitability(species)
        if suitability is not None and len(species) >= 3:
            break
        if suitability is None or len(species) <= 2:
            print(
                '\nHmmm. It looks like the tree species you entered '
                'is not in our data set. '
            )
            reenter_species = get_string_from_user(
                'Would you like to re-enter the information? (yes/no) ',
                response_option_1='yes',
                response_option_2='no'
            )
            if reenter_species == 'no':
                preference = get_string_from_user(
                    '\nWould you like to continue with this tree even '
                    'though its species may or may not be suitable? '
                    '(continue/exit program) ',
                    response_option_1='continue',
                    response_option_2='exit program'
                )
                if preference == 'exit program':
                    print(program_close_statement)
                    quit()
                if preference == 'continue':
                    suitability = 'unknown'
                    break
                # End nested if statement
            # End if statement
        # End while loop
    return suitability, species_pretty

def save_unique_user_data_text_file(user_name, filename):
    '''
    Save user's tree data as a unique text file. 

    See Also
    --------
    get_string_from_user
    check_if_file_exists
    locate_file_in_directory

    '''
    ans_sure = ''
    ans = ''
    f_path = locate_file_in_directory(filename, file_type='text')
    prompt_1 = ('Would you like to save the information you entered today '
                'as a text file? (yes/no)')
    prompt_2 = ('Are you sure you dont want to save your tree data? \n'
                '{choosing yes will cause all information to be lost!} '
                '(yes/no)')
    try:
        # Ask the user if they would like to save their tree data.
        ans = get_string_from_user(prompt_1, 'yes', 'no')
        # If the user says no, ask them if they are sure.
        if ans.lower() == 'no':
            ans_sure = get_string_from_user(prompt_2, 'yes', 'no')
        # If the user wants to save their data, create a new file
        if ans.lower() == 'yes' or ans_sure.lower() == 'no':
            print('\n...Saving file...')
            # Define the new file name.
            new_file_name = (f"{user_name.lower()}'s_{filename}")
            # Check if the name exists and if it does, loop until user 
            # enters a unique name that does not.
            while check_if_file_exists(new_file_name) is True:
                filename = input(
                    '\nPlease enter a unique name to save file as: '
                )
                # End while loop.
            # Open the original file and copy its contents to new file.
            with open(filename, 'r') as original_file:
                with open(new_file_name, 'at') as new_file:
                    for line in original_file:
                        if line !=0:
                            print(line, file=new_file)
                    # Close new file.
                # Close original file.
            print(f"\n...File saved as {new_file_name}... ")
        # If user does not want to save their data, tell them it was
        # not saved.
        if ans == 'no' or ans_sure == 'yes':
            print('\n...file was not saved...')
        return None
        # End try statement.
    # If the argument passed for filename is not valid.
    except OSError as opperating_sys_error:
        print(f"\nError: '{filename}' is not a valid file name. ")
        quit()

#endregion


#region Functions- not used (1)
#--------------------------

# Math standard library has this function!
def convert_degrees_and_radians(angle, in_units='degrees'):
    '''
    Get the value of an angle in its opposite units.

    This function uses the conversion formula between degrees and radians.
    If the angle is degrees, it converts to its value in radians.
    If the angle is radians, it converts to its value in degrees.
    angle_in_degrees = angle_in_radians * 180/pi

    Parameters
    ----------
    angle : int or float
        Measurement in radians or degrees.
    units : int or float {default 'degrees', 'radians'}
        The units of the angle arguement.

    Returns
    -------
    float or None
        angle_in_degrees or angle_in_radians or None
    '''
    if in_units == 'degrees':
        angle_in_radians = (angle) * (math.pi/180)
        return float(angle_in_radians)
    if in_units == 'radians':
        angle_in_degrees = (angle) * (180/math.pi)
        return float(angle_in_degrees)
    else:
        return None

#endregion

# region Call to main
if __name__ == '__main__':
    main()
