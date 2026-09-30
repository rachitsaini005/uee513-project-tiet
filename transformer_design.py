"""
TRANSFORMER DESIGN CALCULATIONS (A.K. SAWHNEY — Using Python)
UEE513 — Electrical System Design | Lab Assignment 1, Q1

Bug-fixed version of the original program found in the assignment PDF.
Two corrections are made, each marked >>> FIX <<< at the point it applies:

  1. Mean-length-of-turn (MLT) unit mismatch. The prompts ask for LV/HV
     MLT "(mm)" and the code correctly divides by 1000 to convert to
     metres -- that part was always right. The bug was in the *example
     run*: the value entered was the Sawhney reference figure already in
     metres (0.462, 0.6667) typed straight into a field expecting mm, so
     it got divided by 1000 a second time. The fix is entering the actual
     mm figures (462, 666.7) -- the prompts below now say so explicitly
     so the mistake can't be repeated by accident.

  2. Copper-loss double unit-conversion. `cu_loss = m*(ipp**2*ref)` is
     already in watts (amps and ohms in, watts out -- no kW anywhere in
     that line). The original then did `total_loss = core_loss +
     cu_loss*1000`, i.e. multiplied an already-correct watt figure by
     1000 again before adding it to core_loss (also in watts). With the
     original (buggy) Ref -- which was ~1000x too small because of bug
     1 -- this *coincidentally* produced a plausible-looking total_loss
     and efficiency. With bug 1 fixed, that stray *1000 would now
     massively overstate total_loss, so it is removed here.

Everything else (every formula, every prompt, the overall structure) is
unchanged from the original.
"""
import math

print('TRANSFORMER DESIGN CALCULATIONS (A.K. SAWHNEY - Using Python)')
print('=' * 50)

# CORE DESIGN
print('CORE DESIGN')
kva = float(input('KVA rating: '))
f = float(input('Line frequency (Hz): '))
m = float(input('Number of phases: '))

# Using Voltage per Turn directly as per design sheet
et = float(input('Voltage per turn (Et): '))

bm = float(input('Flux density (Tesla): '))
ki = float(input('Stacking factor: '))

phlm = et / (4.44 * f)
ai_m2 = phlm / bm
ai_mm2 = ai_m2 * 1e6

print('Enter type of core: 1)Square 2)2-Stepped 3)3-Stepped 4)4-Stepped')
c = int(input('Choice: '))
ct_map = {1: 0.45, 2: 0.56, 3: 0.6, 4: 0.62}
ct = ct_map.get(c, 0.45)
d_mm = math.sqrt(ai_mm2 / ct)
print(f'Diameter of circumscribing circle: {d_mm:.2f} mm')

# WINDOW DESIGN
print('\nWINDOW DESIGN')
hw_mm = float(input('Height of window (mm): '))
ww_mm = float(input('Width of window (mm): '))
kw_factor = float(input('Window space factor (Kw): '))

# YOKE DESIGN
print('\nYOKE DESIGN')
ratioyl = float(input('Ratio - area of yoke to limbs: '))
dy_mm = float(input('Depth of yoke (mm): '))
ay_mm2 = ratioyl * ai_mm2
hy_mm = (ay_mm2 / ki) / dy_mm
print(f'Yoke height: {hy_mm:.4f} mm')

# LOW VOLTAGE (LV) WINDING DESIGN
print('\nLOW VOLTAGE (LV) WINDING DESIGN')
v_line_s = float(input('Secondary line voltage (V): '))
c1 = int(input('Type of connection: 1.Star 2.Delta: '))
vsp = v_line_s / math.sqrt(3) if c1 == 1 else v_line_s
ts = round(vsp / et)
isp = (kva * 1000) / (m * vsp)

delta_s = float(input('Secondary current density (A/mm^2): '))
as_area = float(input('Secondary conductor area (mm^2): '))
bs_mm = float(input('Radial depth of LV winding (mm): '))
h_lv_mm = float(input('Axial height of LV winding (mm): '))
# >>> FIX 1 <<< prompt now says explicitly this is millimetres, e.g. 462
# for a 0.462 m turn -- NOT 0.462 itself (that was the original bug).
mlt_s_mm = float(input('Mean length of turn for LV, in mm (e.g. 462 for a 0.462 m turn): '))

