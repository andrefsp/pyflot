from distutils.core import setup

setup(name='PyFlot',
    version='0.1',
    description='Python Interface the JavaScript Flot chart librabry',
    long_description=open('README.rst', 'r').read(),
    license='MIT',
    author='Andre da Palma',
    author_email='andrefsp@gmail.com',
    url='http://github.com/andrefsp/pyflot',
    packages=['flot', 'flot.templatetags'],
    package_dir={'flot': 'src/flot'},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries"
    ]
)
