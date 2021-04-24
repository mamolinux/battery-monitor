import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    # metadata to display on PyPI
    name="battery-monitor",
    version="0.7",
    author="hsbasu",
    author_email="hsb10@iitbbs.ac.in",
    description="An X-platform utility tool developed on Golang, notifies about charging, discharging, and critically low battery state of the battery.",
    keywords="Battery Monitor Indicator Notify",
    url="https://hsbasu.github.io/battery-monitor",   # project home page, if any
    project_urls={
        "Source Code": "https://github.com/hsbasu/battery-monitor",
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
    ],
    packages=setuptools.find_packages(),
    package_data={
        '': ['icons/*.png'],
    },
    python_requires=">=3.6",
    install_requires=[
        "pygobject",
    ],
    entry_points={
        "console_scripts": [
            "battery-monitor=battery_monitor.run:main",
        ],
    }
    # could also include long_description, download_url, etc.
)
