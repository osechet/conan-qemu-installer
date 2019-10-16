import os
from six import StringIO
from conans import ConanFile


class QEmuInstallerConanTest(ConanFile):

    def build(self):
        pass

    def test(self):
        output = StringIO()
        qemu_path = os.path.join(self.deps_cpp_info["qemu_installer"].rootpath,
                                 "bin", "qemu-system-arm")
        self.run("{} --version".format(qemu_path), output=output, run_environment=True)
        self.output.info(str(output.getvalue()))
        ver = str(self.requires["qemu_installer"].ref.version)
        expected_version = """QEMU emulator version %s
Copyright (c) 2003-2019 Fabrice Bellard and the QEMU Project developers""" % ver

        qemu_version = str(output.getvalue()).strip()
        self.output.info("Expected value: {}".format(expected_version))
        self.output.info("Detected value: {}".format(qemu_version))
        assert expected_version == qemu_version
