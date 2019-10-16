import os
from conans import tools, ConanFile, AutoToolsBuildEnvironment
from conans import __version__ as conan_version
from conans.model.version import Version
from conans.errors import ConanInvalidConfiguration, NotFoundException, ConanException


AVAILABLE_VERSIONS = [
    "4.1.0",
    "4.0.0",
    "3.1.1.1"
]

class QEmuInstallerConan(ConanFile):
    name = "qemu_installer"
    version = "4.1.0"
    license = "MIT"
    author = "Olivier Sechet"
    url = "https://gitlab.com/osechet/conan-qemu-installer"
    description = "create qemu binaries package"
    homepage = "https://www.qemu.org"
    topics = ("conan", "qemu", "build", "installer")
    settings = "os_build", "arch_build", "compiler", "arch"
    options = {"version": AVAILABLE_VERSIONS}
    default_options = {"version": [v for v in AVAILABLE_VERSIONS if "-" not in v][0]}
    #generators = "cmake"
    exports = "LICENSE"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _arch(self):
        return self.settings.get_safe("arch_build") or self.settings.get_safe("arch")

    @property
    def _os(self):
        return self.settings.get_safe("os_build") or self.settings.get_safe("os")

    @property
    def _qemu_version(self):
        if "version" in self.options:
            return str(self.options.version)
        else:
            return self.version

    def _minor_version(self):
        return ".".join(str(self._qemu_version).split(".")[:2])

    def _get_filename(self):
        return self._get_filename_src()

    def _get_filename_src(self):
        return "qemu-%s" % self._qemu_version

    def config_options(self):
        if self.version >= Version("2.8"):  # XXX: fix this
            del self.options.version

    def _download_source(self):
        ext = "tar.xz"
        dest_file = "file.tar.xz"
        unzip_folder = self._get_filename()

        def download_qemu(url, dest_file, unzip_folder):
            self.output.info("Downloading: %s" % url)
            tools.get(url, filename=dest_file, verify=False)
            os.rename(unzip_folder, self._source_subfolder)

        url = "https://download.qemu.org/%s.%s" % (self._get_filename_src(), ext)
        download_qemu(url, dest_file, unzip_folder)

    def _configure_qemu(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir=self._source_subfolder)
        return autotools

    def build(self):
        self._download_source()
        self.settings.arch = self.settings.arch_build  # workaround for cross-building to get the correct arch during the build
        autotools = self._configure_qemu()
        autotools.make()

    def package_id(self):
        self.info.include_build_settings()
        if self.settings.os_build == "Windows":
            del self.info.settings.arch_build # same build is used for x86 and x86_64
        del self.info.settings.arch
        del self.info.settings.compiler

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        autotools = self._configure_qemu()
        autotools.install()

    def package_info(self):
        if self.package_folder is not None:
            self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        else:
            self.output.warn("No package folder have been created.")
