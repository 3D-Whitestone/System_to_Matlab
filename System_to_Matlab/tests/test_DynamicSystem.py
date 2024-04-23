import symengine as se
import filecmp
import os
from System_to_Matlab import DynamicSymbol, StaticSymbols, diff_t, Drehmatrix, DynamicSystem
import symengine as se

def create_sys():
    se.init_printing(pretty_print=True)

    params = StaticSymbols(["g", "m_2", "m_3", "s_2", "s_3", "l_2", "l_3", "B_{S1}", "A_{S2}", "B_{S2}", "C_{S2}", "A_{S3}", "B_{S3}", "C_{S3}", "i_{G1}", "i_{G2}", "i_{G3}", "B_{M1}", "C_{M2}", "C_{M3}"])

    [g, m2, m3, s2, s3, l2, l3, B_S1, A_S2, B_S2, C_S2, A_S3, B_S3, C_S3, i_G1, i_G2, i_G3, B_M1, C_M2, C_M3] = params
    param_values = [9.81, 1.866, 2.173, 0.125, 0.131, 0.25, 0.25, 0.103, 0.0036, 0.0159, 0.0170, 0.0021, 0.018, 0.0583, 72, 72, 72, 1.89e-5, 1.89e-5, 1.89e-5]

    q_var = DynamicSymbol("q",3,2)
    u_var = DynamicSymbol("M",3,0)

    [q,q_dot,q_ddot] = q_var.vars
    [[q1,q2,q3],[q1_dot, q2_dot, q3_dot],[q1_ddot, q2_ddot, q3_ddot]] = q_var.vars

    M_Mot1 = u_var.vars[0]
    M_Mot2 = u_var.vars[1]
    M_Mot3 = u_var.vars[2]

    RI1 = Drehmatrix([0,-q1,0])
    R1I = RI1.T

    R12 = Drehmatrix([0,0,se.pi/2 - q2])
    R21 = R12.T

    R13 = Drehmatrix([0,0,q3])
    R31 = R13.T

    RI2 = RI1 * R12
    R2I = RI2.transpose()

    RI3 = RI1 * R13
    R3I = RI3.transpose()

    R23 = R21 * R13
    R32 = R23.T

    M1_j_M1 = se.diag(*[0,B_M1*i_G1**2,0])

    M2_j_M2 = se.diag(*[0,0,C_M2*i_G2**2])

    M3_j_M3 = se.diag(*[0,0,C_M3*i_G3**2])

    K1_J_K1 = se.diag(*[0,B_S1,0])

    K2_J_K2 = se.diag(*[A_S2,B_S2,C_S2])

    K3_J_K3 = se.diag(*[A_S3,B_S3,C_S3])

    J1 = M1_j_M1 + K1_J_K1
    J2 = M2_j_M2 + K2_J_K2
    J3 = M3_j_M3 + K3_J_K3

    KS2_r_I =RI2 * se.Matrix([s2,0,0])
    KS3_r_I = RI2 * se.Matrix([l2,0,0]) + RI3 * se.Matrix([s3,0,0])
    KS2_r_S2 = se.Matrix([s2,0,0])
    KS3_R_S3 = R32 * KS2_r_S2.subs(s2,l2) + se.Matrix([s3,0,0])
    KI1_w_I = se.Matrix([0,-q1_dot,0])
    K12_w_2 = se.Matrix([0,0,-q2_dot])
    KI2_w_I = se.sympify(RI2 * (R2I * KI1_w_I + K12_w_2))
    K13_w_3 = se.Matrix([0,0,q3_dot])
    KI3_w_I = se.sympify(RI3 * (R3I * KI1_w_I + K13_w_3))
    KI1_w_1 = R1I * KI1_w_I
    KI2_w_2 = R21 * KI1_w_I + K12_w_2
    KI3_w_3 = R31 * KI1_w_I +  K13_w_3
    KI3_w_3 = se.sympify(KI3_w_3)

    KS2_v_I = diff_t(KS2_r_I)
    KS3_v_I = diff_t(KS3_r_I)
    KS2_v_2 = diff_t(KS2_r_S2) + KI2_w_2.cross(KS2_r_S2)
    KS3_v_3 = R3I * KS3_v_I

    P1 = se.Matrix([0,0,0])
    P2 = m2 * KS2_v_2
    P3 = m3 * KS3_v_3

    L1 = J1 * KI1_w_I
    L2 = J2 * KI2_w_2
    L3 = J3 * KI3_w_3  

    fe1 = se.Matrix([0,0     ,0])
    fe2 = R2I * se.Matrix([0, -m2*g,0])
    fe3 = R3I * se.Matrix([0, -m3*g,0])

    V2 = m2 * g * se.cos(q2) * s2
    V3 = g * l2 * m3 * se.cos(q2) + se.sin(q3)*g*m3*s3

    V = se.Matrix([V2 + V3]).jacobian(q).T

    Me1 = se.Matrix([0, -M_Mot1 * i_G1,0])
    Me2 = se.Matrix([0,0,-M_Mot2 * i_G2])
    Me3 = se.Matrix([0,0, M_Mot3 * i_G3])

    Jv1 = se.Matrix([0,0,0]).jacobian(q_dot)
    Jv2 = KS2_v_2.jacobian(q_dot)
    Jv3 = KS3_v_3.jacobian(q_dot)

    Jw1 = KI1_w_I.jacobian(q_dot)
    Jw2 = KI2_w_2.jacobian(q_dot)
    Jw3 = KI3_w_3.jacobian(q_dot)

    part1 = Jv1.T * (diff_t(P1) + (KI1_w_I.cross(P1) - fe1)) + Jw1.T * (diff_t(L1) + KI1_w_I.cross(L1) - Me1)
    part2 = Jv2.T * (diff_t(P2) + (KI2_w_2.cross(P2) - fe2)) + Jw2.T * (diff_t(L2) + KI2_w_2.cross(L2) - Me2)
    part3 = Jv3.T * (diff_t(P3) + (KI3_w_3.cross(P3) - fe3)) + Jw3.T * (diff_t(L3) + KI3_w_3.cross(L3) - Me3)

    eom = part1 + part2 + part3

    M_mat = eom.jacobian(q_ddot)
    g_vec = (eom - M_mat * q_ddot).expand()

    f = -M_mat.inv() * g_vec
    f = q_dot.col_join(f)

    Q = se.Matrix.multiply_elementwise(u_var.vars , se.Matrix([i_G1, i_G2, i_G3]))
    
    h = q.col_join(q_dot)
    sys = DynamicSystem(h,u_var.vars)
    sys.addStateEquations(f, add_as_Output=True)
    
    # sys.addOutput(h, "x")
    
    out1 = q1+q2 / q3
    sys.addCalculation(se.Symbol("out1"),out1)
    sys.addOutput(se.Symbol("out1"))
    # sys.addInput(se.Matrix(u_var.vars), "u")
    sys.addParameter(params, param_values)
    
    return sys

