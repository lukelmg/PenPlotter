from svgpathtools import svg2paths

def svg_to_gcode(svg_file, gcode_file, feed_rate=1000, x_offset=10, y_offset=10, width=300, hop_height=5):
    paths, _ = svg2paths(svg_file)

    with open(gcode_file, 'w') as f:
        f.write("G21 ; set units to millimeters\n")
        f.write("G90 ; use absolute coordinates\n")
        f.write("M107 ; turn off fan\n")
        f.write("G28 ; home all axes\n")
        f.write(f"G1 Z{hop_height} F5000 ; lift nozzle\n")

        for path in paths:
            for segment in path:
                start = segment.start
                end = segment.end

                # Flip horizontally by subtracting the real part from the width
                flipped_start_x = width/x_offset*2 - (start.real / x_offset)
                flipped_end_x = width/x_offset*2 - (end.real / x_offset)

                # Lift the nozzle before moving to the start of a new segment
                f.write(f"G1 Z{hop_height} F5000 ; lift nozzle\n")
                f.write(f"G1 X{flipped_start_x} Y{start.imag / y_offset} F5000 ; move to start\n")
                
                # Lower the nozzle to draw the segment
                f.write(f"G1 Z0.3 F5000 ; lower nozzle\n")
                f.write(f"G1 X{flipped_end_x} Y{end.imag / y_offset} Z0.3 F{feed_rate}\n")

        f.write("G1 Z10 F5000 ; lift nozzle\n")
        # If not using heaters, the following two lines can be removed or commented out
        f.write("M104 S0 ; turn off extruder heater\n")
        f.write("M140 S0 ; turn off bed heater\n")
        f.write("M84 ; disable motors\n")

svg_to_gcode('path.svg', 'output_gcode_file2.gcode')
