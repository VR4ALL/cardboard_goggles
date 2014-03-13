#!/usr/bin/pyhton
# this script help to build guides for a cardboard laser cut.
# in way to ease the creation of cardboard goggles.

import lazercad
import math

# define the parametric const
thickness = 2.8;  # cardboard thinkness
folding = 2;  # folding line
height = 72;  # height of the goggles and the phone
width = 125;  # width of the goggles and the phone
focal = 40;  # focal distance : distance between the lenses and the screen
depth = 40;  # depth of the goggles.
phone_depth = 8;  # thinkness otf the phone
holes = 20;  # lenght oh the holes used to fix the lenses plane.
d_lenses = 24.5;  # lenses diameters
eyes_distance = 60;  # distance between centers of lenses.
camera_hole_width = 13;
camera_hole_height = 40;
camera_hole_left_pos = 10;
nose_length = 20;

# place guide relative position in lists
vertical_guide_list = [ 10,  # page margin
                        thickness, # we remove half thickness to the nose part, cause holes the maintain the lenses plate are centered
                        nose_length, focal - nose_length,  # needed for nose part
                        height - thickness - focal, # we remove thinkness and focal
                        folding, folding,  # consumed by the folding
                        thickness,  # we add thinckness of cardboard, for corect alignement
                        width/2., width/2.,
                        folding, folding,  # consumed by the folding
                        height,
                        folding, folding,  # consumed by the folding
                        (width - eyes_distance)/2., eyes_distance/2.,
                        eyes_distance/2., (width - eyes_distance)/2.,
                        folding, folding,  # consumed by the folding
                        height];
horizontal_guide_list = [ 10,  # margin
                        40,  # rabat
                        folding, folding,  # consumed by the folding
                        thickness,  # we add thinckness of cardboard, for corect alignement
                        height/2.,  # to draw the middle,
                        height/2. - nose_length,
                        nose_length,
                        folding, folding,  # consumed by the folding
                        phone_depth,
                        focal/2., focal/2.,
                        depth];

# define some helpers const to ease the reding of the code.
h_top = 0;  # horizontal guide number
h_fold_2 = h_top+2; # horizontal guide number
h_lenses = h_fold_2+3;  # horizontal giude number of lenses center
h_fold_1 = h_lenses+3;  # horizontal guide number
h_contour = h_fold_1+2;  # horizontal guide number
h_lens = h_contour + 2;  # horizontal guide number of the lenses plane
h_base = h_lens + 1;  # horizontal guide number of the base

v_base = 0;  # vertical guide number
v_left = v_base + 4;  # vertical guide number
v_nose = v_left + 4;  # vertical guide number in front of the nose
v_right = v_nose + 3;  # vertical guide number
v_left_top = v_right + 3;  # vertical guide number
v_forhead = v_left_top + 2; # vertical guide number in front of forhead
v_right_top = v_forhead + 2;  # vertical guide number
v_last = v_right_top + 3;  # vertical guide number

# instanciate a guide object to calculate absolute guide positions
guides = lazercad.GuideList(vertical_guide_list, horizontal_guide_list);
guides.print_absolute_lists();
# instanciate the goggles drawings
drawing = lazercad.Drawing('goggle.svg');
# instanciate an object to draw using the guides and draw the guides
guide_draw = lazercad.GuidesDraw(drawing, guides);
guide_draw.draw_guides();

# MAIN
# draw the vertical cutting lines
guide_draw.draw_vertical_cut_line(v_base, h_contour, h_base);
guide_draw.draw_vertical_cut_line(v_left, h_contour, h_top);
guide_draw.draw_vertical_cut_line(v_right, h_contour, h_top);
guide_draw.draw_vertical_cut_line(v_last, h_contour, h_base);
# draw the upper horizontal cutting lines
guide_draw.draw_horizontal_cut_line(h_contour, v_base, v_left+2);
guide_draw.draw_horizontal_cut_line(h_top, v_left, v_right);
guide_draw.draw_horizontal_cut_line(h_contour, v_right-2, v_last);
# draw the base horizontal cutting lines
guide_draw.draw_horizontal_cut_line(h_base, v_base, v_left)
guide_draw.draw_horizontal_cut_line(h_base, v_left, v_right);
guide_draw.draw_horizontal_cut_line(h_base, v_right, v_left_top);
guide_draw.draw_horizontal_cut_line(h_base, v_left_top, v_right_top);
guide_draw.draw_horizontal_cut_line(h_base, v_right_top, v_last);
# draw the holes
guide_draw.draw_horizontal_centered_hole(h_lens, v_base, v_left, holes, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_nose-1, v_nose, holes, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_nose, v_nose+1, holes, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_right, v_left_top, holes, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_left_top, v_forhead, holes, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_forhead, v_right_top, holes, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_right_top, v_last, holes, thickness);
guide_draw.draw_vertical_centered_hole(v_nose, h_contour, h_contour+1, holes/2., thickness);
guide_draw.draw_vertical_centered_hole(v_forhead, h_contour, h_contour+2, holes, thickness);
# draw the horizontal folding lines
guide_draw.draw_horizontal_fold_line(h_fold_1, v_left, v_right);
guide_draw.draw_horizontal_fold_line(h_fold_2, v_left, v_right);
# draw the vertical folding lines
guide_draw.draw_vertical_fold_line(v_left + 1, h_base, h_contour);
guide_draw.draw_vertical_fold_line(v_right - 1, h_base, h_contour);
guide_draw.draw_vertical_fold_line(v_left_top - 1, h_base, h_contour);
guide_draw.draw_vertical_fold_line(v_right_top + 1, h_base, h_contour);
# add the hole for the camera
(x, y) = guides.get_coordinate(v_left, h_lenses);
x = x + camera_hole_left_pos;
y = y - camera_hole_height/2.;
drawing.draw_rounded_hole(x, y, camera_hole_width, camera_hole_height);

