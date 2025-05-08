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
        # Add any Python dependencies here
    ],
    python_requires='>=3.7',
    author='JFriso Technologies',
    description='FPC CLI',
    url='https://github.com/jfrisotech/fpc',
)
