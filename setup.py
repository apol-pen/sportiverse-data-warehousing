from setuptools import find_packages, setup

setup(
    name="sportiverse_project",
    packages=find_packages(exclude=["sportiverse_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
