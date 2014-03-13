#!/usr/bin/pyhton
# this script help to build guides for a cardboard laser cut.
# in way to ease the creation of cardboard goggles.

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

# The Drawing class as the responsability to manage svgwrite using more high level command
# High level commande are dedicated to laser cutting
# it is a compostion around a Drawing object from svgwrite
class Drawing(object):
    def __init__(self, filename):
        # declare the size of the cutting machine
        self.canvas_width = 600;
        self.canvas_heigh = 300;

        # declare the color needed by the cutting machine
        self.cut_color = svgwrite.rgb(0, 0, 0, '%');
        self.cut_width = 0.05;
        self.vertical_fold_color = svgwrite.rgb(255, 0, 0, '%');
        self.horizontal_fold_color = svgwrite.rgb(0, 0, 255, '%');
        self.fold_width = 0.05;
        self.draw_color = svgwrite.rgb(0, 255, 0, '%');
        self.draw_width = 0.03;
        self.engrave_color = svgwrite.rgb(0, 255, 255, '%');

        # dwg is public to allow direct manipulation using svgwrite
        self.dwg = svgwrite.Drawing(filename,
                size=('%dmm'%self.canvas_width,
                        '%dmm'%self.canvas_heigh),
                viewBox=('0 0 %d %d')%(
                        self.canvas_width,
                        self.canvas_heigh));

    def draw_horizontal_guide(self, y, from_x, to_x):
        line = self.dwg.line(
                (from_x, y),
                (to_x, y),
                stroke=self.draw_color,
                stroke_width=self.draw_width);
        line.dasharray(dasharray=[1, 1, 9,1], offset=None);
        self.dwg.add(line);

    def draw_vertical_guide(self, x, from_y, to_y):
        line = self.dwg.line(
                (x, from_y),
                (x, to_y),
                stroke=self.draw_color,
                stroke_width=self.draw_width);
        line.dasharray(dasharray=[1, 1, 9,1], offset=None);
        self.dwg.add(line);

    def draw_horizontal_hole(self, x, y, length, thickness):
        self.dwg.add(self.dwg.rect(
                insert=(x, y),
                size=(length, thickness),
                rx=None, 
                ry=None,
                stroke=self.cut_color,
                fill='white',
                stroke_width=self.cut_width));

    def draw_rounded_hole(self, x, y, width, height):
        self.dwg.add(self.dwg.rect(
                insert=(x, y),
                size=(width, height),
                rx=5, 
                ry=5,
                stroke=self.cut_color,
                fill='white',
                stroke_width=self.cut_width));

    def draw_vertical_hole(self, x, y, length, thickness):
        self.dwg.add(self.dwg.rect(
                insert=(x, y),
                size=(thickness, length),
                rx=None, 
                ry=None,
                stroke=self.cut_color,
                fill='white',
                stroke_width=self.cut_width));

    def draw_cut_line(self, x1, y1, x2, y2):
        self.dwg.add(self.dwg.line(
                (x1, y1),
                (x2, y2),
                stroke=self.cut_color,
                stroke_width=self.cut_width));

    def draw_fold_line(self, x1, y1, x2, y2):
        self.dwg.add(self.dwg.line(
                (x1, y1),
                (x2, y2),
                stroke=self.vertical_draw_color,
                stroke_width=self.vertical_fold_width));

    def draw_cut_path(self, path_string):
        path = self.dwg.path(
            d=path_string,
            stroke=self.cut_color,
            fill='white',
            stroke_width=self.cut_width);
        self.dwg.add(path);

    def save(self):
        self.dwg.save();

