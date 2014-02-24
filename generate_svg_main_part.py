#!/usr/bin/pyhton
# this script help to build guides for a cardboard laser cut.
# in way to ease the creation of cardboard goggles.

import create_xml_guides
import svgwrite

# The GuideList Class has the responsability to manage a list of Guide position
class GuideList(object):
    def __init__(self, vertical_relative_list, horizontal_relative_list):
        self.relative_vertical_list = vertical_relative_list;
        self.relative_horizontal_list = horizontal_relative_list;
        self.absolute_vertical_list = self.calculate_absolute(vertical_relative_list);
        self.absolute_horizontal_list = self.calculate_absolute(horizontal_relative_list);

    def calculate_absolute(self, relative_list):
        last_position = 0;
        absolute_position_list = [];
        for relative_position in relative_list:
            absolute_position = last_position + relative_position;
            absolute_position_list.append(absolute_position);
            last_position = absolute_position;
        return absolute_position_list;

    def get_coordinate(self, vertical_guide_number, horizontal_guide_number):
        return (self.absolute_vertical_list[vertical_guide_number],
                self.absolute_horizontal_list[horizontal_guide_number]);

    def print_absolute_lists(self):
        print "vertical list: ", self.absolute_vertical_list;
        print "horizontal list: ", self.absolute_horizontal_list;


class LazerCutDrawing(object):
    def __init__(self, filename):
        self.canvas_width = 600;
        self.canvas_heigh = 300;

        self.cut_color = svgwrite.rgb(0, 0, 0, '%');
        self.cut_width = 0.05;
        self.fold_color = svgwrite.rgb(255, 0, 0, '%');
        self.fold_width = 0.05;
        self.draw_color = svgwrite.rgb(0, 255, 0, '%');
        self.draw_width = 0.03;
        self.engrave_color = svgwrite.rgb(0, 0, 255, '%');

        self.dwg = svgwrite.Drawing(filename,
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

    def add_guides(self, guides):
        last_vertical_position = 0;
        for vertical_position in guides.absolute_vertical_list:
            for horizontal_position in guides.absolute_horizontal_list:
                self.add_horizontal_guide(horizontal_position,
                                            last_vertical_position,
                                            vertical_position);
            last_vertical_position = vertical_position;

        last_horizontal_position = 0;
        for horizontal_position in guides.absolute_horizontal_list:
            for vertical_position in guides.absolute_vertical_list:
                self.add_vertical_guide(vertical_position,
                                            last_horizontal_position,
                                            horizontal_position);
            last_horizontal_position = horizontal_position;

    def add_horizontal_hole(self, x, y, length, thickness):
        self.dwg.add(self.dwg.rect(
                insert=(x, y),
                size=(length, thickness),
                rx=None, 
                ry=None,
                stroke=self.cut_color,
                fill='white',
                stroke_width=self.cut_width));

    def add_horizontal_hole_guide(self,
            guide,
            vertical,
            horizontal,
            position,
            length,
            thickness):

        (x, y) =  guides.get_coordinate(vertical, horizontal);
        x = x + position;
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
                stroke=self.cut_color,
                stroke_width=self.cut_width));

    def add_cut_vertical_line(self,
            guides,
            vertical,
            horizontal_start,
            horizontal_stop):
        start = guides.get_coordinate(vertical, horizontal_start);
        stop = guides.get_coordinate(vertical, horizontal_stop);
        self.dwg.add(self.dwg.line(
                start,
                stop,
                stroke=self.cut_color,
                stroke_width=self.cut_width));

    def add_cut_horizontal_line(self,
            guides,
            horizontal,
            vertical_start,
            vertical_stop):
        start = guides.get_coordinate(vertical_start, horizontal);
        stop = guides.get_coordinate(vertical_stop, horizontal);
        self.dwg.add(self.dwg.line(
                start,
                stop,
                stroke=self.cut_color,
                stroke_width=self.cut_width));

    def add_fold_line(self, x1, y1, x2, y2):
        self.dwg.add(self.dwg.line(
                (x1, y1),
                (x2, y2),
                stroke=self.fold_color,
                stroke_width=self.fold_width));

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
    thickness = 3;  # cardboard thinkness
    height = 75;  # height of the goggles and the phone
    width = 135;  # width of the goggles and the phone
    focal = 40;  # focal distance : distance between the lenses and the screen
    depth = 40;  # depth of the goggles.
    phone_depth = 7;

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

    horizontal_guide_list = [ 10,  # margin
                            40,  # rabat
                            thickness,  # consumed by the folding
                            height + thickness,
                            thickness,  # consumed by the folding
                            phone_depth,
                            focal/2, focal/2,
                            depth];

    guides = GuideList(vertical_guide_list, horizontal_guide_list);
    guides.print_absolute_lists();
    g = LazerCutDrawing('goggle.svg');
    g.add_guides(guides);

    h_base = 8;
    h_contour = 5;
    h_top = 0;
    h_lens = 6;  # lenses plane

    v_base = 0;
    v_left = 2;
    v_rigth = 4;
    v_last = 11;

    g.add_cut_vertical_line(guides, v_base, h_contour, h_base);
    g.add_cut_vertical_line(guides, v_left, h_contour, h_top);
    g.add_cut_vertical_line(guides, v_rigth, h_contour, h_top);
    g.add_cut_vertical_line(guides, v_last, h_contour, h_base);

    g.add_cut_horizontal_line(guides, h_base, v_base, v_left);
    g.add_cut_horizontal_line(guides, h_contour, v_base, v_left);
    g.add_cut_horizontal_line(guides, h_top, v_left, v_rigth);
    g.add_cut_horizontal_line(guides, h_contour, v_rigth, v_last);

    g.add_horizontal_hole_guide(guides, v_base, h_lens, 20, 20, thickness);
    g.add_horizontal_hole(100, 300, 200, thickness);
    g.save();

    print "goggle.svg created or updated"




