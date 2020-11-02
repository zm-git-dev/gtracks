import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gtracks',
    version='1.3.3',
    author='Anthony Aylward',
    author_email='aaylward@eng.ucsd.edu',
    description='Plot genome track data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/anthony-aylward/gtracks.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['deeptools', 'pyGenomeTracks', 'seaborn'],
    entry_points={
        'console_scripts': [
            'gtracks=gtracks.gtracks:main',
            'gtracks-download-example-bw=gtracks.download_example_bw:main'
        ]
    },
    include_package_data=True
)
