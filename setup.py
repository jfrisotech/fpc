from setuptools import setup, find_packages

setup(
    name='fpc',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fpc=main:main',
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
