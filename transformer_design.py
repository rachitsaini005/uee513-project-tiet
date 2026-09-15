"""
================================================================================
 TRANSFORMER DESIGN CALCULATIONS (A.K. Sawhney method) -- Python conversion
 UEE513 -- Electrical System Design, Laboratory Assignment 1, Q2
 Converted from the sample MATLAB program supplied with the assignment
 (Lab_Assign-1.pdf), plus a Losses & Efficiency section added to complete
 the "overall design of transformer" the question asks for.
================================================================================

Every input() prompt below matches the corresponding MATLAB `input(...)`
prompt one-for-one, and every formula is the direct Python translation of
the MATLAB line it replaces (kept as an inline comment for cross-reference).
Two differences from a literal line-by-line port, both deliberate:

  1. Python's input() always returns a string, so numeric prompts are
     wrapped in float()/int() (MATLAB's input() parses numbers natively).
  2. Core/window/yoke/winding dimensions are converted from the base SI
     units the formulas naturally produce (metres, m^2) to mm / mm^2 for
     display -- the MATLAB source does this implicitly by how the numbers
     are typically keyed in; this conversion makes it explicit so the
     printed design sheet is directly readable, matching standard
     engineering design-sheet style.
"""

import math


def get_float(prompt):
    return float(input(prompt))


def get_int(prompt):
    return int(input(prompt))


