from setuptools import setup, find_packages


def get_description():
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except ImportError:
        print("Could not convert markdown to rst")
        return open('README.md', 'rb').read().decode('utf-8')


setup(
    name='ultima_lib',
    version='0.0.7',
    description='A python library for wrapping around the ULTIMA service',
    long_description=get_description(),
    maintainer='eLIPSE',
    url='',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'requests',
    ],
    license='MIT License',
    keywords='',
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
