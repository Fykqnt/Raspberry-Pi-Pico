# font8x8.py

class Font8x8Basic:
    WIDTH = 8
    HEIGHT = 8
    FIRST = 32
    LAST = 127
    FONT = [
        # Bitmap data for characters from 32 (space) to 127
        # Each character is represented by 8 bytes (one byte per row)
        
        # ' ' (32)
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        
        # '!' (33)
        0x00, 0x00, 0x5F, 0x00, 0x00, 0x00, 0x00, 0x00,
        
        # '"' (34)
        0x00, 0x07, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00,
        
        # Add remaining characters here...
        
        # '~' (126)
        0x08, 0x04, 0x08, 0x10, 0x08, 0x00, 0x00, 0x00,
    ]
    WIDTHS = [8] * (LAST - FIRST + 1)  # Each character is 8 pixels wide
    OFFSETS = list(range(0, len(FONT), HEIGHT))  # Starting index for each character

font8x8_basic = Font8x8Basic()