def main():
    print("CORE DESIGN OF TRANSFORMER\n")
    print("Enter the following values:")
    KVA = get_float("KVA rating: ")

    print("voltage per turn calculation give k :\n"
          "1 0.75-0.85 for 1phase core\n"
          "2 0.45 for 3phase core\n"
          "3 1-1.2 for 1phase shell\n"
          "4 1.3 for 3phase shell\n")
    k = get_float("k: ")
    Et = k * math.sqrt(KVA)                                    # Et=k*sqrt(KVA);

    f = get_float("Line frequency: ")
    m = get_int("Number of phases: ")
    Bm = get_float("Flux density: ")
    Ki = get_float("Stacking factor: ")

    print("\nThe values of peak flux per pole, net iron area and Gross iron area calculated are")
    PHlm = Et / (4.44 * f)                                     # PHlm=Et/(4.44*f);
    Ai = PHlm / Bm                                             # Ai=PHlm/Bm  %net iron area
    Agi = Ai / Ki                                              # Agi=Ai/Ki   %gross core section area
    print(f"  Net iron area, Ai        = {Ai*1e6:.3f} mm^2")
    print(f"  Gross core section area  = {Agi*1e6:.3f} mm^2")

    print("\nEnter the type of core:\n1) Square\n2) Stepped\n3) 3-Stepped\n4) 4-Stepped")
    c = get_int("Choice: ")
    ct = {1: 0.45, 2: 0.56, 3: 0.6, 4: 0.62}[c]

    d = math.sqrt(Ai / ct)                                     # d=sqrt(Ai/ct)  %dia of circumscribing circle
    print(f"  Diameter of circumscribing circle, d = {d*1000:.2f} mm")

    if c == 1:
        a = math.sqrt(0.5) * d                                 # a=sqrt(0.5)*d  %width of largest stamping
        print(f"  Width of largest stamping, a = {a*1000:.2f} mm")
        stepped_dims = {"a": a}
    elif c == 2:
        a = 0.85 * d                                           # a=0.85*d
        b = 0.53 * d                                           # b=0.53*d
        print(f"  a = {a*1000:.2f} mm,  b = {b*1000:.2f} mm")
        stepped_dims = {"a": a, "b": b}
    elif c == 3:
        a = 0.42 * d                                           # a=0.42*d
        b = 0.7 * d                                            # b=0.7*d
        cc = 0.9 * d                                           # c=0.9*d  (renamed cc: 'c' already used for core-type choice)
        print(f"  a = {a*1000:.2f} mm,  b = {b*1000:.2f} mm,  c = {cc*1000:.2f} mm")
        stepped_dims = {"a": a, "b": b, "c": cc}
    else:  # c == 4
        a = 0.36 * d                                           # a=0.36*d
        b = 0.36 * d                                           # b=0.36*d
        cc = 0.78 * d                                          # c=0.78*d
        r = 0.92 * d                                           # r=0.92*d
        print(f"  a = {a*1000:.2f} mm,  b = {b*1000:.2f} mm,  c = {cc*1000:.2f} mm,  r = {r*1000:.2f} mm")
        stepped_dims = {"a": a, "b": b, "c": cc, "r": r}

    # ---------------------------------------------------------------
    print("\nWINDOW DESIGN OF TRANSFORMER\n")
    KV = get_float("Primary winding voltage: ")                # KV=input(...)  -- kept for fidelity; unused downstream, as in the source
    deltap = get_float("Primary current density: ")
    Kw = get_float("Enter window space factor: ")
    # Aw=(KVA*1000)/(3.33*Bm*f*Kw*deltap*Ai)  %window area  -- deltap here in A/mm^2, Ai in m^2, Aw in m^2 x 1e-6 handled via deltap*1e6
    Aw = (KVA * 1000) / (3.33 * Bm * f * Kw * (deltap * 1e6) * Ai)
    print(f"  Window area, Aw = {Aw*1e6:.3f} mm^2")

    ratiohw = get_float("Ratio - height to width of window in the range of 2-4: ")
    print("\nThe window width and window height are")
    Ww = math.sqrt(Aw / ratiohw)                               # Ww=sqrt(Aw/ratiohw)  %window width
    Hw = Ww * ratiohw                                          # Hw=Ww*ratiohw  %window height
    print(f"  Window width,  Ww = {Ww*1000:.3f} mm")
    print(f"  Window height, Hw = {Hw*1000:.3f} mm")

    # ---------------------------------------------------------------
    print("\nYOKE DESIGN OF TRANSFORMER\n")
    ratioyl = get_float("ratio - area of yoke to limbs: ")
    Dy = get_float("Depth of yoke (m): ")
    print("\nThe flux density in yoke, yoke area, gross yoke area and height of yoke are calculated as")
    FDy = Bm / ratioyl                                         # FDy=Bm/ratioyl  %flux density in yoke
    Ay = ratioyl * (PHlm / Bm)                                 # Ay=ratioyl*(PHlm/Bm)  %yoke area   [== ratioyl*Ai]
    Agy = Ay / Ki                                              # Agy=Ay/Ki  %gross area of yoke
    Hy = Agy / Dy                                              # Hy=Agy/Dy  %height of yoke
    print(f"  Flux density in yoke = {FDy:.4f} Wb/m^2")
    print(f"  Yoke area, Ay        = {Ay*1e6:.3f} mm^2")
    print(f"  Gross yoke area      = {Agy*1e6:.3f} mm^2")
    print(f"  Height of yoke, Hy   = {Hy*1000:.4f} mm")

    # ---------------------------------------------------------------
    print("\nOVERALL DIMENSION OF TRANSFORMER\n")
    print("The distance between core centers, height, width and depth of transformer are obtained as")
    D = d + Ww                                                 # D=d+Ww  %dist between adjacent core centres
    H = Hw + 2 * Hy                                            # H=Hw+2*Hy  %height of frame
    W = 2 * D + Dy                                             # W=2*D+Dy  %width of frame
    Df = Dy                                                    # Df=Dy  %depth of frame
    print(f"  D (centre distance) = {D*1000:.3f} mm")
    print(f"  H (height of frame) = {H*1000:.3f} mm")
    print(f"  W (width of frame)  = {W*1000:.3f} mm")
    print(f"  Df (depth of frame) = {Df*1000:.3f} mm")

    # ---------------------------------------------------------------
    print("\nLOW VOLTAGE WINDING DESIGN OF TRANSFORMER\n")
    Vls = get_float("Secondary line voltage: ")
    c1 = get_int("Type of connection: \n1.Star\n2.Delta:\n")
    Vsp = Vls / math.sqrt(3) if c1 == 1 else Vls               # switch c1: Vsp=Vls/sqrt(3) (star) / Vsp=Vls (delta)
    print("\nThe no of turns per phase and current per phase of LV winding are")
    Ts = round(Vsp / Et)                                       # Ts=round(Vsp/Et)  %no of turns per phase
    Isp = (KVA * 1000) / (3 * Vsp)                             # Isp=(KVA*1000)/(3*Vsp)  %secondary current per phase
    print(f"  Turns per phase, Ts = {Ts}")
    print(f"  Secondary current per phase, Isp = {Isp:.4f} A")

    delta_s = get_float("Enter secondary current density: ")
    print("\nThe area of conductor of LV winding is")
    as_ = Isp / delta_s                                        # as=Isp/delta  %area of secondary conductor
    print(f"  Secondary conductor area, as = {as_:.3f} mm^2")

    print("\nLet us choose copper rectangular conductors and paper insulation for these conductors.")
    x = get_float("Width of conductor along height of window (mm): ")
    y = get_float("Width of conductor along width of window (mm): ")
    z = get_float("Increase in dimensions because of insulation (mm): ")
    x1 = x + z                                                 # x1=x+z
    y1 = y + z                                                 # y1=y+z  %dimension with covering
    print(f"  x1 = {x1:.3f} mm,  y1 = {y1:.3f} mm")

    ly = get_int("Number of layers: ")
    print("Using helical winding:")
    Ts1 = round((Ts / ly) + 1)                                 # Ts1=round((Ts/ly)+1)  %turns along axial length
    Lcs = Ts1 * x1                                             # Lcs=Ts1*x1  %axial length of lv winding (mm)
    cls_ = (Hw * 1000 - Lcs) / 2                                # cls=(Hw*1000-Lcs)/2  %clearance
    print(f"  Turns along axial length, Ts1 = {Ts1}")
    print(f"  Axial length of LV winding, Lcs = {Lcs:.3f} mm")
    print(f"  Clearance = {cls_:.3f} mm")
    if cls_ < 6:                                               # if(cls<6) ... end
        print("  clearance is <6. Min limit not satisfied")

    cly_lv = get_float("Enter thickness of pressboard cylinders (mm): ")
    bs = 2 * ly * y1 + cly_lv                                  # bs=2*ly*y1+cly  %radial depth of lv winding
    print(f"  Radial depth of LV winding, bs = {bs:.3f} mm")

    lvi = get_float("Enter thickness of insulation between LV winding and core (mm): ")
    print("\nThe inside, outside, mean dia of LV winding and its mean length of turn are")
    Idl = d * 1000 + 2 * lvi                                   # Idl=d*1000+2*lvi  %inside diameter
    Odl = Idl + 2 * bs                                         # Odl=Idl+2*bs  %outside diameter
    Mdl = (Idl + Odl) / 2                                      # Mdl=(Idl+Odl)/2  %Mean diameter
    Mlt_lv = math.pi * Mdl                                     # Mlt=pi*Mdl  %Mean length of turn (mm)
    print(f"  Idl = {Idl:.3f} mm,  Odl = {Odl:.3f} mm,  Mdl = {Mdl:.3f} mm,  MLT = {Mlt_lv:.3f} mm")

    # ---------------------------------------------------------------
    print("\nHIGH VOLTAGE WINDING DESIGN OF TRANSFORMER\n")
    Vlp = get_float("primary line voltage: ")
    c1 = get_int("Type of connection: \n1.Star\n2.Delta:\n")
    Vpp = Vlp / math.sqrt(3) if c1 == 1 else Vlp               # Vpp=Vlp/sqrt(3) (star) / Vpp=Vlp (delta)
    print("\nThe no of turns per phase and current per phase of HV winding are")
    Tp = round(Ts * (Vpp / Vsp))                               # Tp=round(Ts*(Vpp/Vsp))  %no of turns
    Ipp = (KVA * 1000) / (3 * Vpp)                             # Ipp=(KVA*1000)/(3*Vpp)  %primary current per phase
    print(f"  Turns per phase, Tp = {Tp}")
    print(f"  Primary current per phase, Ipp = {Ipp:.4f} A")

    delta_p = get_float("primary current density: ")
    print("\nLet us choose copper round conductors")
    print("The area of conductor of HV winding, dia of conductor, total copper area in window and window space factor are")
    ap = Ipp / delta_p                                         # ap=Ipp/delta  %area of primary conductor
    dp = math.sqrt((4 * ap) / math.pi)                         # dp=sqrt((4*ap)/pi)  %diameter of conductor
    Acw = 2 * (ap * Tp + as_ * Ts)                              # Acw=2*(ap*Tp+as*Ts)  %total copper area in window (mm^2)
    Kw_actual = Acw / (Aw * 1e6)                                # Kw=Acw/(Aw*10000)  -- Aw here converted to cm^2 in MATLAB; kept equivalent in mm^2
    print(f"  Primary conductor area, ap = {ap:.4f} mm^2")
    print(f"  Diameter of conductor, dp = {dp:.4f} mm")
    print(f"  Total copper area in window, Acw = {Acw:.3f} mm^2")
    print(f"  Actual window space factor = {Kw_actual:.4f}")

    ca = get_int("Number of coils in HV winding (volt/coil should not exceed 1500V): ")
    ta = get_int("Number of turns in each coil of HV winding: ")
    tec = Tp - ca * ta                                         # tec=Tp-ca*ta  %Number of turns in end coil
    ly_hv = get_int("Number of layers of normal coil: ")
    tly = get_int("Turns per layer of normal coil: ")
    Mxvly = 2 * tly * (Vlp / Tp)                               # Mxvly=2*tly*(Vlp/Tp)  %Max voltage between layers
    print(f"  Turns in end coil = {tec},  Max voltage between layers = {Mxvly:.2f} V")

    sci = get_float("Size of conductor with insulation (mm): ")
    adn = tly * sci                                            # adn=tly*sci  %axial depth of normal coil
    lye = get_int("Number of layers of end coil: ")
    tlye = get_int("Turns per layer of end coil: ")
    ade = tlye * sci                                           # ade=tlye*sci  %axial depth of end coil
    sp = get_float("Height of spaces used between adjacent coils (mm): ")
    Lcp = ca * adn + ade + ca * sp                             # Lcp=ca*adn+ade+ca*sp  %axial length of HV winding
    Cl = (Hw * 1000 - Lcp) / 2                                 # Cl=(Hw-Lcp)/2  %clearance   (Hw converted to mm for consistency)
    print(f"  Axial length of HV winding, Lcp = {Lcp:.3f} mm,  clearance = {Cl:.3f} mm")

    cly_hv = get_float("Thickness of insulation between layers (mm): ")
    bp = ly_hv * sci + (ly_hv - 1) * cly_hv                    # bp=ly*sci+(ly-1)*cly  %radial depth of HV coil
    T = 5 + ((0.9 * Vlp) / 1000)                               # T=5+((0.9*Vlp)/1000)
    Idh = ca * adn + 2 * T                                     # Idh=ca*adn+2*T  %inside diameter
    Odh = Idh + 2 * ade                                        # Odh=Idh+2*ade  %outside diameter
    Mdh = (Idh + Odh) / 2                                      # Mdh=(Idh+Odh)/2  %Mean diameter
    print(f"  Radial depth of HV winding, bp = {bp:.3f} mm")
    print(f"  Idh = {Idh:.3f} mm,  Odh = {Odh:.3f} mm,  Mdh = {Mdh:.3f} mm")

    # ---------------------------------------------------------------
    print("\nRESISTANCE DESIGN OF TRANSFORMER\n")
    Lmtp = (math.pi * Mdh) / 1000                              # Lmtp=(pi*Mdh)/1000  %length of mean turn in HV winding (m)
    rop = get_float("Resistivity of material in HV winding (ohm-mm^2/m): ")
    print("The Resistance of conductor of HV winding is")
    Rp = (Tp * Lmtp * rop) / ap                                # Rp=(Tp*Lmtp*rop)/ap  %resistance in HV side
    print(f"  Lmtp = {Lmtp*1000:.3f} mm,  Rp = {Rp:.4f} ohm")

    Lmts = (math.pi * Mdl) / 1000                              # Lmts=(pi*Mdl)/1000  %length of mean turn in LV winding (m)
    ros = get_float("Resistivity of material in LV winding (ohm-mm^2/m): ")
    print("The Resistance of conductor of LV winding, resistance referred to HV side and per-unit resistance are")
    Rs = (Ts * Lmts * ros) / as_                               # Rs=(Ts*Lmts*ros)/as  %resistance in LV side
    Ref = Rp + (((Tp * Tp) / (Ts * Ts)) * Rs)                  # Ref=Rp+(((Tp*Tp)/(Ts*Ts))*Rs)  %Resistance referred to primary
    ep = (Ipp * Ref) / Vlp                                     # ep=(Ipp*Ref)/Vlp  %per unit resistance
    print(f"  Lmts = {Lmts*1000:.3f} mm,  Rs = {Rs:.5f} ohm")
    print(f"  Resistance referred to primary, Ref = {Ref:.4f} ohm")
    print(f"  Per-unit resistance, ep = {ep:.5f}")

    # ---------------------------------------------------------------
    print("\nLEAKAGE REACTANCE DESIGN OF TRANSFORMER\n")
    Dm = (Odl + Odh) / 2                                       # Dm=(Odl+Odh)/2  %Mean diameter of windings
    Lmt = (math.pi * Dm) / 1000                                # Lmt=(pi*Dm)/1000  %Length of mean turn of winding
    Lc = (Lcp + Lcs) / 2                                       # Lc=(Lcp+Lcs)/2  %Mean axial length of winding
    print("The leakage reactance referred to HV side and per-unit impedance are")
    Xp = (2 * math.pi * f * 4 * math.pi * 10e-7 * Tp * Tp * Lmt * (T + (bp + bs) / 3)) / Lc   # Xp=... %Leakage reactance
    epx = (Ipp * Xp) / Vpp                                     # epx=(Ipp*Xp)/Vpp  %per unit leakage reactance
    epi = math.sqrt((ep * ep) + (epx * epx))                   # epi=sqrt((ep*ep)+(epx*epx))  %per unit impedance
    print(f"  Xp = {Xp:.4f} ohm,  epx = {epx:.5f},  epi (p.u. impedance) = {epi:.5f}")

    # =================================================================
    # LOSSES AND EFFICIENCY  -- not part of the supplied MATLAB snippet
    # (which stops at leakage reactance); added here to complete the
    # "overall design of transformer" Q2 asks for, using standard
    # weight = density x volume and core-loss = weight x specific-loss
    # relations, and I^2R copper loss from the resistance section above.
    # =================================================================
    print("\nLOSSES AND EFFICIENCY\n")
    density = get_float("Density of core steel (kg/m^3) [typical CRGO ~7600-7650]: ")
    wt_limb = density * m * Ai * Hw                            # weight of the m wound limbs (net iron volume x density)
    wt_yoke = density * 2 * Ay * W                              # weight of the 2 yokes (top+bottom)
    print(f"  Total weight of limbs = {wt_limb:.3f} kg")
    print(f"  Total weight of yoke  = {wt_yoke:.3f} kg")

    sp_loss_limb = get_float("Specific iron loss for limbs (W/kg): ")
    sp_loss_yoke = get_float("Specific iron loss for yoke (W/kg): ")
    core_loss = wt_limb * sp_loss_limb + wt_yoke * sp_loss_yoke
    print(f"  Total core loss = {core_loss:.2f} W")

    Pcu = m * Ipp * Ipp * Ref                                  # I^2R loss, m phases, primary current & referred resistance
    print(f"  Total copper loss = {Pcu/1000:.2f} kW")

    total_loss = core_loss + Pcu
    output_w = KVA * 1000
    efficiency = 100 * output_w / (output_w + total_loss)
    print(f"  Total loss = {total_loss:.2f} W")
    print(f"  Full load efficiency = {efficiency:.2f} %")

    print("\n" + "=" * 60)
    print("DESIGN SHEET SUMMARY")
    print("=" * 60)
    print(f"{'Core diameter (d)':35s}{d*1000:>10.2f} mm")
    print(f"{'Window (Ww x Hw)':35s}{Ww*1000:>6.1f} x {Hw*1000:.1f} mm")
    print(f"{'Yoke height (Hy)':35s}{Hy*1000:>10.2f} mm")
    print(f"{'Turns (LV / HV)':35s}{Ts:>6d} / {Tp}")
    print(f"{'Total core loss':35s}{core_loss:>10.2f} W")
    print(f"{'Total copper loss':35s}{Pcu/1000:>10.2f} kW")
    print(f"{'Full load efficiency':35s}{efficiency:>10.2f} %")


if __name__ == "__main__":
    main()
