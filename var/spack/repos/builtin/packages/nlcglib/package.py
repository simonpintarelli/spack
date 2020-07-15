# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install nlcglib
#
# You can edit this file again by typing:
#
#     spack edit nlcglib
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Nlcglib(CMakePackage, CudaPackage):
    """Nonlinear CG methods for wave-function optimization in DFT."""

    homepage = "https://github.com/simonpintarelli/nlcglib"
    git      = "https://github.com/simonpintarelli/nlcglib.git"
    url      = "https://github.com/simonpintarelli/nlcglib/archive/master.zip"

    maintainers = ['simonpintarelli']

    version('master', branch='master')
    version('develop', branch='develop')

    variant('wrapper', default=False,
            description='Use nvcc-wrapper for CUDA build')
    variant('openmp', default=False)
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    depends_on('lapack')
    depends_on('kokkos +cuda~cuda_relocatable_device_code+cuda_lambda')
    depends_on('kokkos-nvcc-wrapper', when='+wrapper')
    depends_on('kokkos +cuda~cuda_relocatable_device_code+cuda_lambda+wrapper', when='+wrapper')
    depends_on("cmake@3.15:", type='build')
    depends_on('kokkos+cuda~cuda_relocatable_device_code+cuda_lambda+openmp+wrapper', when='+openmp+wrapper')

    def setup_dependent_package(self, module, dependent_spec):
        try:
            self.spec.kokkos_cxx = self.spec['kokkos-nvcc-wrapper'].kokkos_cxx
        except Exception:
            self.spec.kokkos_cxx = spack_cxx

    @property
    def libs(self):
        libraries = ['libnlcglib']

        return find_libraries(
            libraries, root=self.prefix,
            shared='+shared' in self.spec, recursive=True
        )

    def cmake_args(self):
        options = []

        if '+openmp' in self.spec:
            options.append('-DUSE_OPENMP=On')
        if '~openmp' in self.spec:
            options.append('-DUSE_OPENMP=Off')
        if self.spec['blas'].name in ['intel-mkl', 'intel-parallel-studio']:
            options.append('-DLAPACK_VENDOR=MKL')
        elif self.spec['blas'].name in ['openblas']:
            options.append('-DLAPACK_VENDOR=OpenBLAS')
        else:
            raise Exception('blas/lapack must be either openblas or mkl.')


        # set compiler
        try:
            options.append('-DCMAKE_CXX_COMPILER=%s' %
                           self.spec['kokkos-nvcc-wrapper'].kokkos_cxx)
        except Exception:
            options.append('-DCMAKE_CXX_COMPILER=%s' % spack_cxx)

        options.append('-DBUILD_TESTS=OFF')

        return options
