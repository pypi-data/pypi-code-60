"""file Fluent API Helper.

This module contains helper methods for calling file.*
Notecard API commands.
"""
import notecard
from .validators import validate_card_object


@validate_card_object
def changes(card, tracker=None, files=None):
    """Perform individual or batch queries on Notefiles.

    Args:
        tracker (string): A developer-defined tracker ID.
        files (array): A list of Notefiles to retrieve changes for.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "file.changes"}
    if tracker:
        req["tracker"] = tracker
    if files:
        req["files"] = files
    return card.Transaction(req)


@validate_card_object
def delete(card, files=None):
    """Delete individual notefiles and their contents.

    Args:
        files (array): A list of Notefiles to delete.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "file.delete"}
    if files:
        req["files"] = files
    return card.Transaction(req)


@validate_card_object
def stats(card):
    """Obtain statistics about local notefiles.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "file.stats"}

    return card.Transaction(req)


@validate_card_object
def pendingChanges(card):
    """Retrive information about pending Notehub changes.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "file.changes.pending"}

    return card.Transaction(req)
