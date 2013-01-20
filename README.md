# Po, a Windows package manager

Po is a command-line-oriented package manager for Windows. While it aims to
include a useful repository of open-source libraries and development tools, it
is currently most useful for managing your own projects.

Po is in early development. Most notably, it does not yet manage dependencies.

## Features

* Keeps environment variables like PATH and INCLUDE in sync with installed
  packages. Does not modify your system-wide environment variables.

* Designed from the ground up to support several versions or build
  configurations per project, and to let you choose which are active.

* Downloads and installs supported third-party packages.

* Define your own local packages to be managed alongside third-party ones.

* Supports source and binary packages.

* Can detect and manage pre-installed software that wasn't installed via Po.

## Installation

First, install [Python 2.7][python]. Once that is installed, open a command
window and run this command:

    C:\Python27\python -c "exec __import__('urllib2').urlopen('http://raw.github.com/robin-allen/po/master/Scripts/installer.py').read()"

If you didn't install Python to the default location you'll need to change
the ```C:\Python27\python``` part.

[python]: http://python.org/download/

The installer will ask you for two paths. I recommend you just press Enter
to use the default for both. The paths are:

* **Packages path**: This is where Po will install itself, and any packages you
  install via Po.

* **Site path**: This is where Po will look for your own custom packages.

Once the installer has finished running, it will give you the path of your
Po initialization file. You need to run this file in any command window you
intend to use Po in, so you might want to change your command prompt settings
to have it always run when you open a new window.

## Usage

Po keeps track of its packages in its own private environment. To use your
packages, you need to enter this environment by typing:

    po enter

Your command prompt will change to show you're in the environment. To leave
the environment, use the standard Windows command

    exit

You can get a full list of commands by doing ```po help``` and help on any
command with ```po help <command>```.

## Standard Packages

Po defines a list of so-called "Standard Packages" which it knows how to
download and install for you. You can install one of these packages with the
command

    po install <package-name>

There is currently no way to view or search the list of standard packages, and
the list is very short and fairly buggy.

To see what standard packages are available, look in the Recipes subfolder
inside Po's "Package Manager" folder.

## System Packages

Po defines a list of "System Packages" corresponding to software which it can
detect on your system. Po cannot install this software itself, but it can
add the relevant paths to your environment for you.

System packages are useful for managing multiple versions of tools like
Python and Microsoft Visual Studio; you can select which version you want
to be loaded into the command-line environment with ```po select``` and Po
will do the rest.

To see what system packages are available, look in the Recipes subfolder
inside Po's "Package Manager" folder.

## Site Packages

Site packages are defined by you and placed in your Site folder. You write
a ```package.py``` file and place it inside your package's folder to tell Po
how to set up the enviroment for that package. Site packages can be selected
and deselected like other packages, and will contribute to the enviroment, but
they cannot be automatically installed or uninstalled.

Po does not try to detect when you make changes to a site package; when you
do, you need to reload the environment with

    po load

## The Inventory

To see a list of all installed packages, run

    po inv

Each package is shown with its package ID and its human-readable name. Packages
which are selected are shown in a brighter font, and deselected packages are
shown in a darker font. Only selected packages contribute to the environment.

You can select or deselect a package by giving its ID to the ```po select```
and ```po deselect``` commands. When several packages have the same ID, as in
the case of multiple installed versions, you can specify which package you
mean by using package attributes, for example:

    po select msvs version=11.0

This would select Visual Studio 11.0 and deselect other versions, so that if
you ran a VS tool like ```cl.exe```, you'd get the VS 11.0 version.


