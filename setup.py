# coding: utf-8

from __future__ import with_statement, print_function, absolute_import

from setuptools import setup, find_packages, Extension
import setuptools.command.develop
import setuptools.command.build_py
from distutils.version import LooseVersion
import subprocess
import numpy as np
import os
from os.path import join

version = '0.0.1'

sinsy_install_prefix = os.environ.get(
    "SINSY_INSTALL_PREFIX", "/usr/local/")

sinsy_include_top = join(sinsy_install_prefix, "include")
sinsy_library_path = join(sinsy_install_prefix, "lib")

lib_candidates = list(filter(lambda l: l.startswith("libsinsy."),
                             os.listdir(join(sinsy_library_path))))
if len(lib_candidates) == 0:
    raise OSError("sinsy library cannot be found")

min_cython_ver = '0.21.0'
try:
    import Cython
    ver = Cython.__version__
    _CYTHON_INSTALLED = ver >= LooseVersion(min_cython_ver)
except ImportError:
    _CYTHON_INSTALLED = False

try:
    if not _CYTHON_INSTALLED:
        raise ImportError('No supported version of Cython installed.')
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    cython = True
except ImportError:
    cython = False

if cython:
    ext = '.pyx'
    cmdclass = {'build_ext': build_ext}
else:
    ext = '.cpp'
    cmdclass = {}
    if not os.path.exists(join("pysinsy", "sinsy" + ext)):
        raise RuntimeError("Cython is required to generate C++ code")

ext_modules = cythonize(
    [Extension(
        name="pysinsy.sinsy",
        sources=[
            join("pysinsy", "sinsy" + ext),
        ],
        include_dirs=[np.get_include(),
                      join(sinsy_include_top)],
        library_dirs=[sinsy_library_path],
        libraries=["sinsy"],
        extra_compile_args=[],
        extra_link_args=[],
        language="c++")],
)

# Adapted from https://github.com/pytorch/pytorch
cwd = os.path.dirname(os.path.abspath(__file__))
if os.getenv('PYSINSY_BUILD_VERSION'):
    version = os.getenv('PYSINSY_BUILD_VERSION')
else:
    try:
        sha = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=cwd).decode('ascii').strip()
        version += '+' + sha[:7]
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
        print('-- Building version ' + version)
        version_path = os.path.join(cwd, 'pysinsy', 'version.py')
        with open(version_path, 'w') as f:
            f.write("__version__ = '{}'\n".format(version))


class develop(setuptools.command.develop.develop):

    def run(self):
        build_py.create_version_file()
        setuptools.command.develop.develop.run(self)


cmdclass['build_py'] = build_py
cmdclass['develop'] = develop


with open('README.md', 'r') as fd:
    long_description = fd.read()

setup(
    name='pysinsy',
    version=version,
    description='A python wrapper for sinsy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ryuichi Yamamoto',
    author_email='zryuichi@gmail.com',
    url='https://github.com/r9y9/pysinsy',
    license='MIT',
    packages=find_packages(),
    package_data={'': ['htsvoice/*']},
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    install_requires=[
        'numpy >= 1.8.0',
        'cython >= ' + min_cython_ver,
        'six',
    ],
    tests_require=['nose', 'coverage'],
    extras_require={
        'docs': ['sphinx_rtd_theme'],
        'test': ['nose', 'scipy'],
    },
    classifiers=[
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
    ],
    keywords=["Sinsy", "Research"]
)
