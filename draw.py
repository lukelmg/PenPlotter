import svgwrite
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

def text_to_path(font_path, text, size):
    font = TTFont(font_path)
    glyph_set = font.getGlyphSet()
    pen = SVGPathPen(glyph_set)

    for char in text:
        glyph_index = font.getBestCmap().get(ord(char))
        if glyph_index is not None:
            glyph = glyph_set[glyph_index]
            glyph.draw(pen)

    path = pen.getCommands()
    return path

def create_svg(text, font_path, file_name, size=(300, 300)):
    dwg = svgwrite.Drawing(file_name, size=(f"{size[0]}mm", f"{size[1]}mm"), profile='tiny')
    path = text_to_path(font_path, text, size)
    dwg.add(dwg.path(d=path, fill='none', stroke='black'))
    dwg.save()

# Example usage
font_path = 'DazHandwriting.ttf'  # Replace with the path to your TTF font file
create_svg("Hello World", font_path, "hello_world.svg")
