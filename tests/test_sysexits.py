import subprocess

import pytest

import sysexits


def test_successful_command_returns_none():
    process = subprocess.CompletedProcess(["exit", "0"], returncode=0)
    assert sysexits.raise_for_returncode(process) is None


def test_nonexistent_returncode_raises_valueerror():
    process = subprocess.CompletedProcess(["exit", "5"], returncode=5)
    with pytest.raises(ValueError):
        sysexits.raise_for_returncode(process)


def test_raises_correct_error_with_no_message():
    process = subprocess.CompletedProcess(["exit", "67"], returncode=67)
    with pytest.raises(sysexits.NoUserError):
        sysexits.raise_for_returncode(process)


def test_raises_correct_error_with_binary_stderr_message():
    process = subprocess.CompletedProcess(
        ["exit", "67"], returncode=67, stderr=b"Exiting with code 67."
    )
    with pytest.raises(sysexits.NoUserError, match="Exiting with code 67"):
        sysexits.raise_for_returncode(process)


def test_raises_correct_error_with_str_stderr_message():
    process = subprocess.CompletedProcess(
        ["exit", "67"], returncode=67, stderr="Exiting with code 67."
    )
    with pytest.raises(sysexits.NoUserError, match="Exiting with code 67"):
        sysexits.raise_for_returncode(process)


def test_raises_correct_error_with_custom_message():
    process = subprocess.CompletedProcess(
        ["exit", "67"], returncode=67, stderr="Exiting with code 67."
    )
    with pytest.raises(sysexits.NoUserError, match="No user found"):
        sysexits.raise_for_returncode(process, "No user found.")
