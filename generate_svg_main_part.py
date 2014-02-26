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
# instanciate a guide object to calculate absolute guide positions
guides = lazercad.GuideList(vertical_guide_list, horizontal_guide_list);
guides.print_absolute_lists();
# instanciate the goggles drawings
drawing = lazercad.Drawing('goggle.svg');
# instanciate an object to draw using the guides and draw the guides
guide_draw = lazercad.GuidesDraw(drawing, guides);
guide_draw.draw_guides();
# define some helpers const to ease the reding of the code.
h_base = 8;  # horizontal guide number of the base
h_contour = 5;  # horizontal guide number
h_top = 0;  # horizontal guide number
h_lens = 6;  # horizontal guide number of the lenses plane
v_base = 0;  # vertical guide number
v_left = 2;  # vertical guide number
v_rigth = 4;  # vertical guide number
v_last = 11;  # vertical guide number
v_left_top = 7;  # vertical guide number
v_rigth_top = 10;  # vertical guide number
# draw the vertical cutting lines
guide_draw.draw_vertical_cut_line(v_base, h_contour, h_base);
guide_draw.draw_vertical_cut_line(v_left, h_contour, h_top);
guide_draw.draw_vertical_cut_line(v_rigth, h_contour, h_top);
guide_draw.draw_vertical_cut_line(v_last, h_contour, h_base);
# draw the upper horizontal cutting lines
guide_draw.draw_horizontal_cut_line(h_contour, v_base, v_left);
guide_draw.draw_horizontal_cut_line(h_top, v_left, v_rigth);
guide_draw.draw_horizontal_cut_line(h_contour, v_rigth, v_last);
# draw the base horizontal cutting lines
guide_draw.draw_horizontal_cut_line(h_base, v_base, v_left)
guide_draw.draw_horizontal_cut_line(h_base, v_left, v_rigth);
guide_draw.draw_horizontal_cut_line(h_base, v_rigth, v_left_top);
guide_draw.draw_horizontal_cut_line(h_base, v_left_top, v_rigth_top);
guide_draw.draw_horizontal_cut_line(h_base, v_rigth_top, v_last);
# draw the holes
guide_draw.draw_horizontal_hole_guide(v_base, h_lens, 20, 20, thickness);
# save the drawing as SVG
drawing.save();
print "goggle.svg created or updated"




