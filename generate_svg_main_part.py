#!/usr/bin/pyhton
# this script help to build guides for a cardboard laser cut.
# in way to ease the creation of cardboard goggles.

import lazercad

# define the parametric const
thickness = 3;  # cardboard thinkness
height = 75;  # height of the goggles and the phone
width = 135;  # width of the goggles and the phone
focal = 40;  # focal distance : distance between the lenses and the screen
depth = 40;  # depth of the goggles.
phone_depth = 7;

# place guide relative position in lists
vertical_guide_list = [ 10,  # margin
                        height - thickness,  # this part goes inside so we remove thinkness
                        thickness/2, thickness/2,  # consumed by the folding
                        width/2, width/2,
                        thickness/2, thickness/2,  # consumed by the folding
                        height,
                        thickness/2, thickness/2,  # consumed by the folding
                        width/2, width/2,
                        thickness/2, thickness/2,  # consumed by the folding
                        height];
horizontal_guide_list = [ 10,  # margin
                        40,  # rabat
                        thickness/2, thickness/2,  # consumed by the folding
                        height + thickness,
                        thickness/2, thickness/2,  # consumed by the folding
                        phone_depth,
                        focal/2, focal/2,
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
h_contour = 7;  # horizontal guide number
h_top = 0;  # horizontal guide number
h_lens = 9;  # horizontal guide number of the lenses plane
v_base = 0;  # vertical guide number
v_left = 3;  # vertical guide number
v_right = 5;  # vertical guide number
v_left_top = 10;  # vertical guide number
v_right_top = 12;  # vertical guide number
v_last = 15;  # vertical guide number
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
guide_draw.draw_horizontal_centered_hole(h_lens, v_base, v_left, 20, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_left, v_left+1, 20, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_left+1, v_right, 20, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_right, v_left_top, 20, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_left_top, v_left_top+1, 20, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_left_top+1, v_right_top, 20, thickness);
guide_draw.draw_horizontal_centered_hole(h_lens, v_right_top, v_last, 20, thickness);
guide_draw.draw_vertical_centered_hole(v_left+1, h_contour, h_contour+1, 10, thickness);
guide_draw.draw_vertical_centered_hole(v_left_top+1, h_contour, h_contour+2, 20, thickness);
# save the drawing as SVG
drawing.save();
print "goggle.svg created or updated"




