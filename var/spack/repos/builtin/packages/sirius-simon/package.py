# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class SiriusSimon(CMakePackage, CudaPackage):
    """Domain specific library for electronic structure calculations"""

    homepage = "https://github.com/simonpintarelli/SIRIUS"
    url      = "https://github.com/simonpintarelli/SIRIUS/archive/v6.1.5.tar.gz"
    list_url = "https://github.com/simonpintarelli/SIRIUS/releases"
    git      = "https://github.com/simonpintarelli/SIRIUS.git"

    version('develop', branch='develop')
    version('master', branch='master')
    version('nlcg', branch='feat/nlcg')
    version('nlcg-mag', branch='nlcg-mag')

    version('6.5.4', sha256='5f731926b882a567d117afa5e0ed33291f1db887fce52f371ba51f014209b85d')
    version('6.5.3', sha256='eae0c303f332425a8c792d4455dca62557931b28a5df8b4c242652d5ffddd580')
    version('6.5.2', sha256='c18adc45b069ebae03f94eeeeed031ee99b3d8171fa6ee73c7c6fb1e42397fe7')
    version('6.5.1', sha256='599dd0fa25a4e83db2a359257a125e855d4259188cf5b0065b8e7e66378eacf3')
    version('6.5.0', sha256='5544f3abbb71dcd6aa08d18aceaf53c38373de4cbd0c3af44fbb39c20cfeb7cc')

    variant('shared', default=False, description="Build shared libraries")
    variant('openmp', default=True, description="Build with OpenMP support")
    variant('fortran', default=False, description="Build Fortran bindings")
    variant('python', default=False, description="Build Python bindings")
    variant('memory_pool', default=True, description="Build with memory pool")
    variant('elpa', default=False, description="Use ELPA")
    variant('vdwxc', default=False, description="Enable libvdwxc support")
    variant('scalapack', default=False, description="Enable scalapack support")
    variant('magma', default=False, description="Enable MAGMA support")
    variant('nlcglib', default=False, description="enable robust wave function optimization")
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    depends_on('python', type=('build', 'run'))
    depends_on('mpi')
    depends_on('gsl')
    depends_on('lapack')
    depends_on('fftw-api@3')
    depends_on('libxc')
    depends_on('spglib')
    depends_on('hdf5+hl')
    depends_on('pkgconfig', type='build')
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('py-scipy', when='+python', type=('build', 'run'))
    depends_on('py-h5py', when='+python', type=('build', 'run'))
    depends_on('py-mpi4py', when='+python', type=('build', 'run'))
    depends_on('py-pyyaml', when='+python', type=('build', 'run'))
    depends_on('py-mpi4py', when='+python', type=('build', 'run'))
    depends_on('py-voluptuous', when='+python', type=('build', 'run'))
    depends_on('py-pybind11', when='+python', type=('build', 'run'))
    depends_on('magma', when='+magma')

    depends_on('spfft', when='@6.4.0:')
    depends_on('spfft', when='@master')
    depends_on('spfft', when='@develop')
    depends_on('spfft', when='@nlcg')
    depends_on('spfft+cuda', when='@6.4.0:+cuda')
    depends_on('spfft+cuda', when='@master+cuda')
    depends_on('spfft+cuda', when='@develop+cuda')
    depends_on('spfft+cuda', when='@nlcg+cuda')
    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')
    depends_on('nlcglib', when='+nlcglib')
    depends_on('libvdwxc+mpi', when='+vdwxc')
    depends_on('scalapack', when='+scalapack')
    depends_on('cuda', when='+cuda')
    extends('python', when='+python')

    conflicts('+shared', when='@6.3.0:')  # option to build shared libraries has been removed

    # TODO:
    # add support for CRAY_LIBSCI, ROCm, testing

    patch("strip-spglib-include-subfolder.patch", when='@6.1.5')
    patch("link-libraries-fortran.patch", when='@6.1.5')
    patch("cmake-fix-shared-library-installation.patch", when='@6.1.5')

    @property
    def libs(self):
        libraries = []

        if '@6.3.0:' in self.spec:
            libraries += ['libsirius']

            return find_libraries(
                libraries, root=self.prefix,
                shared=True, recursive=True
            )

        else:
            if '+fortran' in self.spec:
                libraries += ['libsirius_f']

            if '+cuda' in self.spec:
                libraries += ['libsirius_cu']

            return find_libraries(
                libraries, root=self.prefix,
                shared='+shared' in self.spec, recursive=True
            )

    def cmake_args(self):
        spec = self.spec

        def _def(variant, flag=None):
            """Returns "-DUSE_VARIANT:BOOL={ON,OFF}" depending on whether
               +variant is set. If the CMake flag differs from the variant
               name, pass the flag name explicitly.
            """

            return "-D{0}:BOOL={1}".format(
                flag if flag else "USE_{0}".format(
                    variant.strip('+~').upper()
                ),
                "ON" if variant in spec else "OFF"
            )

        args = [
            _def('+openmp'),
            _def('+elpa'),
            _def('+magma'),
            _def('+nlcglib'),
            _def('+vdwxc'),
            _def('+memory_pool'),
            _def('+scalapack'),
            _def('+fortran', 'CREATE_FORTRAN_BINDINGS'),
            _def('+python', 'CREATE_PYTHON_MODULE'),
            _def('+cuda')
        ]

        if '@:6.2.999' in self.spec:
            args += [_def('+shared', 'BUILD_SHARED_LIBS')]

        lapack = spec['lapack']
        blas = spec['blas']

        args += [
            '-DLAPACK_FOUND=true',
            '-DLAPACK_LIBRARIES={0}'.format(lapack.libs.joined(';')),
            '-DBLAS_FOUND=true',
            '-DBLAS_LIBRARIES={0}'.format(blas.libs.joined(';')),
        ]

        if '+scalapack' in spec:
            args += [
                '-DSCALAPACK_FOUND=true',
                '-DSCALAPACK_INCLUDE_DIRS={0}'.format(
                    spec['scalapack'].prefix.include),
                '-DSCALAPACK_LIBRARIES={0}'.format(
                    spec['scalapack'].libs.joined(';')),
            ]

        if spec['blas'].name in ['intel-mkl', 'intel-parallel-studio']:
            args += ['-DUSE_MKL=ON']

        if '+elpa' in spec:
            elpa_incdir = os.path.join(
                spec['elpa'].headers.directories[0],
                'elpa'
            )
            args += ["-DELPA_INCLUDE_DIR={0}".format(elpa_incdir)]

        if '+cuda' in spec:
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch[0] != 'none':
                args += [
                    '-DCMAKE_CUDA_FLAGS=-arch=sm_{0}'.format(cuda_arch[0])
                ]

        return args
