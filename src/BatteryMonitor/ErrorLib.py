# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Battery Monitor – Maximize Your Battery Life.
#  Copyright (C) 2016–2020 Maksudur Rahman Maateen
#  Copyright (C) 2021–2025 Himadri Sekhar Basu
#  Licensed under GPLv3 or later (see <http://www.gnu.org/licenses/>)
# -----------------------------------------------------------------------------

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ValidationError(Error):
    """Exception raised for errors in the validation.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str):
        self.message = message
