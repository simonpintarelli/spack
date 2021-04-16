# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
#     spack install q-e-sirius
#
# You can edit this file again by typing:
#
#     spack edit q-e-sirius
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class QESiriusCmake(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/electronic-structure/q-e-sirius"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    version('ristretto', branch='ristretto')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    variant('openmp', default=True)
    variant('mpi', default=True)
    variant('scalapack', default=False)
    variant('elpa', default=False)
    variant('libxc', default=False)
    variant('hdf5', default=False)

    depends_on('sirius+fortran')

    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+scalapack')
    depends_on('elpa', when='+elpa')
    depends_on('libxc', when='+libxc')
    depends_on('hdf5', when='+hdf5')
    conflicts('~mpi', when='+scalapack')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        spec = self.spec

        def _def(variant):
            return "-DQE_ENABLE_{0}:BOOL={1}".format(
                variant.strip('+~n').upper(),
                "ON" if variant in spec else "OFF"
            )

        args = ['+elpa', '+mpi', '+openmp', '+hdf5']

        args.append('-DQE_ENABLE_SIRIUS=On')

        return args
