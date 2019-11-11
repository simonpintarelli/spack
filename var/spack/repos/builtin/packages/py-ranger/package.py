# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyRanger(PythonPackage):
    """A VIM-inspired filemanager for the console"""

    homepage = "http://ranger.nongnu.org/"
    url      = "https://github.com/ranger/ranger/archive/v1.7.2.tar.gz"

    version('1.7.2', sha256='80917c93396e46272b6de63816d925eb708291a9f7a559d49b24c571ea0eeeb3')
    version('1.9.2', sha256='49a2d8dc5fa7b1c0cac0fa72d4ad704fc7107dee36cb9feb325a42754774d363')

    depends_on('python@2.6:')
