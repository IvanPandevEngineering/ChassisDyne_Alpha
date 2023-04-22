'''
Ivan Pandev, March 2023

This document defines the application of the Runge-Kutta 4th Order, 2nd derivative
numerical iteration method to solve the x_dd matrix over time.
'''

import chassis_model as model

def RK4_iterator(
    dt, 
    self,  # Many static vehicle parameters passed in self
    a_fr, a_fl, a_rr, a_rl, b_fr, b_fl, b_rr, b_rl, c_fr, c_fl, c_rr, c_rl,  # Node position inputs
    a_d_fr, a_d_fl, a_d_rr, a_d_rl, b_d_fr, b_d_fl, b_d_rr, b_d_rl, c_d_fr, c_d_fl, c_d_rr, c_d_rl,  # Node velocity inputs
    I_roll_inst_f, I_roll_inst_r, I_pitch_inst_f, I_pitch_inst_r, I_roll_arm_inst_f, I_roll_arm_inst_r, I_pitch_arm_inst_f, I_pitch_arm_inst_r,  # Inertias, radii of rotation
    C_s_fr, C_s_fl, C_s_rr, C_s_rl,  # Springs and Dampers
    G_lat, G_long, G_lat_half_next, G_long_half_next, G_lat_next, G_long_next  # lateral and longitudinal acceleration in G
) -> tuple:

    F_mat = model.get_x_matrix(
        a_fr = a_fr, a_fl = a_fl, a_rr = a_rr, a_rl = a_rl, b_fr = b_fr, b_fl = b_fl, b_rr = b_rr, b_rl = b_rl, c_fr = c_fr, c_fl = c_fl, c_rr = c_rr, c_rl = c_rl,  # Node position inputs
        a_d_fr = a_d_fr, a_d_fl = a_d_fl, a_d_rr = a_d_rr, a_d_rl = a_d_rl, b_d_fr = b_d_fr, b_d_fl = b_d_fl, b_d_rr = b_d_rr, b_d_rl = b_d_rl, c_d_fr = c_d_fr, c_d_fl = c_d_fl, c_d_rr = c_d_rr, c_d_rl = c_d_rl,  # Node velocity inputs
        sm = self.sm, sm_f = self.sm_f, sm_r = self.sm_r, usm_f = self.usm_f, usm_r = self.usm_r,  # Masses
        I_roll_inst_f = I_roll_inst_f, I_roll_inst_r = I_roll_inst_r, I_pitch_inst_f = I_pitch_inst_f, I_pitch_inst_r = I_pitch_inst_r, I_roll_arm_inst_f = I_roll_arm_inst_f, I_roll_arm_inst_r = I_roll_arm_inst_r, I_pitch_arm_inst_f = I_pitch_arm_inst_f, I_pitch_arm_inst_r = I_pitch_arm_inst_r,  # Inertias, radii of rotation
        tw_f = self.tw_f, tw_r = self.tw_r, pitch_arm_f = self.pitch_arm_f, pitch_arm_r = self.pitch_arm_r, rc_height_f = self.rc_height_f, rc_height_r = self.rc_height_r, pc_height = self.pc_height, cm_height = self.cm_height, tire_diam_f = self.tire_diam_f, tire_diam_r = self.tire_diam_r,  # Vehicle geometries
        K_ch = self.K_ch, K_s_f = self.K_s_f, K_s_r = self.K_s_r, K_t_f = self.K_t_f, K_t_r = self.K_t_r, C_s_fr = C_s_fr, C_s_fl = C_s_fl, C_s_rr = C_s_rr, C_s_rl = C_s_rl, C_t_f = self.C_t_f, C_t_r = self.C_t_r,  # Springs and Dampers
        G_lat = G_lat, G_long = G_long  # lateral and longitudinal acceleration in G
    )
    x1_a_fr = dt * a_d_fr
    x1_a_fl = dt * a_d_fl
    x1_a_rr = dt * a_d_rr
    x1_a_rl = dt * a_d_rl
    x1_b_fr = dt * b_d_fr
    x1_b_fl = dt * b_d_fl
    x1_b_rr = dt * b_d_rr
    x1_b_rl = dt * b_d_rl
    v1_a_d_fr = dt * F_mat[0][0]
    v1_a_d_fr = dt * F_mat[1][0]
    v1_a_d_fr = dt * F_mat[2][0]
    v1_a_d_fr = dt * F_mat[3][0]
    v1_b_d_fr = dt * F_mat[4][0]
    v1_b_d_fr = dt * F_mat[5][0]
    v1_b_d_fr = dt * F_mat[6][0]
    v1_b_d_fr = dt * F_mat[7][0]

    F_mat_half_next_1 = model.get_x_matrix_1Dtest(
        self.m, F_sm_half_next, F_usm_half_next, self.K_s_f, self.C_lsc_f, self.K_t_f, self.C_t_f, a + x1_a/2, a_d + v1_a_d/2, b + x1_b/2, b_d + v1_b_d/2, c, c_d
    )
    x2_a = dt * (a_d + v1_a_d / 2)
    v2_a_d = dt * F_mat_half_next_1[0][0]
    x2_b = dt * (b_d + v1_b_d / 2)
    v2_b_d = dt * F_mat_half_next_1[1][0]
    
    F_mat_half_next_2 = model.get_x_matrix_1Dtest(
        self.m, F_sm_half_next, F_usm_half_next, self.K_s_f, self.C_lsc_f, self.K_t_f, self.C_t_f, a + x2_a/2, a_d + v2_a_d/2, b + x2_b/2, b_d + v2_b_d/2, c, c_d
    )
    x3_a = dt * (a_d + v2_a_d / 2)
    v3_a_d = dt * F_mat_half_next_2[0][0]
    x3_b = dt * (b_d + v2_b_d / 2)
    v3_b_d = dt * F_mat_half_next_2[1][0]

    F_mat_next = model.get_x_matrix_1Dtest(
        self.m, F_sm_next, F_usm_next, self.K_s_f, self.C_lsc_f, self.K_t_f, self.C_t_f, a + x3_a, a_d + v3_a_d, b + x3_b, b_d + v3_b_d, c, c_d
    )
    x4_a = dt * (a_d + v3_a_d)
    v4_a_d = dt * F_mat_next[0][0]
    x4_b = dt * (b_d + v3_b_d)
    v4_b_d = dt * F_mat_next[1][0]

    a_next = a + (x1_a + 2*x2_a + 2*x3_a + x4_a) / 6
    a_d_next = a_d + (v1_a_d + 2*v2_a_d + 2*v3_a_d + v4_a_d) / 6
    b_next = b + (x1_b + 2*x2_b + 2*x3_b + x4_b) / 6
    b_d_next = b_d + (v1_b_d + 2*v2_b_d + 2*v3_b_d + v4_b_d) / 6

    return a_next, a_d_next, b_next, b_d_next

