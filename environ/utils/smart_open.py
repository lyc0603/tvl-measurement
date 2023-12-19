"""
Smart open that supports stdout
"""
from typing import IO, cast

from smart_open import open as _smart_open


def smart_open(
    uri,
    mode="r",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
    transport_params=None,
) -> IO[str]:
    """
    Fix smart_open to support stdout
    """
    return cast(
        IO,
        _smart_open(
            uri,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
            transport_params=transport_params,
        ),
    )
