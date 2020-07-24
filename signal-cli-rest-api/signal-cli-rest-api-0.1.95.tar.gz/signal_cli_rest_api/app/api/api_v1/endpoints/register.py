from subprocess import run
from typing import Any
from fastapi import APIRouter, Depends, File
from starlette.responses import StreamingResponse
from signal_cli_rest_api.app.utils import run_signal_cli_command
from signal_cli_rest_api.app.schemas import Verification, Registration
from io import BytesIO
import pyqrcode
router = APIRouter()


@router.get("/{number}/link")
def link_device(number: str) -> Any:
    response = run_signal_cli_command(["link"], False)
    print(response)
    buf = BytesIO()
    qr = pyqrcode.create(response, error='L')
    qr.png(buf, scale=3)
    buf.seek(0)  # important here!
    return StreamingResponse(buf, media_type="image/png")

@router.post("/{number}/update-account")
def update_account(number: str) -> Any:
    response = run_signal_cli_command(["-u", number, "updateAccount"])
    return response

@router.post("/{number}", response_model=Registration)
def register_number(registration: Registration, number: str) -> Any:
    """
    register a new number
    """

    cmd = ["-u", number, "register"]

    if registration.voice_verification:
        cmd.append("--voice")

    run_signal_cli_command(cmd)
    return registration


@router.post("/{number}/verify", response_model=Verification)
def verify_registration(verification: Verification, number: str) -> Any:
    """
    verify a registration, using the installation pin is currently not supported by signal-cli
    """

    cmd = ["-u", number, "verify", verification.verification_code]

    if verification.pin:
        cmd.extend(["-p", verification.pin])

    run_signal_cli_command(cmd)
    return verification
