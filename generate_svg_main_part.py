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
phone_depth = 7;
holes = 20;

# place guide relative position in lists
vertical_guide_list = [ 10,  # margin
                        height - thickness,  # this part goes inside so we remove thinkness
                        thickness/2., thickness/2.,  # consumed by the folding
                        width/2., width/2.,
                        thickness/2., thickness/2.,  # consumed by the folding
                        height,
                        thickness/2., thickness/2.,  # consumed by the folding
                        width/2., width/2.,
                        thickness/2., thickness/2.,  # consumed by the folding
                        height];
horizontal_guide_list = [ 10,  # margin
                        40,  # rabat
                        thickness/2., thickness/2.,  # consumed by the folding
                        height + thickness,
                        thickness/2., thickness/2.,  # consumed by the folding
                        phone_depth,
                        focal/2., focal/2.,
                        depth];
# instanciate a guide object to calculate absolute guide positions
guides = lazercad.GuideList(vertical_guide_list, horizontal_guide_list);
guides.print_absolute_lists();
# instanciate the goggles drawings
drawing = lazercad.Drawing('goggle.svg');
# instanciate an object to draw using the guides and draw the guides
guide_draw = lazercad.GuidesDraw(drawing, guides);
guide_draw.draw_guides();
# define some helpers const to ease the reding of the code.
h_base = 10;  # horizontal guide number of the base
h_lens = 9;  # horizontal guide number of the lenses plane
h_contour = 7;  # horizontal guide number
h_fold_1 = 5;  # horizontal guide number
h_fold_2 = 2; # horizontal guide number
h_top = 0;  # horizontal guide number
v_base = 0;  # vertical guide number
v_left = 3;  # vertical guide number
v_nose = 4;  # vertical guide number in front of the nose
v_right = 5;  # vertical guide number
v_left_top = 10;  # vertical guide number
v_forhead =11; # vertical guide number in front of forhead
v_right_top = 12;  # vertical guide number
v_last = 15;  # vertical guide number

# MAIN
# draw the vertical cutting lines
guide_draw.draw_vertical_cut_line(v_base, h_contour, h_base);
guide_draw.draw_vertical_cut_line(v_left, h_contour, h_top);
guide_draw.draw_vertical_cut_line(v_right, h_contour, h_top);
guide_draw.draw_vertical_cut_line(v_last, h_contour, h_base);
# draw the upper horizontal cutting lines
guide_draw.draw_horizontal_cut_line(h_contour, v_base, v_left);
guide_draw.draw_horizontal_cut_line(h_top, v_left, v_right);
guide_draw.draw_horizontal_cut_line(h_contour, v_right, v_last);
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
guide_draw.draw_vertical_fold_line(v_left - 1, h_base, h_contour);
guide_draw.draw_vertical_fold_line(v_right + 1, h_base, h_contour);
guide_draw.draw_vertical_fold_line(v_left_top - 1, h_base, h_contour);
guide_draw.draw_vertical_fold_line(v_right_top + 1, h_base, h_contour);

# LENS SUPORT
# draw the horizontal cutting lines
guide_draw.draw_horizontal_centered_crenau(h_fold_1-1, v_left_top, v_forhead, holes, thickness);
guide_draw.draw_horizontal_centered_crenau(h_fold_1-1, v_forhead, v_right_top, holes, thickness);
guide_draw.draw_horizontal_centered_crenau(h_fold_2+1, v_left_top, v_forhead, holes, -thickness);
guide_draw.draw_horizontal_centered_crenau(h_fold_2+1, v_forhead, v_right_top, holes, -thickness);
# draw the vertical cutting lines
guide_draw.draw_vertical_centered_crenau(v_left_top, h_fold_2+1, h_fold_1-1, holes, -thickness);
guide_draw.draw_vertical_centered_crenau(v_right_top, h_fold_2+1, h_fold_1-1, holes, thickness);
# draw the hole
guide_draw.draw_vertical_centered_hole(v_forhead, h_fold_2+1, h_fold_1-1, holes, thickness);

# save the drawing as SVG
drawing.save();
print "goggle.svg created or updated"




