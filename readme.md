[![license - apache 2.0](https://img.shields.io/:license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# Ros test generator

Assuming a [ROS model][ros_model] has been extracted from a package, this component will generate the appropriate pattern specification file for the [ROS package generator][ros_pkg_gen], to enable the creation of a test package.

[ros_model]: https://github.com/ipa320/ros-model
[ros_pkg_gen]: https://github.com/tecnalia-advancedmanufacturing-robotics/ros_pkg_gen

**Author & Maintainer**: Anthony Remazeilles, anthony.remazeilles@tecnalia.com

**Affiliation** : Tecnalia Research and Innovation, Spain

**License**: This project is under the Apache 2.0 License.

## Getting started

### Prerequisites

We assume [`ROS`][ros] is installed on the machine.
Code is developed and tested so far under `ROS kinetic`.

[ros]: http://www.ros.org/

### Installing

The installation procedure follows the standard operations as any ROS package does.

```shell
# Assuming ~/catkin_ws is the workspace in which the repository has been downloaded
cd ~/catkin_ws
sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro $ROS_DISTRO
```

### Usage

We assume a package has been analysed using [IPA320 tools][ros_model], and that a `.ros` model file is available for the node of interest:

```shell
# go to the workspace root
roscd
rosrun ros_test_generator generate_xml -m ../ros_model_parser/resources/cob_light.ros -o check.xml
rosrun package_generator generate_package check.xml
catkin build
source devel/setup.zsh
```

The first operation parse the ROS model and interact with you to complete the test definition.
The second operation generates the testing package.

> [!WARNING]
> the generated test files need to be open to check and adjust the testing configuration.
> This is particularly the case if a service or a filter-like node is tested (to introduce input& output values in the test file)


## Acknowledgements

This development is supported by the European Union’s Horizon 2020 project [ROSIN][rosin_website].
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under
grant agreement No 732287.

The opinions and arguments expressed reflect only the author‘s view and reflect in no way the European Commission‘s opinions.
The European Commission is not responsible for any use that may be made of the information it contains.

[![ROSIN website][rosin_logo]][rosin_website]

[rosin_logo]: http://rosin-project.eu/wp-content/uploads/2017/03/Logo_ROSIN_CMYK-Website.png
[rosin_website]: http://rosin-project.eu/ "Go to website"
