import os
import subprocess
import sys
from distutils.errors import DistutilsExecError
from distutils.spawn import spawn
from distutils.version import LooseVersion
from glob import glob
from itertools import chain
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


msvc_extra_compile_args_config = [
    "/source-charset:utf-8",
    "/execution-charset:utf-8",
]

try:
    if not _CYTHON_INSTALLED:
        raise ImportError("No supported version of Cython installed.")
    from Cython.Distutils import build_ext

    cython = True
except ImportError:
    cython = False

if cython:
    ext = ".pyx"

    def msvc_extra_compile_args(compile_args):
        cas = set(compile_args)
        xs = filter(lambda x: x not in cas, msvc_extra_compile_args_config)
        return list(chain(compile_args, xs))

    class custom_build_ext(build_ext):
        def build_extensions(self):
            compiler_type_is_msvc = self.compiler.compiler_type == "msvc"
            for entry in self.extensions:
                if compiler_type_is_msvc:
                    entry.extra_compile_args = msvc_extra_compile_args(
                        entry.extra_compile_args
                        if hasattr(entry, "extra_compile_args")
                        else []
                    )

            build_ext.build_extensions(self)

    cmdclass = {"build_ext": custom_build_ext}
else:
    ext = ".cpp"
    cmdclass = {}
    if not os.path.exists(join("pyopenjtalk", "openjtalk" + ext)):
        raise RuntimeError("Cython is required to generate C++ code")


# Workaround for `distutils.spawn` problem on Windows python < 3.9
# See details: [bpo-39763: distutils.spawn now uses subprocess (GH-18743)]
# (https://github.com/python/cpython/commit/1ec63b62035e73111e204a0e03b83503e1c58f2e)
def test_quoted_arg_change():
    child_script = """
import os
import sys
if len(sys.argv) > 5:
    try:
        os.makedirs(sys.argv[1], exist_ok=True)
        with open(sys.argv[2], mode=sys.argv[3], encoding=sys.argv[4]) as fd:
            fd.write(sys.argv[5])
    except OSError:
        pass
"""

    try:
        # write
        package_build_dir = "build"
        file_name = join(package_build_dir, "quoted_arg_output")
        output_mode = "w"
        file_encoding = "utf8"
        arg_value = '"ARG"'

        spawn(
            [
                sys.executable,
                "-c",
                child_script,
                package_build_dir,
                file_name,
                output_mode,
                file_encoding,
                arg_value,
            ]
        )

        # read
        with open(file_name, mode="r", encoding=file_encoding) as fd:
            return fd.readline() != arg_value
    except (DistutilsExecError, TypeError):
        return False


def escape_string_macro_arg(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def escape_macro_element(x):
    (k, arg) = x
    return (k, escape_string_macro_arg(arg)) if type(arg) == str else x


def escape_macros(macros):
    return list(map(escape_macro_element, macros))


custom_define_macros = (
    escape_macros
    if platform_is_windows and test_quoted_arg_change()
    else (lambda macros: macros)
)


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
        language="c++",
        define_macros=custom_define_macros(
            [
                ("HAVE_CONFIG_H", None),
                ("DIC_VERSION", 102),
                ("MECAB_DEFAULT_RC", '"dummy"'),
                ("PACKAGE", '"open_jtalk"'),
                ("VERSION", '"1.10"'),
                ("CHARSET_UTF_8", None),
            ]
        ),
    )
]

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
    tests_require=["pytest", 'coverage'],
    extras_require={
        'docs': ['sphinx_rtd_theme'],
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
    keywords=["Sinsy", "Research"]
)