def lense_hole(drawing, x, y,d):
    support_number = 8;
    normal_radius = d/2.;
    small_radius = d/2.-2;
    cut_radius = d/2.+3;
    ratio = 0.2;
    last_radius = small_radius;
    last_x = x + last_radius;
    last_y = y;
    for i in range(0, 362):
        if (i%(360/support_number)>(360/support_number)*ratio):
            radius = normal_radius;
        else:
            radius = small_radius;
        if (last_radius != radius):
            xi = x + cut_radius * math.cos(2.*math.pi/360*i);
            yi = y + cut_radius * math.sin(2.*math.pi/360*i);
            drawing.draw_cut_line(last_x, last_y, xi, yi);
        else:
            xi = x + radius * math.cos(2.*math.pi/360*i);
            yi = y + radius * math.sin(2.*math.pi/360*i);
        drawing.draw_cut_line(last_x, last_y, xi, yi);
        last_x = xi;
        last_y = yi;
        last_radius = radius;

# LENS SUPORT
# draw the horizontal cutting lines
guide_draw.draw_horizontal_centered_crenau(h_fold_1-1, v_left_top, v_forhead, holes, thickness);
guide_draw.draw_horizontal_centered_crenau(h_fold_1-1, v_forhead, v_right_top, holes, thickness);
guide_draw.draw_horizontal_centered_crenau(h_fold_2+2, v_left_top, v_forhead, holes, -thickness);
guide_draw.draw_horizontal_centered_crenau(h_fold_2+2, v_forhead, v_right_top, holes, -thickness);
# draw the vertical cutting lines
guide_draw.draw_vertical_centered_crenau(v_left_top, h_fold_2+2, h_fold_1-1, holes, -thickness*2.5);
guide_draw.draw_vertical_centered_crenau(v_right_top, h_fold_2+2, h_fold_1-1, holes, thickness);
# draw the holes
guide_draw.draw_vertical_centered_hole(v_forhead, h_fold_2+2, h_lenses+1, holes, thickness);
(x, y) = guides.get_coordinate(v_left_top+1, h_lenses);
lense_hole(drawing, x, y, d_lenses);
(x, y) = guides.get_coordinate(v_right_top-1, h_lenses);
lense_hole(drawing, x, y, d_lenses);

# NOSE, Eyes separator
# draw the horizontal cutting lines
guide_draw.draw_horizontal_centered_crenau(h_fold_1-1, v_base+2, v_base+3, holes/2., thickness);
guide_draw.draw_horizontal_centered_crenau(h_fold_2+2, v_base+1, v_base+3, holes, -thickness);
# draw the vertical cutting lines
guide_draw.draw_vertical_centered_crenau(v_base+1, h_fold_2+2, h_lenses+1, holes, -thickness);
guide_draw.draw_vertical_cut_line(v_base+3, h_fold_2+2, h_fold_1-1);

drawing.draw_cut_path("m 89.5,222 c 0,0 20,-38.5 46.16202,-38.24895 2.051,-11.79839 4.31823,-21.70893 13.83798,-21.75105 9.51975,-0.0421 11.88326,8.62957 13.6988,21.64992 "
                     + "C 191.38562,183.5 209.5,222 209.5,222");
drawing.draw_cut_path("m 290.5,222 c 0,0 10.16559,-38.16667 60,-38.16668 49.83333,0 60,38.16668 60,38.16668");
drawing.draw_cut_path("m 337.41667,130.99996 c 2.12499,-14.54167 0.39944,-28.78182 13.08333,-28.74996 12.68389,0.0319 10.49814,14.31504 13.58333,28.74996");
drawing.draw_cut_path("m 11.5,102.25 c 0,0 10.995974,0.36746 15.285955,8.5143 C 30.673958,118.14776 31.5,131 31.5,131");

# save the drawing as SVG
drawing.save();
print "goggle.svg created or updated"




