#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Created Date:       2020-05-02 18:16:41
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-05-02 18:23:22
Copyright © 2020-Pagliacii-MIT License
"""

import math
from struct import unpack

from app.errors import InvalidHeader


class Header:
    """The file header of SWF files.

    # Header format

    From the Adobe SWF file format specification, all SWF files begin with the following header:
    +------------+------+-------------------------------------------------------------+
    |    Field   | Type |                           Comment                           |
    +------------+------+-------------------------------------------------------------+
    | Signature  | UI8  | Signature byte:                                             |
    |            |      | "F" indicates uncompressed                                  |
    |            |      | "C" indicates a zlib compressed SWF (SWF 6 and later only)  |
    |            |      | "Z" indicates a LZMA compressed SWF (SWF 13 and later only) |
    +------------+------+-------------------------------------------------------------+
    | Signature  | UI8  | Signature byte always "W"                                   |
    +------------+------+-------------------------------------------------------------+
    | Signature  | UI8  | Signature byte always "S"                                   |
    +------------+------+-------------------------------------------------------------+
    | Version    | UI8  | Single byte file version (for example, 0x06 for SWF 6)      |
    +------------+------+-------------------------------------------------------------+
    | FileLength | UI32 | Length of entire file in bytes                              |
    +------------+------+-------------------------------------------------------------+
    | FrameSize  | RECT | Frame size in twips (1 twip = 1/20 pixels)                  |
    +------------+------+-------------------------------------------------------------+
    | FrameRate  | UI16 | Frame delay in 8.8 fixed number of frames per second        |
    +------------+------+-------------------------------------------------------------+
    | FrameCount | UI16 | Total number of frames in file                              |
    +------------+------+-------------------------------------------------------------+

    # Types

    ## Integer Types (not all)

    +------+-------------------------------+
    | Type | Comment                       |
    +------+-------------------------------+
    | UI8  | Unsigned 8-bit integer value  |
    +------+-------------------------------+
    | UI16 | Unsigned 16-bit integer value |
    +------+-------------------------------+
    | UI32 | Unsigned 32-bit integer value |
    +------+-------------------------------+

    Notes:
    1. All integer values are stored in the SWF file by using little-endian byte order.
    2. The bit order with in bytes in the SWF file format is big-endian.
    3.All integer types must be byte-aligned.

    ## Rectangle record (RECT)

    A rectangle value represents a rectangular region defined by a minimum x- and y-coordinate position
    and a maximum x- and y-coordinate position. The RECT record must be byte aligned.
    +-------+-----------+-------------------------------------------+
    | Field | Type      | Comment                                   |
    +-------+-----------+-------------------------------------------+
    | Nbits | UB[5]     | Bits used for each subsequent field       |
    +-------+-----------+-------------------------------------------+
    | Xmin  | SB[Nbits] | x minimum position for rectangle in twips |
    +-------+-----------+-------------------------------------------+
    | Xmax  | SB[Nbits] | x maximum position for rectangle in twips |
    +-------+-----------+-------------------------------------------+
    | Ymin  | SB[Nbits] | y minimum position for rectangle in twips |
    +-------+-----------+-------------------------------------------+
    | Ymax  | SB[Nbits] | y maximum position for rectangle in twips |
    +-------+-----------+-------------------------------------------+

    ## Fixed-point numbers

    The SWF file format supports two types of fixed-point numbers: 32-bit and 16-bit.

    The 32-bit fixed-point numbers are 16.16. That is, the high 16 bits represent
    the number before the decimal point, and the low 16 bits represent the number
    after the decimal point. FIXED values are stored like 32-bit integers in the SWF
    file (using little-endian byte order) and must be byte aligned.

    For example: The real value 7.5 is equivalent to: 0x0007.8000. This value is
    stored in the SWF file as: 00 80 07 00.

    SWF 8 and later supports 16-bit 8.8 signed, fixed-point numbers. The high 8 bits
    represent the number before the decimal point, and the low 8 bits represent the
    number after the decimal point. FIXED8 values are stored like 16-bit integers
    in the SWF file (using the little-endian byte order) and must be byte aligned.

    +--------+---------------------------------+
    | Type   | Comment                         |
    +--------+---------------------------------+
    | FIXED  | 32-bit 16.16 fixed-point number |
    +--------+---------------------------------+
    | FIXED8 | 16-bit 8.8 fixed-point number   |
    +--------+---------------------------------+

    ## Bit values

    Bit values are variable-length bit fields that can represent three types of numbers:
        1. Unsigned integers
        2. Signed integers
        3. Signed 16.16 fixed-point values

    +-----------+-------------------------------+
    | Type      | Comment                       |
    +-----------+-------------------------------+
    | SB[nBits] | Signed-bit value              |
    +-----------+-------------------------------+
    | UB[nBits] | Unsigned-bit value            |
    +-----------+-------------------------------+
    | FB[nBits] | Signed, fixed-point bit value |
    +-----------+-------------------------------+
    Note: nBits is the number of bits used to store the value

    Bit values do not have to be byte aligned. If a byte-aligned type follows a bit value,
    the last byte that contains the bit value is padded with zeros.

    Example:
    Byte1     |Byte2     |Byte3      |Byte4     |Byte5     |Byte6    |Byte7    |Byte8
    0101,10|10,100|1,0010,0|101,1|110,0100,0|110,1011,1|001,1001,0000,0100,1100,1010,1101
    BV1    |BV2   |BV3     |BV4  |BV5       |BV6|BV7   |BV8|BV9 |pad |U16

    The bit stream begins with a 6-bit value (BV1), followed by a 5-bit value (BV2) that
    is spread across Byte1 and Byte2. BV3 is spread across Byte2 and Byte3, while BV4 is
    wholly contained within Byte3. Byte5 contains two bit values: BV7 and BV8. BV9 is
    followed by a byte-aligned type (UI16), so the last four bits of Byte6 are padded with 0s.
    """  # noqa

    def __init__(self, path: str):
        self.__signature = None
        self.__version = None
        self.__file_length = None
        self.__frame_size = None
        self.__frame_rate = None
        self.__frame_count = None
        self.parse_file(path)

    def parse_file(self, path: str):
        with open(path, "rb") as f:
            first_part = f.read(9)
            sig1, sig2, sig3, version, length, needed_byte = unpack("<3cBIB", first_part)  # noqa E501

            if not (sig1 in b"FCZ" or sig2 == b"W" or sig3 == b"S"):
                raise InvalidHeader("Invalid signature")

            self.__signature = (sig1, sig2, sig3)
            self.__version = version
            self.__file_length = length

            n_bits = (needed_byte & 0b11111000) >> 3
            extra_bits = needed_byte & 0b00000111
            second_part_length = math.ceil((n_bits * 4 - 3) / 8)
            second_part = f.read(second_part_length)

            binary = format(extra_bits, '03b') + format(int(second_part.hex(), 16), f'0{second_part_length * 8}b')  # noqa E501
            x_min = int(binary[0 * n_bits:1 * n_bits], 2)
            x_max = int(binary[1 * n_bits:2 * n_bits], 2)
            y_min = int(binary[2 * n_bits:3 * n_bits], 2)
            y_max = int(binary[3 * n_bits:4 * n_bits], 2)
            self.__frame_size = {
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max,
                "width": (x_max - x_min) // 20,
                "height": (y_max - y_min) // 20,
            }

            third_part = f.read(4)
            rate_dec_part, rate_int_part, count = unpack("<2BH", third_part)
            self.__frame_rate = float.fromhex(f"{rate_int_part}.{rate_dec_part}")  # noqa E501
            self.__frame_count = count

    @property
    def signature(self):
        """tuple: Signature bytes"""
        return self.__signature

    @property
    def version(self):
        """int: The SWF file version"""
        return self.__version

    @property
    def file_length(self):
        """int: Length of entire file in bytes"""
        return self.__file_length

    @property
    def frame_x_min(self):
        """int: The x minimum position for frame size in twips"""
        return self.__frame_size["x_min"]

    @property
    def frame_x_max(self):
        """int: The x maximum position for frame size in twips"""
        return self.__frame_size["x_max"]

    @property
    def frame_y_min(self):
        """int: The y minimum position for frame size in twips"""
        return self.__frame_size["y_min"]

    @property
    def frame_y_max(self):
        """int: The y maximum position for frame size in twips"""
        return self.__frame_size["y_max"]

    @property
    def frame_width(self):
        """int: The frame width in pixels"""
        return self.__frame_size["width"]

    @property
    def frame_height(self):
        """int: The frame height in pixels"""
        return self.__frame_size["height"]

    @property
    def frame_rate(self):
        """float: Frame delay of frames per second"""
        return self.__frame_rate

    @property
    def frame_count(self):
        """int: Total number of frames in file"""
        return self.__frame_count
