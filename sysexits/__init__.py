from subprocess import CompletedProcess, SubprocessError
from typing import Optional


def raise_for_returncode(process: CompletedProcess, msg: Optional[str]):
    """Raise an error if a completed process has non-zero exit code.

    Parameters
    ----------
    process
        A completed process.
    msg
        An optional message to attach to the exception if raised. If no message is
        specified, the stderr of the process will be used (if it is available).

    Raises
    ------
    ValueError
        If the return code does not correspond to any of the listed exceptions.
    """
    if process.returncode == 0:
        return

    try:
        Exc = EXCEPTIONS[process.returncode]
    except KeyError:
        raise ValueError(f"No exception found for return code f{process.returncode}")
    else:
        if msg is not None:
            raise Exc(msg)
        elif isinstance(process.stderr, str):
            raise Exc(process.stderr)
        else:
            raise Exc()


class UsageError(SubprocessError):
    """A command was used incorrectly.

    E.g. with the wrong number of arguments, a bad flag, bad syntax in a parameter etc.
    """


class DataError(SubprocessError):
    """The user-inputted data was incorrect in some way."""


class NoInputError(SubprocessError):
    """An input file (not a system file) did not exist or was not readable.

    This could also include errors like "No message" to a mailer.
    """


class NoUserError(SubprocessError):
    """The user specified did not exist.

    For example in mail addresses or remote logins.
    """


class NoHostError(SubprocessError):
    """The host specified did not exist.

    For example in mail addresses or network requests.
    """


class UnavailableError(SubprocessError):
    """A service is unavailable.

    For example a support program or file does not exist, or "when something you wanted
    to do does not work, but you do not know why".
    """


class SoftwareError(SubprocessError):
    """An "internal software error" has been detected.

    Generally limited to non- OS-related errors.
    """


class OperatingSystemError(SubprocessError):
    """An operating system error has been detected.

    Intended to be used for such things as "cannot fork", "cannot create pipe", or the
    like. It includes things like getuid returning a user that does not exist in the
    passwd file.
    """


class OSFileError(SubprocessError):
    """Error with a system or OS file.

    Some system file (e.g., /etc/passwd, /var/run/utx.active, etc.) does not exist,
    cannot be opened, or has some sort of error (e.g., syntax error).
    """


class CannotCreateFileError(SubprocessError):
    """A user-specified output file cannot be created."""


class InputOutputError(SubprocessError):
    """An error occurred while doing I/O on some file."""


class TemporaryError(SubprocessError):
    """A temporary failure.

    Indicates something that is not really an error. E.g. a mailer could not create a
    connection, and the request should be reattempted later.
    """


class ProtocolError(SubprocessError):
    """Remote system returned something "impossible" during a protocol exchange."""


class InsufficientPermissionsError(SubprocessError):
    """You have insufficient permission to perform the operation.

    This is not intended for file system problems, which should use NoInputError or
    CannotCreateFileError, but rather for higher level permissions.
    """


class ConfigError(SubprocessError):
    """Something was found in an unconfigured or misconfigured state."""


EX_USAGE = 64
EX_DATAERR = 65
EX_NOINPUT = 66
EX_NOUSER = 67
EX_NOHOST = 68
EX_UNAVAILABLE = 69
EX_SOFTWARE = 70
EX_OSERR = 71
EX_OSFILE = 72
EX_CANTCREAT = 73
EX_IOERR = 74
EX_TEMPFAIL = 75
EX_PROTOCOL = 76
EX_NOPERM = 77
EX_CONFIG = 78

EXCEPTIONS = {
    EX_USAGE: UsageError,
    EX_DATAERR: DataError,
    EX_NOINPUT: NoInputError,
    EX_NOUSER: NoUserError,
    EX_NOHOST: NoHostError,
    EX_UNAVAILABLE: UnavailableError,
    EX_SOFTWARE: SoftwareError,
    EX_OSERR: OperatingSystemError,
    EX_OSFILE: OSFileError,
    EX_CANTCREAT: CannotCreateFileError,
    EX_IOERR: InputOutputError,
    EX_TEMPFAIL: TemporaryError,
    EX_PROTOCOL: ProtocolError,
    EX_NOPERM: InsufficientPermissionsError,
    EX_CONFIG: ConfigError,
}
