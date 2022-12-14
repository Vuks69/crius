import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="crius",
    version="0.1",
    scripts=["crius/crius", "arp-scan.py", "crius/nmap.py"],
    author="KS, MM, DW",
    author_email="",
    description="Simple network discovery script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vuks69/crius",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Systems Administration",
        "Intended Audience :: System Administrators",
    ],
)
