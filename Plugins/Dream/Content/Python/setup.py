#UNREAL HAS TORCH, NUMPY,... SPECIAL PACKAGES
from setuptools import setup, find_packages

setup(
    name='Dream',
    version='0.0.1',
    description='ue5 stable diffusion integration',
    packages=find_packages(),
    install_requires=[
        'torch',
        'numpy',
        'tqdm'
    ],
)
