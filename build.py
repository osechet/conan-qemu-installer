import os
import platform
from conans.tools import OSInfo
from cpt.packager import ConanMultiPackager

AVAILABLE_VERSIONS = [
    "4.1.0",
    "4.0.0",
    "3.1.1.1",
]

def detected_os():
    if OSInfo().is_macos:
        return "Macos"
    if OSInfo().is_windows:
        return "Windows"
    return platform.system()

def main():
    command = "sudo apt-get -qq update && sudo apt-get -qq install -y libglib2.0-dev"

    arch = os.environ["CONAN_ARCHS"]
    builder = ConanMultiPackager(docker_entry_script=command)
    current_os = detected_os()

    for version in AVAILABLE_VERSIONS:
        builder.add({"os" : current_os, "arch_build" : arch, "arch": arch}, {}, {}, {},
                    reference="qemu_installer/%s" % version)

    builder.run()

if __name__ == '__main__':
    main()