# GuidesDraw provide hight level drawing commands based on guides
class GuidesDraw(object):
    def __init__(self, drawing, guides):
        self.drawing = drawing;
        self.guides = guides;

    def draw_guides(self):
        last_vertical_position = 0;
        for vertical_position in self.guides.absolute_vertical_list:
            for horizontal_position in self.guides.absolute_horizontal_list:
                self.drawing.draw_horizontal_guide(horizontal_position,
                                            last_vertical_position,
                                            vertical_position);
            last_vertical_position = vertical_position;

        last_horizontal_position = 0;
        for horizontal_position in self.guides.absolute_horizontal_list:
            for vertical_position in self.guides.absolute_vertical_list:
                self.drawing.draw_vertical_guide(vertical_position,
                                            last_horizontal_position,
                                            horizontal_position);
            last_horizontal_position = horizontal_position;

    def draw_vertical_fold_line(self,
            vertical,
            horizontal_start,
            horizontal_stop):
        start = self.guides.get_coordinate(vertical, horizontal_start);
        stop = self.guides.get_coordinate(vertical, horizontal_stop);
        self.drawing.dwg.add(self.drawing.dwg.line(
                start,
                stop,
                stroke=self.drawing.vertical_fold_color,
                stroke_width=self.drawing.fold_width));

    def draw_horizontal_fold_line(self,
            horizontal,
            vertical_start,
            vertical_stop):
        start = self.guides.get_coordinate(vertical_start, horizontal);
        stop = self.guides.get_coordinate(vertical_stop, horizontal);
        self.drawing.dwg.add(self.drawing.dwg.line(
                start,
                stop,
                stroke=self.drawing.horizontal_fold_color,
                stroke_width=self.drawing.fold_width));

    def draw_vertical_cut_line(self,
            vertical,
            horizontal_start,
            horizontal_stop):
        start = self.guides.get_coordinate(vertical, horizontal_start);
        stop = self.guides.get_coordinate(vertical, horizontal_stop);
        self.drawing.dwg.add(self.drawing.dwg.line(
                start,
                stop,
                stroke=self.drawing.cut_color,
                stroke_width=self.drawing.cut_width));

    def draw_horizontal_cut_line(self,
            horizontal,
            vertical_start,
            vertical_stop):
        start = self.guides.get_coordinate(vertical_start, horizontal);
        stop = self.guides.get_coordinate(vertical_stop, horizontal);
        self.drawing.dwg.add(self.drawing.dwg.line(
                start,
                stop,
                stroke=self.drawing.cut_color,
                stroke_width=self.drawing.cut_width));

    def draw_horizontal_hole_guide(self,
            vertical,
            horizontal,
            position,
            length,
            thickness):

        (x, y) =  self.guides.get_coordinate(vertical, horizontal);
        x = x + position;
        self.drawing.dwg.add(self.drawing.dwg.rect(
                insert=(x, y),
                size=(length, thickness),
                rx=None, 
                ry=None,
                stroke=self.drawing.cut_color,
                fill='white',
                stroke_width=self.drawing.cut_width));

    def draw_horizontal_centered_hole(self,
            horizontal,
            vertical_start,
            vertical_stop,
            length,
            thickness):

        (x1, y) = self.guides.get_coordinate(vertical_start, horizontal);
        (x2, y) = self.guides.get_coordinate(vertical_stop, horizontal);
        x = (x1+x2-length)/2.;
        y = y - thickness/2.;
        self.drawing.dwg.add(self.drawing.dwg.rect(
                insert=(x, y),
                size=(length, thickness),
                rx=None, 
                ry=None,
                stroke=self.drawing.cut_color,
                fill='white',
                stroke_width=self.drawing.cut_width));

    def draw_vertical_centered_hole(self,
            vertical,
            horizontal_start,
            horizontal_stop,
            length,
            thickness):

        (x, y1) = self.guides.get_coordinate(vertical, horizontal_start);
        (x, y2) = self.guides.get_coordinate(vertical, horizontal_stop);
        y = (y1+y2-length)/2.;
        x = x - thickness/2.;
        self.drawing.dwg.add(self.drawing.dwg.rect(
                insert=(x, y),
                size=(thickness, length),
                rx=None, 
                ry=None,
                stroke=self.drawing.cut_color,
                fill='white',
                stroke_width=self.drawing.cut_width));

    def draw_horizontal_centered_crenau(self,
            horizontal,
            vertical_start,
            vertical_stop,
            length,
            thickness):
        (x1, y) = self.guides.get_coordinate(vertical_start, horizontal);
        (x2, y) = self.guides.get_coordinate(vertical_stop, horizontal);
        x_crenau_start = (x1+x2-length)/2.;
        x_crenau_stop = x_crenau_start + length;
        y_crenau = y + thickness;
        drw = self.drawing;
        drw.draw_cut_line(x1, y, x_crenau_start, y);
        drw.draw_cut_line(x_crenau_start, y, x_crenau_start, y_crenau);
        drw.draw_cut_line(x_crenau_start, y_crenau, x_crenau_stop, y_crenau);
        drw.draw_cut_line(x_crenau_stop, y_crenau, x_crenau_stop, y);
        drw.draw_cut_line(x_crenau_stop, y, x2, y);

    def draw_vertical_centered_crenau(self,
            vertical,
            horizontal_start,
            horizontal_stop,
            length,
            thickness):
        (x, y1) = self.guides.get_coordinate(vertical, horizontal_start);
        (x, y2) = self.guides.get_coordinate(vertical, horizontal_stop);
        y_crenau_start = (y1+y2-length)/2.;
        y_crenau_stop = y_crenau_start + length;
        x_crenau = x + thickness;
        drw = self.drawing;
        drw.draw_cut_line(x, y1, x, y_crenau_start);
        drw.draw_cut_line(x, y_crenau_start, x_crenau, y_crenau_start);
        drw.draw_cut_line(x_crenau, y_crenau_start, x_crenau, y_crenau_stop);
        drw.draw_cut_line(x_crenau, y_crenau_stop, x, y_crenau_stop);
        drw.draw_cut_line(x, y_crenau_stop, x, y2);

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
    height = 50;  # height of the test shape
    width = 50;  # width of the test shape

    vertical_guide_list = [ 10,  # margin
                            width/3,
                            width/3,
                            width/3];

    horizontal_guide_list = [ 10,  # margin
                            height];

    guides = GuideList(vertical_guide_list, horizontal_guide_list);
    guides.print_absolute_lists();

    drawing = Drawing('test.svg');
    guide_draw = GuidesDraw(drawing, guides);

    guide_draw.draw_guides();

    h_top = 0;  # horizontal guide number 0
    h_bottom = 1;  # horizontal guide number 1
    v_left = 0;  # vertical guide number 0
    v_right = 3;  # vertical guide number 3

    guide_draw.draw_vertical_cut_line(v_left, h_bottom, h_top);
    guide_draw.draw_vertical_cut_line(v_right, h_bottom, h_top);

    guide_draw.draw_horizontal_cut_line(h_top, v_left, v_right);
    guide_draw.draw_horizontal_cut_line(h_bottom, v_left, v_right);

    guide_draw.draw_vertical_fold_line(v_left+1, h_bottom, h_top);
    guide_draw.draw_vertical_fold_line(v_left+2, h_bottom, h_top);

    drawing.save();

    print "test.svg created or updated"




