import os
import subprocess
import sys
from distutils.version import LooseVersion
from glob import glob
from os.path import join

import numpy as np
import setuptools.command.build_py
import setuptools.command.develop
from setuptools import Extension, find_packages, setup

platform_is_windows = sys.platform == "win32"

version = "0.0.1"

min_cython_ver = "0.21.0"
try:
    import Cython

    ver = Cython.__version__
    _CYTHON_INSTALLED = ver >= LooseVersion(min_cython_ver)
except ImportError:
    _CYTHON_INSTALLED = False


try:
    if not _CYTHON_INSTALLED:
        raise ImportError("No supported version of Cython installed.")
    from Cython.Distutils import build_ext

    cython = True
except ImportError:
    cython = False

if cython:
    ext = ".pyx"
    cmdclass = {"build_ext": build_ext}
else:
    ext = ".cpp"
    cmdclass = {}
    if not os.path.exists(join("pysinsy", "sinsy" + ext)):
        raise RuntimeError("Cython is required to generate C++ code")


# sinsy sources
src_top = join("lib", "sinsy", "src")

all_src = []
include_dirs = []
for s in [
    "lib",
    "lib/converter",
    "lib/japanese",
    "lib/label",
    "lib/score",
    "lib/temporary",
    "lib/util",
    "lib/xml",
    "lib/hts_engine_API",
    "lib/hts_engine_API/hts_engine/src/lib",
]:
    all_src += glob(join(src_top, s, "*.c"))
    all_src += glob(join(src_top, s, "*.cpp"))
    include_dirs.append(join(os.getcwd(), src_top, s))
# Add top include dir
include_dirs.append(join(src_top, "include", "sinsy"))
include_dirs.append(join(src_top, "lib/hts_engine_API/hts_engine/src/include"))

# Extension for sinsy
ext_modules = [
    Extension(
        name="pysinsy.sinsy",
        sources=[join("pysinsy", "sinsy" + ext)] + all_src,
        include_dirs=[np.get_include()] + include_dirs,
        extra_compile_args=[],
        extra_link_args=[],
        libraries=["winmm"] if platform_is_windows else [],
        language="c++",
    )
]

# Adapted from https://github.com/pytorch/pytorch
cwd = os.path.dirname(os.path.abspath(__file__))
if os.getenv("PYSINSY_BUILD_VERSION"):
    version = os.getenv("PYSINSY_BUILD_VERSION")
else:
    try:
        sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=cwd)
            .decode("ascii")
            .strip()
        )
        version += "+" + sha[:7]
    except subprocess.CalledProcessError:
        pass
    except IOError:  # FileNotFoundError for python 3
        pass


class build_py(setuptools.command.build_py.build_py):
    def run(self):
        self.create_version_file()
        setuptools.command.build_py.build_py.run(self)

    @staticmethod
    def create_version_file():
        global version, cwd
        print("-- Building version " + version)
        version_path = os.path.join(cwd, "pysinsy", "version.py")
        with open(version_path, "w") as f:
            f.write("__version__ = '{}'\n".format(version))


class develop(setuptools.command.develop.develop):
    def run(self):
        build_py.create_version_file()
        setuptools.command.develop.develop.run(self)


cmdclass["build_py"] = build_py
cmdclass["develop"] = develop


with open("README.md", "r") as fd:
    long_description = fd.read()

setup(
    name="pysinsy",
    version=version,
    description="A python wrapper for sinsy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ryuichi Yamamoto",
    author_email="zryuichi@gmail.com",
    url="https://github.com/r9y9/pysinsy",
    license="MIT",
    packages=find_packages(include=["pysinsy*"]),
    package_data={"": ["htsvoice/*"]},
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    install_requires=[
        "numpy >= 1.8.0",
        "cython >= " + min_cython_ver,
        "six",
    ],
    tests_require=["pytest", "coverage"],
    extras_require={
        "docs": [
            "sphinx_rtd_theme",
            "nbsphinx>=0.8.6",
            "Jinja2>=3.0.1",
            "pandoc",
            "ipython",
            "jupyter",
        ],
        "lint": [
            "pysen",
            "types-setuptools",
            "mypy<=0.910",
            "black>=19.19b0,<=20.8",
            "flake8>=3.7,<4",
            "flake8-bugbear",
            "isort>=4.3,<5.2.0",
        ],
        "test": ["pytest", "scipy"],
    },
    classifiers=[
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
    ],
    keywords=["Sinsy", "Research"],
)
