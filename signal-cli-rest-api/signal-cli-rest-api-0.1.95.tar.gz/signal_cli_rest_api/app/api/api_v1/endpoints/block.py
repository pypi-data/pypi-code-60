from typing import Any, List
from fastapi import APIRouter, Body, Depends
from signal_cli_rest_api.app.schemas import Block
from signal_cli_rest_api.app.utils import run_signal_cli_command

router = APIRouter()


@router.post("/{number}", response_model=Block)
def block_numbers_or_groups(block: Block, number: str) -> Any:
    """
    block one or multiple numbers or group id's
    """
    cmd = ["-u", number, "block"]

    if block.group:
        cmd.append("-g")

    cmd += block.numbers

    run_signal_cli_command(cmd)

    return block


@router.delete("/{number}", response_model=Block)
def unblock_numbers_or_groups(unblock: Block, number: str) -> Any:
    """
    unblock one or multiple numbers or group id's
    """
    cmd = ["-u", number, "unblock"]

    if unblock.group:
        cmd.append("-g")

    cmd += unblock.numbers

    run_signal_cli_command(cmd)

    return unblock
