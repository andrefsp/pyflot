from distutils.core import setup

setup(name='PyFlot',
    version='1.0',
    description='Python Interface for the known JavaScript Flot librabry',
    long_description=open('README.rst', 'r').read(),
    license='MIT',
    author='Andre da Palma',
    author_email='andrefsp@gmail.com',
    url='http://github.com/andrefsp/pyflot',
    packages=['flot', 'flot.templatetags'],
    package_dir={'flot': 'src/flot'},
)
