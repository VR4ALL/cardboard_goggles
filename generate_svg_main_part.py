#!/usr/bin/pyhton
# this script help to build guides for a cardboard laser cut.
# in way to ease the creation of cardboard goggles.

import lazercad

# define the parametric const
thickness = 3;  # cardboard thinkness
height = 75;  # height of the goggles and the phone
width = 130;  # width of the goggles and the phone
focal = 40;  # focal distance : distance between the lenses and the screen
depth = 40;  # depth of the goggles.
phone_depth = 7;  # thinkness otf the phone
holes = 20;  # lenght oh the holes used to fix the lenses plane.
lenses = 35;  # lenses diameters
eyes_distance = 65;  # distance between centers of lenses.
camera_hole_width = 10;
camera_hole_height = 40;
camera_hole_left_pos = 20;

# place guide relative position in lists
vertical_guide_list = [ 10,  # margin
                        height - thickness,  # this part goes inside so we remove thinkness
                        thickness/2., thickness/2.,  # consumed by the folding
                        width/2., width/2.,
                        thickness/2., thickness/2.,  # consumed by the folding
                        height,
                        thickness/2., thickness/2.,  # consumed by the folding
                        (width - eyes_distance)/2., eyes_distance/2.,
                        eyes_distance/2., (width - eyes_distance)/2.,
                        thickness/2., thickness/2.,  # consumed by the folding
                        height];
horizontal_guide_list = [ 10,  # margin
                        40,  # rabat
                        thickness/2., thickness/2.,  # consumed by the folding
                        thickness,  # we add thinckness of cardboard, for corect alignement
                        height/2., height/2.,  # to draw the middle,
                        thickness/2., thickness/2.,  # consumed by the folding
                        phone_depth,
                        focal/2., focal/2.,
                        depth];

# define some helpers const to ease the reding of the code.
h_base = 12;  # horizontal guide number of the base
h_lens = 11;  # horizontal guide number of the lenses plane
h_contour = 9;  # horizontal guide number
h_fold_1 = 7;  # horizontal guide number
h_lenses = 5;  # horizontal giude number of lenses center
h_fold_2 = 2; # horizontal guide number
h_top = 0;  # horizontal guide number
v_base = 0;  # vertical guide number
v_left = 2;  # vertical guide number
v_nose = 4;  # vertical guide number in front of the nose
v_right = 7;  # vertical guide number
v_left_top = 10;  # vertical guide number
v_forhead =12; # vertical guide number in front of forhead
v_right_top = 15;  # vertical guide number
v_last = 17;  # vertical guide number

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
guide_draw.draw_horizontal_cut_line(h_contour, v_base, v_left+1);
guide_draw.draw_horizontal_cut_line(h_top, v_left, v_right);
guide_draw.draw_horizontal_cut_line(h_contour, v_right-1, v_last);
# draw the base horizontal cutting lines
guide_draw.draw_horizontal_cut_line(h_base, v_base, v_left)
guide_draw.draw_horizontal_cut_line(h_base, v_left, v_right);
guide_draw.draw_horizontal_cut_line(h_base, v_right, v_left_top);
guide_draw.draw_horizontal_cut_line(h_base, v_left_top, v_right_top);
guide_draw.draw_horizontal_cut_line(h_base, v_right_top, v_last);
# draw the holes
guide_draw.draw_horizontal_centered_hole(h_lens, v_base, v_left, holes, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_left, v_nose, holes, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_nose, v_right, holes, thickness);
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
guide_draw.draw_vertical_fold_line(v_left, h_base, h_contour);
guide_draw.draw_vertical_fold_line(v_right, h_base, h_contour);
guide_draw.draw_vertical_fold_line(v_left_top - 1, h_base, h_contour);
guide_draw.draw_vertical_fold_line(v_right_top + 1, h_base, h_contour);
# add the hole for the camera
(x, y) = guides.get_coordinate(v_right, h_lenses);
x = x - camera_hole_left_pos;
y = y - camera_hole_height/2.;
drawing.draw_rounded_hole(x, y, camera_hole_width, camera_hole_height);

# LENS SUPORT
# draw the horizontal cutting lines
guide_draw.draw_horizontal_centered_crenau(h_fold_1-1, v_left_top, v_forhead, holes, thickness);
guide_draw.draw_horizontal_centered_crenau(h_fold_1-1, v_forhead, v_right_top, holes, thickness);
guide_draw.draw_horizontal_centered_crenau(h_fold_2+2, v_left_top, v_forhead, holes, -thickness);
guide_draw.draw_horizontal_centered_crenau(h_fold_2+2, v_forhead, v_right_top, holes, -thickness);
# draw the vertical cutting lines
guide_draw.draw_vertical_centered_crenau(v_left_top, h_fold_2+2, h_fold_1-1, holes, -thickness);
guide_draw.draw_vertical_centered_crenau(v_right_top, h_fold_2+2, h_fold_1-1, holes, thickness);
# draw the hole
guide_draw.draw_vertical_centered_hole(v_forhead, h_fold_2+2, h_fold_1-1, holes, thickness);

# save the drawing as SVG
drawing.save();
print "goggle.svg created or updated"




