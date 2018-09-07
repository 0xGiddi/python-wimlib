> This is still somewhat a WIP, but has not yet been fully tested
>Found a bug? Please, open up an issue in the [issue tracker](https://github.com/0xGiddi/python-wimlib/issues)

## Wimlib python wrapper 
Manipulating WIM files is all fun and games until you need to script it or you are not on a Windows platform. Fortunately a great open-source library exists for creating, extracting, and modifying Windows Image Files (WIM). This library named [wimlib](https://wimlib.net) is excellent, and there really is no alternative to it.

This module/project provides python bindings for wimlib for scripting and automation of WIM file manipulation and deployment. The python wrapping allows for rapid scripting of tasks or just to have some fun.

You can find some examples using his module in the `/examples ` directory. More information about the structure and objects of this module will be added at a later time.

### Features
- Written for python 2.7+ with Python 3 in mind
- API wrapped with [cffi](https://cffi.readthedocs.io/en/latest/) for performance and comfort.
- Easy structure and neat layout for easy OOP approach.

### Implemented wimlib modules
- Global init/cleanup functions
- Error logging/printing functions
- Compression and Decompression functions
- Creating and opening WIMs (function w/ progress are a WIP)
- Retrieving WIM and Image information
- Mounting WIMs (fuse seems to exit the python process, you can mount with debug flag in a seprate hread to bypass this)
- Writing and overwriting WIMs

### Contributing
If you would like to help out this project, you can! There are several ways to help python-wimlib:
- Just use the module, the more it's used the more the urge to maintain it.
- Report bugs and request features, reporting bugs can be done via Github's [Issue tracker](https://github.com/0xGiddi/python-wimlib/issues)
- Review the code, don't like what you see? Comment on the code via Github.
- Pull requests, pull requests are welcome, but please don't make drastic changes without consulting the owner first.

### License
python-wimlib (this project) and the [wimlib](https://wimlib.net) library are licensed under the [GNU General Public
License v3](https://www.gnu.org/licenses/gpl-3.0.txt)

