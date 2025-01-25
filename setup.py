import setuptools

setuptools.setup(
    name="app_calendar",
    version="1.0.0",
    scripts=["./scripts/app_calendar"],
    author="Rajakumaran Arivumani",
    description="app_calendar python package install",
    url="https://github.com/dexplorer/df-app-calendar",
    # packages=setuptools.find_packages(),
    packages=[
        "app_calendar",
    ],
    # packages = find_packages(),
    install_requires=[
        "setuptools",
        "requests",
        "utils@git+https://github.com/dexplorer/utils#egg=utils-1.0.1",
        "metadata@git+https://github.com/dexplorer/df-metadata#egg=metadata-1.0.5",
    ],
    python_requires=">=3.12",
)
