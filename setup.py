import setuptools # type: ignore

setuptools.setup(
    name='fpc',
    version='0.1.0',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'fpc=fpc.cli:main',
        ],
    },
    install_requires=[
        'ruamel.yaml>=0.17.0',
        'rich>=13.0.0',
    ],
    python_requires='>=3.7',
    author='JFriso Technologies',
    description='FPC CLI',
    url='https://github.com/jfrisotech/fpc',
)
