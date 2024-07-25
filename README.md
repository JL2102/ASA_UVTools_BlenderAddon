# JL's ASA Mesh Preparation and Toolkit

Welcome to the **Ark Survival Ascended Mesh Preparation and Toolkit**! This Blender add-on is designed to perform a series of operations on a specified mesh, making the mesh able to be used along side ASA's body morph modifications.

## Features

- **Working Version**: Works with Blender 3.6+ and Blender 4.0+
- **Remove LOD Assets**: Ensures that the Human Male TPV model only includes LOD0.
- **Rename Initial UV**: Renames the initial UV layer to 'DiffuseUV'.
- **Clear Bones**: Clears parent and deletes all armatures except 'ROOT_JNT_SKL'.
- **Manage UVs**: Deletes all UV layers except 'DiffuseUV'.
- **Transfer Data**: Transfers UV data from 'Human_Male_TPV_LOD0' to the selected mesh.
- **Set Armature**: Sets the armature to 'ROOT_JNT_SKL'.
- **Clean Up UVs**: Deletes all UV layers except 'DiffuseUV' and 'LightMapUV'.

## Installation for Open Source Contribution

To contribute to the development of **JL's ASA Mesh Preparation and Toolkit**, follow these steps to set up the project locally.

### Prerequisites

Ensure you have the following software installed:

- **Git** / **GitHub Desktop**: To clone the repository.
- **Python**: The version compatible with (Python 3.12+ for Blender 3.6+).
- **Blender**: Ensure you have Blender 3.6.0 or later installed.

### Clone the Repository

1. Open a terminal or command prompt.
2. Clone the repository from GitHub:

    ```sh
    git clone https://github.com/JL2102/ASA_UVTools_BlenderAddon.git
    ```

3. Or Use GitHub CLI:

    ```sh
    gh repo clone JL2102/ASA_UVTools_BlenderAddon
    ```

### Install Requirements

The project dependencies are listed in the `requirements.txt` file. Install them using pip:

1. Ensure you have pip installed. If not, install it by following the instructions [here](https://pip.pypa.io/en/stable/installation/).
2. Install the requirements:

    ```sh
    pip install -r requirements.txt
    ```
3. I also recommend installing the BPY Module [here](https://github.com/nutti/fake-bpy-module/).

    ```sh
    pip install fake-bpy-module
    ```

## Blender Installation

1. **Download the Add-on**: Clone or download this repository.
2. **Install in Blender**:
   - Open Blender.
   - Go to `Edit > Preferences > Add-ons`.
   - Click on `Install...` and select the downloaded `.py` file.
   - Enable the add-on by checking the box next to **ASA Mesh Preparation and Toolkit**.

## Usage

Once installed and enabled, follow these steps to use the toolkit:

1. **Open the Control Panel**:
   - Go to `View3D > Tools > Mesh Preparation Tools`.
   
2. **Select the Mesh**:
   - Use the `Select Mesh` dropdown to choose the mesh you want to operate on.

3. **Configure Operations**:
   - Expand the `Enable Operations` dropdown.
   - Check the operations you want to perform: `Remove LOD Assets`, `Rename Initial UV`, `Clear Bones`, `Manage UVs`, `Transfer Data`, `Set Armature`, and `Clean Up UVs`.

4. **Execute Operations**:
   - Click on `Execute Mesh Operations` to run the selected operations on the chosen mesh.

## Detailed Operations

### Remove LOD Assets (For the Human_Male_TPV)

Removes all LOD (Level of Detail) assets except for the LOD0 asset, ensuring a cleaner scene.

### Rename Initial UV

Renames the initial UV layer of the mesh to `DiffuseUV`.

### Clear Bones

Clears the parent and deletes all armatures except for the `ROOT_JNT_SKL` armature.

### Manage UVs

Deletes all UV layers except for `DiffuseUV`, ensuring that only the necessary UV layer is present.

### Transfer Data

Transfers UV data from `Human_Male_TPV_LOD0` to the selected mesh.

### Set Armature

Sets the armature to `ROOT_JNT_SKL`, ensuring that the mesh is rigged correctly.

### Clean Up UVs

Deletes all UV layers except for `DiffuseUV` and `LightMapUV`, cleaning up any unnecessary UV layers.

## Help

For more detailed information on each operation, click on the help icon in the control panel.

## Contributing

If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the GNU License. See the [LICENSE](LICENSE) file for details.

## Authors

- **JL** - Initial work

## Acknowledgments

We extend our heartfelt gratitude to the following individuals and communities for their invaluable contributions:

- **Mewsie**: For solving the initial steps and providing crucial insights.
- **Elkay**: For their unwavering support and invaluable suggestions.
- **The Blender Community**: For their abundant resources and continuous support.
- **Cliffan**: For the initial steps to solve this problem.


---



Copyright (C) 2024  JL

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

