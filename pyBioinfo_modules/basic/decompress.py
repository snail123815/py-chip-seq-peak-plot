from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile
from tempfile import _TemporaryFileWrapper
from os.path import commonpath

IMPLEMENTED_COMPRESSION_FORMATS: list[str] = ['.gz', '.xz']


def decompressFile(filePath: Path) -> Path:
    match filePath.suffix:
        case '.gz':
            prog = 'gzip'
        case '.xz':
            prog = 'xz'
        case _:
            raise NotImplementedError(
                f'Decompress {filePath.suffix} file is not supported.')
    resultFilePath = filePath.with_suffix('')
    with open(resultFilePath, 'w') as rf:
        decompress = subprocess.run(
            [prog, '-dc', filePath.resolve()],
            stdout=rf,
            stderr=subprocess.PIPE
        )
    if not resultFilePath.exists():
        raise FileNotFoundError('\n'.join([
            f'Unzip file {filePath} failed: no output file found:',
            ' '.join(decompress.args),
            decompress.stderr.decode()
        ]))
    return resultFilePath


def decompFileIfCompressed(
    filePath: Path,
    allowedFormats: list[str] = IMPLEMENTED_COMPRESSION_FORMATS
) -> tuple[Path, bool]:
    if filePath.suffix in allowedFormats:
        return decompressFile(filePath), True
    else:
        return filePath, False