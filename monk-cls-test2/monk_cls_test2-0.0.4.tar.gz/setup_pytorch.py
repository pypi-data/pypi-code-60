import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="monk_cls_test2", # Replace with your own username
    version="0.0.4",
    author="Tessellate Imaging",
    author_email="abhishek@tessellateimaging.com",
    description="Monk Classification's Pytorch backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tessellate-Imaging/monk_v1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: GPU :: NVIDIA CUDA :: 9.0",
    ],
    install_requires=[
        'scipy',
        'scikit-learn',
        'scikit-image',
        'opencv-python',
        'pillow==6.0.0',
        'tqdm',
        'gpustat', 
        'psutil',
        'pandas',
        'GPUtil',
        'torch==1.4.0',
        'torchvision==0.5.0',
        'tabulate',
        'netron',
        'networkx',
        'matplotlib',
        'pylg',
        'ipywidgets'
    ],
    python_requires='>=3.6',

)





