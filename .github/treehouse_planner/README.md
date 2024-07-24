# :deciduous_tree: Treehouse Planner :evergreen_tree:

The Treehouse Planner is designed to assist you in the initial planning phase of building an amazing treehouse. Whether you're evaluating trees for suitability, assessing tree safety, or drafting accurate scaled layouts for platforms, beams, walls, and posts, this tool aims to streamline your treehouse construction process.

## Features

- **Tree Evaluation:** Assess the suitability of trees based on various criteria.
- **Tree Safety:** Evaluate tree safety factors to ensure stability and reliability.
- **Scaled Layout Planning:** Generate accurately scaled plans for treehouse platforms, beams, walls, and posts.
- **Visualization:** Visualize example tree platform layouts to inspire your designs.

## Project Structure

The project is structured as follows:

```bash
treehouse_planner/
├── pyproject.toml
├── README.md
├── tree_species.txt        (List of tree species)
├── treehouse_layout.py     (Main functionality module)
│── layout_images/          (Directory for layout images)
│   ├── 1_tree_platform_examples.png
│   ├── 2_tree_platform_examples.png
│   ├── 3_tree_platform_examples.png
│   ├── 4_tree_platform_examples.png
│   ├── 5_tree_platform_examples.png
│   └── tree_line.png
├── test_treehouse_layout.py (Test Module)
└── test_files/             (Directory for test files)
    ├── p_exists.png
    ├── p1_exists.png
    ├── t_exists.txt
    └── t1_exists.txt

will be added:
my_tree_data.txt
yourname_tree_layout.pdf
```

## Getting Started

Follow these steps to get started with the Treehouse Planner:

### Installation

Ensure you have Python 3.x and `pip` installed.

 **Install Dependencies:**

    pip install matplotlib
    pip install matplotlib-inline
    pip install ipython
    pip install pytest

## Usage

1. **Run the program:**

Ensure that you open folder `treehouse_planner` as the root directory
in VS Code. run the `treehouse_layout.py` script.

2. **Follow Program Instructions:**

The program will guide you through the steps for evaluating trees, assessing safety, and generating scaled layouts. 

>SAMPLE INPUTS

    Tree Species: [Red wood, Seqouia, Maple, Oak, Cedar],
    
    Tree Circumferences(in): [50.25, 56.5, 69, 72.25, 66]
    
    Distances(feet, inches):
        tree_1_to_2: (20, 0)
        tree_1_to_3: (15, 0)
        tree_1_to_4: (11, 7.9)
        tree_1_to_5: (8, 0)
        tree_2_to_3: (15, 0)
        tree_2_to_4: (23, 1.5)
        tree_2_to_5: (19, 9.5)
        tree_3_to_4: (10, 0)
        tree_3_to_5: (9, 7)
        tree_4_to_5: (5, 0)
        
    Bearings(degrees):
        tree_1_to_2: 161
        tree_1_to_3: 210
        tree_1_to_4: 251
        tree_1_to_5: 239

3. **Testing**

Ensure that you open folder `treehouse_planner` as the root directory
in VS Code. Run the `test_treehouse_draft.py` script.
