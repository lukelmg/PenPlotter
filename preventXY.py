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
                flipped_start_y = max_height - start.imag
                flipped_end_y = max_height - end.imag

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
svg_to_gcode('path.svg', 'output_gcode_file2.gcode')
