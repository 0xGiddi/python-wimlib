from setuptools import setup

long_description="""

"""

setup(
	name="pywimlib",
	version="0.1.0",
	description="Python bindings for wimlib (unofficial)",
	long_description=long_description,
	author="Gideon S. (0xGiddi)",
	author_email="elmocia@gmail.com",
	url="https://github.com/0xgiddi/python-wimlib",
	packages=["wimlib"],
	package_dir={
		"wimlib" : "wimlib",
	},
	license="GPLv3",
	install_requires=[
		"cffi>=1.8.2",
	],
	classifiers=[
		'Intended Audience :: Developers',
	],
)