def RK4_iterator_1Dtest(
    self, dt,
    a, a_d, b, b_d, c, c_d,
    F_sm, F_usm, F_sm_half_next, F_usm_half_next, F_sm_next, F_usm_next
) -> tuple:

    F_mat = model.get_x_matrix_1Dtest(
        self.m, F_sm, F_usm, self.K_s_f, self.C_lsc_f, self.K_t_f, self.C_t_f, a, a_d, b, b_d, c, c_d
    )
    x1_a = dt * a_d
    v1_a_d = dt * F_mat[0][0]
    x1_b = dt * b_d
    v1_b_d = dt * F_mat[1][0]

    F_mat_half_next_1 = model.get_x_matrix_1Dtest(
        self.m, F_sm_half_next, F_usm_half_next, self.K_s_f, self.C_lsc_f, self.K_t_f, self.C_t_f, a + x1_a/2, a_d + v1_a_d/2, b + x1_b/2, b_d + v1_b_d/2, c, c_d
    )
    x2_a = dt * (a_d + v1_a_d / 2)
    v2_a_d = dt * F_mat_half_next_1[0][0]
    x2_b = dt * (b_d + v1_b_d / 2)
    v2_b_d = dt * F_mat_half_next_1[1][0]
    
    F_mat_half_next_2 = model.get_x_matrix_1Dtest(
        self.m, F_sm_half_next, F_usm_half_next, self.K_s_f, self.C_lsc_f, self.K_t_f, self.C_t_f, a + x2_a/2, a_d + v2_a_d/2, b + x2_b/2, b_d + v2_b_d/2, c, c_d
    )
    x3_a = dt * (a_d + v2_a_d / 2)
    v3_a_d = dt * F_mat_half_next_2[0][0]
    x3_b = dt * (b_d + v2_b_d / 2)
    v3_b_d = dt * F_mat_half_next_2[1][0]

    F_mat_next = model.get_x_matrix_1Dtest(
        self.m, F_sm_next, F_usm_next, self.K_s_f, self.C_lsc_f, self.K_t_f, self.C_t_f, a + x3_a, a_d + v3_a_d, b + x3_b, b_d + v3_b_d, c, c_d
    )
    x4_a = dt * (a_d + v3_a_d)
    v4_a_d = dt * F_mat_next[0][0]
    x4_b = dt * (b_d + v3_b_d)
    v4_b_d = dt * F_mat_next[1][0]

    a_next = a + (x1_a + 2*x2_a + 2*x3_a + x4_a) / 6
    a_d_next = a_d + (v1_a_d + 2*v2_a_d + 2*v3_a_d + v4_a_d) / 6
    b_next = b + (x1_b + 2*x2_b + 2*x3_b + x4_b) / 6
    b_d_next = b_d + (v1_b_d + 2*v2_b_d + 2*v3_b_d + v4_b_d) / 6

    return a_next, a_d_next, b_next, b_d_next