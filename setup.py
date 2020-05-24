"""
Shows 20 most important Amino acids, can be used to learn them.
"""
from setuptools import setup, find_packages

dependencies = ["pyqt5", "pandas"]
opt_dependencies = []

setup(
    name="amino-acids-tutor",
    version="1.0",
    author="Luka Jeromel",
    author_email="luka.jeromel1@gmail.com",
    description="Shows desired Amino Acid",
    long_description=__doc__,
    packages=find_packages(exclude=["tests"]),
    # modules=["amino_acids"],
    install_requires=dependencies,
    install_extas=opt_dependencies,
    entry_points={
        # "console_scripts": ["luka-led-display=led_display.__main__:main"],
        "gui_scripts": ["amino-acids=amino_acids.__main__:main"],
    },
)
