from setuptools import setup

with open('pyviziosoundbar/version.py') as f: exec(f.read())
with open('README.md', 'r') as myfile:
    longdescription=myfile.read()
setup(
    name='pyviziosoundbar',

    version=__version__,
    description='Python library for interfacing with Vizio SmartCast Sound Bars',
    long_description=longdescription,
    long_description_content_type="text/markdown",
    url='https://github.com/raman325/pyviziosoundbar',

    author='Raman Gupta',
    author_email='raman325@gmail.com',

    license='GPLv3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],

    keywords='vizio smartcast soundbar vizio-soundbar',

    packages=["pyviziosoundbar"],

    install_requires=['click', 'requests', 'jsonpickle', 'xmltodict'],
    entry_points={
        'console_scripts': [
            'pyviziosoundbar=pyviziosoundbar.cli:cli',
        ],
    },
)
