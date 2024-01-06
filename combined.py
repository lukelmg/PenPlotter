import svgwrite
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.basePen import BasePen

class CustomPathPen(BasePen):
    def __init__(self, glyphSet, current_x=0):
        BasePen.__init__(self, glyphSet)
        self.current_x = current_x
        self.commands = []

    def _moveTo(self, p0):
        self.commands.append(f"M {p0[0] + self.current_x} {p0[1]}")

    def _lineTo(self, p1):
        self.commands.append(f"L {p1[0] + self.current_x} {p1[1]}")

    def _curveToOne(self, p1, p2, p3):
        self.commands.append(f"C {p1[0] + self.current_x} {p1[1]}, {p2[0] + self.current_x} {p2[1]}, {p3[0] + self.current_x} {p3[1]}")

    def _closePath(self):
        self.commands.append("Z")

def text_to_path(font, text):
    glyph_set = font.getGlyphSet()
    current_x = 0
    all_commands = []

    for char in text:
        glyph_index = font.getBestCmap().get(ord(char))
        if glyph_index is not None:
            glyph = glyph_set[glyph_index]
            pen = CustomPathPen(glyph_set, current_x)
            glyph.draw(pen)
            all_commands.extend(pen.commands)
            current_x += glyph.width

    return " ".join(all_commands)

def create_svg(text, font_path, file_name, size=(300, 300)):
    font = TTFont(font_path)
    dwg = svgwrite.Drawing(file_name, size=(f"{size[0]}mm", f"{size[1]}mm"), profile='tiny')
    path = text_to_path(font, text)
    dwg.add(dwg.path(d=path, fill='none', stroke='black'))
    dwg.save()

# Example usage
font_path = 'DazHandwriting.ttf'  # Replace with the path to your TTF font file
create_svg("Hello World", font_path, "hello_world.svg")















# bottom

from svgpathtools import svg2paths

def svg_to_gcode(svg_file, gcode_file, feed_rate=1000, hop_height=5, max_width=300, max_height=300):
    paths, _ = svg2paths(svg_file)

    with open(gcode_file, 'w') as f:
        f.write("G21 ; set units to millimeters\n")
        f.write("G90 ; use absolute coordinates\n")
        f.write("M107 ; turn off fan\n")
        f.write("G28 ; home all axes\n")
        f.write(f"G1 Z{hop_height} F5000 ; lift nozzle\n")

        previous_end_x = None
        previous_end_y = None

        for path in paths:
            for segment in path:
                # Scale by 1/10 because image is 10x bigger than paper
                start = segment.start / 4
                end = segment.end / 4

                # Flip horizontally and vertically
                flipped_start_x = start.real
                flipped_end_x = end.real
                flipped_start_y = start.imag
                flipped_end_y = end.imag

                # Check if the start of the new segment is different from the end of the previous segment
                if flipped_start_x != previous_end_x or flipped_start_y != previous_end_y:
                    f.write(f"G1 Z{hop_height} F5000 ; lift nozzle\n")
                    f.write(f"G1 X{flipped_start_x} Y{flipped_start_y} F5000 ; move to start\n")
                    f.write(f"G1 Z0.3 F5000 ; lower nozzle\n")

                f.write(f"G1 X{flipped_end_x} Y{flipped_end_y} Z0.3 F{feed_rate}\n")

                previous_end_x = flipped_end_x
                previous_end_y = flipped_end_y

        f.write("G1 Z10 F5000 ; lift nozzle\n")
        f.write("M104 S0 ; turn off extruder heater\n")
        f.write("M140 S0 ; turn off bed heater\n")
        f.write("M84 ; disable motors\n")

# Use the function
svg_to_gcode('hello_world.svg', 'output_gcode_file2.gcode')
