class IceDims:
    def __init__(self):
        '''
        All dims in feet.
        Based off image at: https://en.wikipedia.org/wiki/Ice_hockey_rink#/media/File:Ice_hockey_layout.svg

        y = "bottom" to "top"
        x = "end" to "end"
        x = 0 @ center line
        ref crease starts at y = 0
        '''
        self.length = 200
        self.width = 85
        self.end_to_goal = 11
        self.blue_line_to_blue_line = 50
        self.goal_line_to_blue_line = 64
        self.fo_circle_rad = 15
        self.nz_dot_spread = 44
        self.nz_bl_offset = 5
        self.crease_width = 8
        self.goal_width = 6
        self.ref_crease_rad = 10
        self.fo_line_thickness = 2/12
        self.center_dot_rad = 0.5
        self.fo_dot_rad = 1
        self.trap_at_boards = 28
        self.trap_at_gl = 22
        self.corner_rad = 28
        self.gl_to_circle = 20
        self.lower_dot_y = self.width/2 - 22
        self.upper_dot_y = self.lower_dot_y + 44
        self.l_dot_x = self.end_to_goal + self.gl_to_circle
        self.r_dot_x = self.length - self.l_dot_x
        self.nz_l_dot_x = self.goal_line_to_blue_line + self.end_to_goal + self.nz_bl_offset
        self.nz_r_dot_x = self.nz_l_dot_x + self.nz_dot_spread

        # --Coords-- #
        self.center = dict(x=0, y=self.width/2)
        self.center_line = dict(x0=0.5, x1=-0.5, y0=0, y1=85)
        self.l_blue_line = dict(x0=-25, x1=-26, y0=0, y1=85)  # x0 > closer to center
        self.r_blue_line = dict(x0=25, x1=26, y0=0, y1=85)  # x0 > closer to center
        self.l_lower_dot = dict(x=self.l_dot_x, y=self.lower_dot_y)
        self.l_upper_dot = dict(x=self.l_dot_x, y=self.upper_dot_y)
        self.r_lower_dot = dict(x=self.r_dot_x, y=self.lower_dot_y)
        self.r_upper_dot = dict(x=self.r_dot_x, y=self.upper_dot_y)
        self.l_nz_upper = dict(x=self.nz_l_dot_x, y=self.upper_dot_y)
        self.l_nz_lower = dict(x=self.nz_l_dox_x, y=self.lower_dot_y)
        self.r_nz_upper = dict(x=self.nz_r_dot_x, y=self.upper_dot_y)
        self.r_nz_lower = dict(x=self.nz_r_dot_x, y=self.lower_dot_y)
        self.l_gl = dict(x0=11, x1=11+(2/12), y0=0, y1=85)
        self.r_gl = dict(x0=200-11, x1=200-11-(2/12), y0=0, y1=85)