# HIGH VOLTAGE (HV) WINDING DESIGN
print('\nHIGH VOLTAGE (HV) WINDING DESIGN')
v_line_p = float(input('Primary line voltage (V): '))
c2 = int(input('Type of connection: 1.Star 2.Delta: '))
vpp = v_line_p / math.sqrt(3) if c2 == 1 else v_line_p
tp = round(ts * (vpp / vsp))
ipp = (kva * 1000) / (m * vpp)

delta_p = float(input('Primary current density (A/mm^2): '))
ap_area = float(input('Primary conductor area (mm^2): '))
bp_mm = float(input('Radial depth of HV winding (mm): '))
h_hv_mm = float(input('Axial height of HV winding (mm): '))
# >>> FIX 1 <<< same correction as the LV prompt above.
mlt_p_mm = float(input('Mean length of turn for HV, in mm (e.g. 666.7 for a 0.6667 m turn): '))

# INSULATION & DUCT
print('\nINSULATION')
cly_mm = float(input('Width of insulation duct between LV and HV (mm): '))

# ELECTRICAL PARAMETERS
print('\nELECTRICAL PARAMETERS')
rop = float(input('Resistivity of HV conductor (ohm-mm^2/m): '))
ros = float(input('Resistivity of LV conductor (ohm-mm^2/m): '))

# Resistance referred to primary
rp = (tp * (mlt_p_mm / 1000) * rop) / ap_area
rs = (ts * (mlt_s_mm / 1000) * ros) / as_area
ref = rp + (rs * (tp / ts) ** 2)
ep = (ipp * ref) / vpp

# Leakage Reactance (Sawhney Formula)
lmt_avg_m = (mlt_p_mm + mlt_s_mm) / (2 * 1000)
lc_avg_m = (h_lv_mm + h_hv_mm) / (2 * 1000)
mu_0 = 4 * math.pi * 1e-7

# Duct term in metres: Width + (Depth_LV + Depth_HV) / 3
duct_term_m = (cly_mm + (bs_mm + bp_mm) / 3) / 1000
xp = (2 * math.pi * f * mu_0 * (tp ** 2) * lmt_avg_m * duct_term_m) / lc_avg_m
epx = (ipp * xp) / vpp
epi = math.sqrt(ep ** 2 + epx ** 2)

# LOSSES AND EFFICIENCY
print('\nLOSSES AND EFFICIENCY')
w_limbs = float(input('Total weight of limbs (kg): '))
sl_limbs = float(input('Specific iron loss for limbs (W/kg): '))
w_yoke = float(input('Total weight of yoke (kg): '))
sl_yoke = float(input('Specific iron loss for yoke (W/kg): '))
core_loss = (w_limbs * sl_limbs) + (w_yoke * sl_yoke)
cu_loss = m * (ipp ** 2 * ref)          # already in watts
# >>> FIX 2 <<< cu_loss is in watts already -- no further scaling here.
total_loss = core_loss + cu_loss
efficiency = (kva * 1000 / (kva * 1000 + total_loss)) * 100

print('\n' + '=' * 40)
print('FINAL CALCULATED PARAMETERS')
print('=' * 40)
print(f'P.U. Resistance (ep): {ep:.5f}')
print(f'P.U. Reactance (epx): {epx:.5f}')
print(f'P.U. Impedance (epi): {epi:.5f}')
print('-' * 40)
print(f'Total Core Loss:      {core_loss:.2f} W')
print(f'Total Copper Loss:    {cu_loss/1000:.2f} kW')   # >>> FIX 2 <<< convert W -> kW for display here instead
print(f'Total Loss:           {total_loss:.2f} W')
print(f'Full Load Efficiency: {efficiency:.2f} %')
print('=' * 40)
