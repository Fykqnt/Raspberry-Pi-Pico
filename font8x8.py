# font8x8.py

class Font8x8Basic:
    WIDTH = 8
    HEIGHT = 8
    FIRST = 32
    LAST = 127
    FONT = [
        # Bitmap data for characters from 32 (space) to 127
        # Each character is represented by 8 bytes (one byte per row)
        # Example for space (' ') and exclamation mark ('!')
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # ' ' (32)
        0x00, 0x00, 0x5F, 0x00, 0x00, 0x00,  # '!' (33)
        # Add bitmap data for remaining characters here...
        # Ensure that each character has 8 bytes
    ]
    WIDTHS = [8] * (LAST - FIRST + 1)  # Assuming fixed width for simplicity
    OFFSETS = list(range(0, len(FONT), HEIGHT))  # Starting index for each character

font8x8_basic = Font8x8Basic()
