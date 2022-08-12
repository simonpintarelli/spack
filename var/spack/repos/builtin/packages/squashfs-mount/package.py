# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SquashfsMount(MesonPackage):
    """Allows non-root users to mount squashfs files without the overhead of
    squashfuse."""

    homepage = "https://github.com/eth-cscs/squashfs-mount"
    url      = "https://github.com/eth-cscs/squashfs-mount/archive/refs/tags/v0.3.1.tar.gz"
    git      = "https://github.com/eth-cscs/squashfs-mount"

    maintainers = ["haampie"]

    version('master', branch='master')
    version("squashfuse", branch="feat/squashfuse")

    version("0.3.1", sha256="bc3c199b006e901668f3043a1d017f16a7bf68abaf377194759a3a8a231252a2")
    version("0.3.0", sha256="f32db27b4207aa77c7825a913596936d77c05f23b20b174f1661d59866452f75")
    version("0.2.3", sha256="79ad1e05ab8f3ec4c42f16b3af2ffc6567d0e5b130baf6925a55e93b89e33765")
    version("0.2.1", sha256="e13ddb79182ea39129abb7e048ef89c67b6c8f1d4399a8fe872b0a5b04deaee5")
    version("0.1.0", sha256="37841ede7a7486d437fd06ae13e432560f81806f69addc72cfc8e564c8727bc6")

    variant("suid", default=False, description="Make squashfs-mount a suid executable")

    depends_on('libfuse')
    depends_on('squashfuse', when='@squashfuse')

    def meson_args(self):
        args = []
        if 'libfuse@:2.99.9'in self.spec:
            args += ['-Dfuse_version=fuse']
        elif 'libfuse@3:' in self.spec:
            args += ['-Dfuse_version=fuse3']

        # meson package doesn't have define_from_variant method
        if "+suid" in self.spec:
            args += ['-Dsuid=true']
        else:
            args += ['-Dsuid=false']

        return args
