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
    arch = os.environ["CONAN_ARCHS"]
    builder = ConanMultiPackager()
    current_os = detected_os()

    for version in AVAILABLE_VERSIONS:
        # New mode, with version field
        builder.add({"os" : current_os, "arch_build" : arch, "arch": arch}, {}, {}, {}, reference="qemu_installer/%s" % version)

    builder.run()

if __name__ == '__main__':
    main()
