#!/usr/bin/pyhton
# this script help to build guides for a cardboard laser cut.
# in way to ease the creation of cardboard goggles.

import create_xml_guides
import svgwrite

class LazerCutDrawing(object):
    def __init__(self):
        self.canvas_width = 600;
        self.canvas_heigh = 300;

        self.cut_color = svgwrite.rgb(0, 0, 0, '%');
        self.cut_width = 0.05;
        self.fold_color = svgwrite.rgb(255, 0, 0, '%');
        self.fold_width = 0.05;
        self.draw_color = svgwrite.rgb(0, 255, 0, '%');
        self.draw_width = 0.03;
        self.engrave_color = svgwrite.rgb(0, 0, 255, '%');

        self.dwg = svgwrite.Drawing('goggle.svg',
                size=('%dmm'%self.canvas_width,
                        '%dmm'%self.canvas_heigh),
                viewBox=('0 0 %d %d')%(
                        self.canvas_width,
                        self.canvas_heigh));

    def add_horizontal_guide(self, y, from_x, to_x):
        line = self.dwg.line(
                (from_x, y),
                (to_x, y),
                stroke=self.draw_color,
                stroke_width=self.draw_width);
        line.dasharray(dasharray=[1, 1, 9,1], offset=None);
        self.dwg.add(line);

    def add_vertical_guide(self, x, from_y, to_y):
        line = self.dwg.line(
                (x, from_y),
                (x, to_y),
                stroke=self.draw_color,
                stroke_width=self.draw_width);
        line.dasharray(dasharray=[1, 1, 9,1], offset=None);
        self.dwg.add(line);

    def add_horizontal_guide_list(self, position_list_mm):
        last_position = 0;
        for relative_position in position_list_mm:
            absolute_position = last_position + relative_position;
            self.add_horizontal_guide(absolute_position);
            last_position = absolute_position;

    def add_vertical_guide_list(self, position_list_mm):
        last_position = 0;
        for relative_position in position_list_mm:
            absolute_position = last_position + relative_position;
            self.add_vertical_guide(absolute_position);
            last_position = absolute_position;

    def add_guide_list(self, vertical_list, horizontal_list):
        last_vertical_position = 0;
        for relative_vertical_position in vertical_list:
            absolute_vertical_position = last_vertical_position + relative_vertical_position;
            last_horizontal_position = 0;
            for relative_horizontal_position in horizontal_list:
                absolute_horizontal_position = last_horizontal_position + relative_horizontal_position;
                self.add_horizontal_guide(absolute_horizontal_position,
                                            last_vertical_position,
                                            absolute_vertical_position);
                last_horizontal_position = absolute_horizontal_position;
            last_vertical_position = absolute_vertical_position;

        last_horizontal_position = 0;
        for relative_horizontal_position in horizontal_list:
            absolute_horizontal_position = last_horizontal_position + relative_horizontal_position;
            last_vertical_position = 0;
            for relative_vertical_position in vertical_list:
                absolute_vertical_position = last_vertical_position + relative_vertical_position;
                self.add_vertical_guide(absolute_vertical_position,
                                            last_horizontal_position,
                                            absolute_horizontal_position);
                last_vertical_position = absolute_vertical_position;
            last_horizontal_position = absolute_horizontal_position;

    def add_horizontal_hole(self, x, y, length, thickness):
        self.dwg.add(self.dwg.rect(
                insert=(x, y),
                size=(length, thickness),
                rx=None, 
                ry=None,
                stroke=self.cut_color,
                fill='white',
                stroke_width=self.cut_width));

    def add_vertical_hole(self, x, y, length, thickness):
        self.dwg.add(self.dwg.rect(
                insert=(x, y),
                size=(thickness, length),
                rx=None, 
                ry=None,
                stroke=self.cut_color,
                fill='white',
                stroke_width=self.cut_width));

    def add_cut_line(self, x1, y1, x2, y2):
        self.dwg.add(self.dwg.line(
                (x1, y1),
                (x2, y2),
                stroke=cut_color));

    def add_fold_line(self, x1, y1, x2, y2):
        self.dwg.add(self.dwg.line(
                (x1, y1),
                (x2, y2),
                stroke=fold_color));

    def save(self):
        self.dwg.save();

"""

path = dwg.path(d="M 0 0",
    fill='lightgray',
    stroke=cut_color,
    stroke_width=0.05);
path.push("h 200");
path.push("v 200");

dwg.add(path);

dwg.add(dwg.text('Telep[OO]rt',
                 insert=(0, 0.2),
                 fill=draw_color,
                 style = "font-size:50px; font-family:Arial"));


"""


if __name__ == '__main__':
    print "script to create goggle main part is running"
    thickness = 3;  # cardboard thinkness
    height = 75;  # height of the goggles and the phone
    width = 135;  # width of the goggles and the phone
    focal = 40;  # focal distance : distance between the lenses and the screen
    depth = 40;  # depth of the goggles.
    phone_depth = 7;

    horizontal_guide_list = [ 10,  # margin
                            40,  # rabat
                            thickness,  # consumed by the folding
                            height + thickness,
                            thickness,  # consumed by the folding
                            phone_depth,
                            focal/2, focal/2,
                            depth];

    vertical_guide_list = [ 10,  # margin
                            height - thickness,
                            thickness,  # consumed by the folding
                            width/2, width/2,
                            thickness,  # consumed by the folding
                            height,
                            thickness,  # consumed by the folding
                            width/2, width/2,
                            thickness,  # consumed by the folding
                            height];


    g = LazerCutDrawing();
    g.add_guide_list(vertical_guide_list, horizontal_guide_list);

    g.add_horizontal_hole(100, 100, 200, thickness);
    g.add_horizontal_hole(100, 300, 200, thickness);
    g.save();


    vertical_list = [ 0, height,
                      thickness/2, thickness/2, width/2, width/2,
                      thickness/2, thickness/2, height,
                      thickness/2, thickness/2, width/2, width/2,
                      thickness/2, thickness/2, height];

    print "script done"




