import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.test import test as TestCommand
import glob
import os
import sys
import setuptools
from pathlib import Path
base_path = os.path.dirname(__file__)
include_dirs=[]
try:
    import pybind11
    include_dirs-append(pybind11.get_include())
except:
    pass
    

ext_modules = [
    # If you need to link extra libraries or specify extra include directories
    # see https://docs.python.org/3/extending/building.html#building-c-and-c-extensions-with-distutils
    Extension(
        'gmicpy',
        define_macros =[("_hypot","hypot")],
        [ str(p) for p in  Path(base_path).rglob("*.cpp")],
        include_dirs=[os.path.join(base_path, 'include')]+include_dirs,
        language='c++',
        undef_macros=["NDEBUG"],
        libraries = ['gmic','gomp','png','z','jpeg',"fftw3","tiff","curl"],
    ),
]


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.

    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
                
        opts.append('-D_hypot=hypot')
        if ct in ['cygwin','unix']:
            opts.append('-fopenmp')
        
        for ext in self.extensions:
            ext.extra_compile_args = opts
            
        build_ext.build_extensions(self)
    def build_extension(self, ext):
        if sys.platform == 'win32':
             ext.libraries.append("gdi32")
        super().build_extension( ext)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='gmicpy',
    version='1.0.0',
    author='cedric.lacrambe',
    author_email='cedric.lacrambe@gmail.com',
     url='https://github.com/cedspam/gmicpy/',
    long_description=open('README.rst').read(),
    ext_modules=ext_modules,
    packages=setuptools.find_packages(),
    install_requires =['numpy',"pybind11"],
    cmdclass={
        'build_ext': BuildExt,
        'test': PyTest,
    },
    zip_safe=False,
    tests_require=['pytest'],
)
