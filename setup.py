from distutils.core import setup

setup(name='PyFlot',
    version='1.0',
    description='Python Interface for the known JavaScript Flot librabry',
    author='Andre da Palma',
    author_email='andrefsp@gmail.com',
    url='http://github.com/andrefsp/pyflot',
    packages=['flot'],
    package_dir={'flot': 'src/flot'},
)
