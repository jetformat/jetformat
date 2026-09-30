import importlib.util
import io
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('check_release', Path(__file__).resolve().parents[1] / 'scripts/check-release.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        for os in ('darwin', 'linux', 'windows'):
            for arch in ('amd64', 'arm64'):
                base = self.directory / f'jetformat_1.2.3_{os}_{arch}'
                magic = {'darwin': b'\xcf\xfa\xed\xfe', 'linux': b'\x7fELF', 'windows': b'MZ'}[os]
                data = magic + b'\0' * 1_000_000
                if os == 'windows':
                    with zipfile.ZipFile(str(base) + '.zip', 'w') as archive:
                        archive.writestr('jetformat.exe', data)
                else:
                    with tarfile.open(str(base) + '.tar.gz', 'w:gz') as archive:
                        info = tarfile.TarInfo('jetformat')
                        info.size = len(data)
                        info.mode = 0o755
                        archive.addfile(info, io.BytesIO(data))

    def test_complete_release_generates_repeatable_checksums(self):
        checker.check_release('1.2.3', self.directory)
        first = (self.directory / 'SHA256SUMS').read_bytes()
        checker.check_release('1.2.3', self.directory)
        self.assertEqual(first, (self.directory / 'SHA256SUMS').read_bytes())
        self.assertEqual(len(first.splitlines()), 6)

    def test_missing_platform_is_rejected(self):
        next(self.directory.glob('*.zip')).unlink()
        with self.assertRaises(ValueError):
            checker.check_release('1.2.3', self.directory)

    def test_unexpected_source_file_is_rejected(self):
        (self.directory / 'source.go').write_text('private source')
        with self.assertRaises(ValueError):
            checker.check_release('1.2.3', self.directory)

    def test_extra_file_in_archive_is_rejected(self):
        with zipfile.ZipFile(next(self.directory.glob('*.zip')), 'a') as archive:
            archive.writestr('../source.go', 'private source')
        with self.assertRaises(ValueError):
            checker.check_release('1.2.3', self.directory)

    def test_symlink_in_archive_is_rejected(self):
        archive_path = next(self.directory.glob('*.tar.gz'))
        with tarfile.open(archive_path, 'w:gz') as archive:
            info = tarfile.TarInfo('jetformat')
            info.type = tarfile.SYMTYPE
            info.linkname = '/etc/passwd'
            archive.addfile(info)
        with self.assertRaises(ValueError):
            checker.check_release('1.2.3', self.directory)

    def test_invalid_version_is_rejected(self):
        with self.assertRaises(ValueError):
            checker.check_release('../1.2.3', self.directory)
