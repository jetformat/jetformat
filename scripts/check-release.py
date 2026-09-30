#!/usr/bin/env python3
"""Reject incomplete or unsafe binary releases; generate deterministic SHA256SUMS."""
import hashlib
import re
import sys
import tarfile
import zipfile
from pathlib import Path


def check_release(version, directory):
    if not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', version):
        raise ValueError('Expected a stable version without v')
    directory = Path(directory)
    expected = {
        f'jetformat_{version}_{os}_{arch}' + ('.zip' if os == 'windows' else '.tar.gz')
        for os in ('darwin', 'linux', 'windows')
        for arch in ('amd64', 'arm64')
    }
    actual = {p.name for p in directory.iterdir() if p.name != 'SHA256SUMS'}
    if actual != expected:
        raise ValueError(f'Archive set mismatch: missing={expected - actual}, unexpected={actual - expected}')
    checksums = []
    for name in sorted(expected):
        path = directory / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'Expected a regular archive: {name}')
        if name.endswith('.zip'):
            with zipfile.ZipFile(path) as archive:
                if archive.namelist() != ['jetformat.exe']:
                    raise ValueError(f'Unexpected ZIP contents: {name}')
                if archive.testzip() is not None:
                    raise ValueError(f'Corrupt ZIP: {name}')
                binary = archive.read('jetformat.exe')
                if not binary.startswith(b'MZ'):
                    raise ValueError(f'Expected a Windows executable: {name}')
        else:
            with tarfile.open(path, 'r:gz') as archive:
                members = archive.getmembers()
                if len(members) != 1 or members[0].name != 'jetformat' or not members[0].isfile():
                    raise ValueError(f'Unexpected tar contents: {name}')
                if not members[0].mode & 0o111:
                    raise ValueError(f'Binary is not executable: {name}')
                binary = archive.extractfile(members[0]).read()
                magic = b'\x7fELF' if '_linux_' in name else b'\xcf\xfa\xed\xfe'
                if not binary.startswith(magic):
                    raise ValueError(f'Unexpected executable format: {name}')
        if len(binary) < 1_000_000:
            raise ValueError(f'Unexpectedly small executable: {name}')
        checksums.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {name}\n')
    (directory / 'SHA256SUMS').write_text(''.join(checksums), encoding='utf-8')
    print(f'Validated {len(expected)} binary archives and wrote SHA256SUMS')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('usage: check-release.py VERSION DIRECTORY')
    check_release(sys.argv[1], sys.argv[2])
