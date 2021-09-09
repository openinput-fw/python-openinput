# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Filipe Laíns <lains@riseup.net>

from typing import NamedTuple, Optional


class Function(NamedTuple):
    """openinput protocol function identifier."""
    page_id: int
    function_id: int


class _PageMeta(type):
    """Helper metaclass to help construct function pages.

    Metaclass that takes an ``id`` argument (function page id) and transform
    the declared fields into :py:class:`Function` instances.

    Example::

        class SomePage(..., id=0x5):
            FUNC1 = 0x01
            FUNC2 = 0x02
            FUNC3 = 0x03

        assert SomePage._PAGE_ID == 0x05
        assert SomePage.FUNC1 == Function(0x05, 0x01)
        assert SomePage.FUNC2 == Function(0x05, 0x02)
        assert SomePage.FUNC3 == Function(0x05, 0x03)
    """
    def __new__(mcs, name, bases, dict_, id: Optional[int] = None):
        if len(bases) != 0:  # not the base class - _Page
            if id is None:
                raise ValueError('Missing `id` class construction argument')
            assert isinstance(id, int)
            for attr in dict_:
                if not attr.startswith('_'):
                    dict_[attr] = Function(id, dict_[attr])
            dict_['_PAGE_ID'] = id
        return super().__new__(mcs, name, bases, dict_)


# Function pages


class _Page(metaclass=_PageMeta):
    '''Function page base class.'''
    _PAGE_ID: int


class Info(_Page, id=0x00):
    VERSION = 0x01
    FW_INFO = 0x02
    SUPPORTED_FUNCTION_PAGES = 0x03
    SUPPORTED_FUNCTIONS = 0x04


class GeneralProfiles(_Page, id=0x01):
    pass


class Gimmicks(_Page, id=0xFD):
    pass


class Debug(_Page, id=0xFE):
    pass
