import winreg

def hex_to_rgb(hex_color):
    """Convert HEX color to RGB"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("HEX code must be exactly 6 characters long.")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"{r} {g} {b}"

def parse_color_input(color_input):
    """Parse color input: RGB or HEX"""
    color_input = color_input.strip()
    if color_input.startswith("#"):
        color_input = color_input[1:]  # Remove "#" if present
    if len(color_input) == 6:  # Check if it's in HEX format
        return hex_to_rgb(color_input)
    else:  # Assume it's in RGB format
        parts = color_input.split()
        if len(parts) != 3:
            raise ValueError("Invalid RGB format. Should be 3 numbers separated by spaces.")
        r, g, b = map(int, parts)
        if not all(0 <= x <= 255 for x in (r, g, b)):
            raise ValueError("Each RGB value should be between 0 and 255.")
        return f"{r} {g} {b}"

def set_colors(rgb_color1, rgb_color2):
    """Change colors in the registry"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Control Panel\Colors", 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, 'Hilight', 0, winreg.REG_SZ, rgb_color1)
            winreg.SetValueEx(key, 'HotTrackingColor', 0, winreg.REG_SZ, rgb_color2)
        print("Colors successfully updated!")
    except Exception as e:
        print(f"Error while changing colors: {e}")

choose = int(input("[1] Choose new color\n[2] Return to Default\n[3] Exit\nChoose your option: "))

if choose == 1:
    try:
        color2_input = input("Enter new color for fill (RGB or HEX): ")
        color1_input = input("Enter new color for outline (RGB or HEX): ")
        color1 = parse_color_input(color1_input)
        color2 = parse_color_input(color2_input)
        set_colors(color1, color2)
    except Exception as e:
        print(f"Error in color input: {e}")
elif choose == 2:
    # Default Windows colors
    default_hilight = "0 120 215"
    default_hottracking = "0 102 204"
    set_colors(default_hilight, default_hottracking)
elif choose == 3:
    exit()
else:
    print("Invalid choice!")

input("\nPress Enter to exit...")