def test_DynamicSystem_values():
    # Test initialization with valid input
    sys = create_sys()

    q0 = se.Matrix([se.Symbol("q10",real=True),se.Symbol("q20",real=True),se.Symbol("q30",real=True),0,0,0])
    u0 = se.Matrix([se.Symbol("M10",real=True),se.Symbol("M20",real=True),se.Symbol("M30",real=True)])
    [A,B,C,D] = sys.linearize(q0,u0)
    
    path_test = os.path.dirname(os.path.abspath(__file__)) + "\\Test_System"
    
    sys.write_ABCD_to_File("ss_matrices",path_test)
    sys.write_init_File("init",path_test)
    sys.write_SFunction("Test",path_test)
    sys.write_MFunctions("Test",path_test)
    
    assert filecmp.cmp(path_test + "\\ss_matrices_ref.m", path_test + "\\ss_matrices.m", shallow = False) == True
    
    assert filecmp.cmp(path_test + "\\init_ref.m", path_test + "\\init.m", shallow = False) == True
    assert filecmp.cmp(path_test + "\\Test_ref.m", path_test + "\\Test.m", shallow = False) == True
    
    assert filecmp.cmp(path_test + "\\Test_dyn_ref.m", path_test + "\\Test_dyn.m", shallow = False) == True
    assert filecmp.cmp(path_test + "\\Test_out_ref.m", path_test + "\\Test_out.m", shallow = False) == True
    
    os.remove(path_test + "\\ss_matrices.m")
    os.remove(path_test + "\\init.m")
    os.remove(path_test +"\\Test.m")
    os.remove(path_test + "\\Test_dyn.m")
    os.remove(path_test + "\\Test_out.m")
