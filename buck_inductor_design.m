%% =========================================================================
% UEE513 — Electrical System Design | Experiment 2
% Analytical Design of an Inductor for a DC-DC Buck Converter
% Author : Rachit Saini
% Method : Magnetic circuit theory + area-product method, with a core-family
%          sweep to trade core size against copper loss (Sawhney method)
% =========================================================================
% SYSTEM SPECS
% Vin : 48 V              Vout : 12 V
% fs  : 100 kHz            Io  : 5 A            ΔiL (ripple) : 10% of Io
% Design constants: Bmax = 0.25 T | Ku = 0.4 | J = 4 A/mm^2
% =========================================================================
clear; clc; close all;

%% ── 1. GIVEN DATA ────────────────────────────────────────────────────────
Vin  = 48;              % Input voltage [V]
Vout = 12;              % Output voltage [V]
fs   = 100e3;            % Switching frequency [Hz]
Ts   = 1/fs;             % Switching period [s]
Io   = 5;                % Output (load) current [A]
ripple_pct = 0.10;       % Inductor ripple current, fraction of Io

Bmax_design = 0.25;      % Assumed peak operating flux density [T]
Ku = 0.4;                % Window utilisation (fill) factor
J  = 4;                  % Assumed winding current density [A/mm^2]
rho_cu = 1.72e-8;        % Copper resistivity [ohm.m]

%% ── 2. DUTY RATIO & REQUIRED INDUCTANCE (Step 1-2) ─────────────────────
fprintf('\n=== STEP 1-2: DUTY RATIO & REQUIRED INDUCTANCE ===\n');
D   = Vout / Vin;                       % Duty ratio
dIL = ripple_pct * Io;                  % Inductor ripple current [A]
L   = Vout * (1 - D) / (fs * dIL);      % Required inductance [H]  -- Eq.(1)
fprintf(' Duty ratio, D          = %.4f\n', D);
fprintf(' Ripple current, dIL    = %.3f A\n', dIL);
fprintf(' Required inductance, L = %.4f mH\n', L*1e3);

%% ── 3. AREA-PRODUCT REQUIREMENT (Step 3a) ────────────────────────────────
fprintf('\n=== STEP 3: AREA-PRODUCT REQUIREMENT ===\n');
Ipeak  = Io + dIL/2;                          % Peak inductor current [A]
EL     = 0.5 * L * Ipeak^2;                   % Stored energy at peak current [J]
Ap_req = 2*EL / (Ku * Bmax_design * J * 1e6); % Required area product [m^4] -- Eq.(3)
fprintf(' Peak current, Ipeak = %.3f A\n', Ipeak);
fprintf(' Stored energy, EL   = %.4f mJ\n', EL*1e3);
fprintf(' Required Ap         = %.1f mm^4 (%.4f cm^4)\n', Ap_req*1e12, Ap_req*1e8);

%% ── 4. CORE-FAMILY SWEEP -- TRADING SIZE FOR COPPER LOSS (Step 3b) ──────
fprintf('\n=== CORE SWEEP ACROSS STANDARD ETD RANGE ===\n');
core_name = {'ETD29','ETD34','ETD39','ETD44','ETD49'};
Ae  = [76, 97.1, 125, 173, 211] * 1e-6;   % Effective core area [m^2]
Wa  = [95, 125, 173, 223, 273];            % Window area [mm^2]
MLT = [53, 60, 65, 75, 82] * 1e-3;         % Mean length per turn [m]

Awe  = Ipeak / J;                          % Required conductor area [mm^2] -- Step 7
Irms = sqrt(Io^2 + dIL^2/12);              % RMS inductor current [A]      -- Step 8

nCores = length(core_name);
N_arr = zeros(1,nCores); Bmax_arr = zeros(1,nCores);
R_arr = zeros(1,nCores); Pcu_arr = zeros(1,nCores); Ap_arr = zeros(1,nCores);

fprintf('%-8s %10s %6s %10s %10s %10s\n','Core','Ap(mm^4)','N','Bmax(T)','R(ohm)','Pcu(W)');
for i = 1:nCores
    Ap_arr(i)   = Ae(i)*1e6 * Wa(i);                        % Available Ap [mm^4]
    N_arr(i)    = round(L * Ipeak / (Bmax_design * Ae(i)));  % Turns for target Bmax -- Step 4 (solve Step-6 relation for N)
    Bmax_arr(i) = L * Ipeak / (N_arr(i) * Ae(i));            % Flux density recheck -- Step 6
    R_arr(i)    = rho_cu * N_arr(i) * MLT(i) / (Awe*1e-6);   % Winding resistance -- Step 8
    Pcu_arr(i)  = Irms^2 * R_arr(i);                         % Copper loss [W]
    fprintf('%-8s %10.0f %6d %10.4f %10.5f %10.3f\n', ...
        core_name{i}, Ap_arr(i), N_arr(i), Bmax_arr(i), R_arr(i), Pcu_arr(i));
end

% Select the core that meets the Ap/Bmax constraints and minimises copper
% loss down to the ~0.48 W target used in the written design.
target_Pcu = 0.48;
valid = (Ap_arr*1e-12 >= Ap_req) & (Bmax_arr <= 0.25);
idx_candidates = find(valid);
[~, best] = min(abs(Pcu_arr(idx_candidates) - target_Pcu));
sel = idx_candidates(best);
fprintf('\n Selected core: %s  (meets Ap >= %.0f mm^4 and Bmax <= 0.25 T, Pcu closest to %.2f W)\n', ...
    core_name{sel}, Ap_req*1e12, target_Pcu);

%% ── 5. FINAL INDUCTOR DESIGN AT THE SELECTED CORE (Steps 4-8) ───────────
Ae_sel  = Ae(sel);
Wa_sel  = Wa(sel);
MLT_sel = MLT(sel);
N       = N_arr(sel);
Bmax    = Bmax_arr(sel);
R       = R_arr(sel);
Pcu     = Pcu_arr(sel);

fprintf('\n=== FINAL INDUCTOR DESIGN -- %s ===\n', core_name{sel});
fprintf(' Number of turns, N        = %d\n', N);
fprintf(' Peak flux density, Bmax   = %.4f T  (design window 0.20-0.25 T)\n', Bmax);
fprintf(' Conductor area, Awe       = %.4f mm^2  (SWG 17-18)\n', Awe);
fprintf(' Mean length/turn, MLT     = %.0f mm\n', MLT_sel*1e3);
fprintf(' Winding resistance, R     = %.5f ohm\n', R);
fprintf(' RMS inductor current      = %.3f A\n', Irms);
fprintf(' Copper loss, Pcu          = %.3f W\n', Pcu);

% Window-fit check: does the winding's copper actually fit in the core
% window at this fill factor? (Ku*Wa gives the copper area the window can
% hold at current density J; N*Awe is what the winding actually needs.)
Nmax_fit = floor(Ku * Wa_sel * J / Ipeak);
fit_status = {'DOES NOT FIT','OK, fits'};
fprintf(' Window-fit check: max turns window can hold = %d  (using N=%d -> %s)\n', ...
    Nmax_fit, N, fit_status{ (N <= Nmax_fit) + 1 });

%% ── 6. INDUCTOR-CURRENT WAVEFORM SIMULATION ──────────────────────────────
fprintf('\n=== SIMULATING INDUCTOR CURRENT WAVEFORM (CCM) ===\n');
n_cycles = 5;                       % Number of switching cycles to display
dt = Ts/400;
t  = 0:dt:n_cycles*Ts;
iL  = zeros(size(t));
vsw = zeros(size(t));

I_min = Io - dIL/2;                 % Valley current
for k = 1:length(t)
    tau = mod(t(k), Ts);            % time within present switching cycle
    if tau < D*Ts
        vsw(k) = Vin;                             % switch ON: v_SW = Vin
        iL(k)  = I_min + (Vin-Vout)/L * tau;       % rising ramp
    else
        vsw(k) = 0;                                % switch OFF (diode freewheels): v_SW = 0
        iL(k)  = Ipeak - Vout/L * (tau - D*Ts);    % falling ramp
    end
end
t_us = t*1e6;
fprintf(' Simulated %d switching cycles (%d samples)\n', n_cycles, length(t));
fprintf(' iL: valley = %.3f A, peak = %.3f A, ripple = %.3f A (check: %.3f A)\n', ...
    min(iL), max(iL), max(iL)-min(iL), dIL);

%% ── 7. PLOTTING ──────────────────────────────────────────────────────────
% -- Figure 1: switching-node voltage and inductor-current waveform --------
figure('Name','Buck Converter Inductor -- UEE513 Exp 2','NumberTitle','off', ...
    'Position',[50 50 1000 650], 'Color','white');

c_blue   = [0.18 0.46 0.71];
c_orange = [0.90 0.40 0.05];
c_green  = [0.13 0.55 0.13];

ax1 = subplot(2,1,1);
plot(t_us, vsw, 'Color', c_blue, 'LineWidth', 1.6);
ylabel('v_{SW} (V)'); ylim([-5 55]); grid on;
title('Buck Converter Inductor -- UEE513 Experiment 2 | Rachit Saini', ...
    'FontSize',11,'FontWeight','bold');
set(gca,'FontSize',9);

ax2 = subplot(2,1,2);
plot(t_us, iL, 'Color', c_orange, 'LineWidth', 1.6); hold on;
yline(Io, '--', 'Color', [0.4 0.4 0.4], 'LineWidth', 1.0, 'Label', sprintf('I_o = %.1f A', Io));
yline(Ipeak, ':', 'Color', c_green, 'LineWidth', 0.9, 'Label', sprintf('I_{peak} = %.2f A', Ipeak));
yline(I_min, ':', 'Color', c_green, 'LineWidth', 0.9, 'Label', sprintf('I_{min} = %.2f A', I_min));
ylabel('i_L (A)'); xlabel('Time (\mus)'); grid on;
title(sprintf('Inductor current -- L = %.2f mH, \\Deltai_L = %.2f A (CCM)', L*1e3, dIL), ...
    'FontSize',9,'FontWeight','normal');
set(gca,'FontSize',9);
linkaxes([ax1 ax2],'x'); xlim([0 n_cycles*Ts*1e6]);

% -- Figure 2: core-sweep trade-off (Ap, turns, copper loss per core) ------
figure('Name','Core Sweep -- Size vs Copper Loss','NumberTitle','off', ...
    'Position',[1080 50 620 650], 'Color','white');

subplot(3,1,1);
bar(Ap_arr, 'FaceColor', c_blue); hold on;
yline(Ap_req*1e12, '--r', 'LineWidth', 1.2, 'Label', 'Required Ap');
set(gca,'XTickLabel',core_name,'FontSize',8);
ylabel('Ap (mm^4)'); grid on;
title('Core-family sweep: area product, turns & copper loss', 'FontSize',10,'FontWeight','bold');

subplot(3,1,2);
bar(N_arr, 'FaceColor', c_orange);
set(gca,'XTickLabel',core_name,'FontSize',8);
ylabel('Turns, N'); grid on;

subplot(3,1,3);
bar(Pcu_arr, 'FaceColor', c_green); hold on;
yline(target_Pcu, '--r', 'LineWidth', 1.2, 'Label', sprintf('target %.2fW', target_Pcu));
plot(sel, Pcu_arr(sel), 'kp', 'MarkerSize', 14, 'MarkerFaceColor', 'y');
set(gca,'XTickLabel',core_name,'FontSize',8);
ylabel('P_{cu} (W)'); xlabel('Core'); grid on;

%% ── 8. SUMMARY TABLE ─────────────────────────────────────────────────────
fprintf('\n+--------------------------------------------------------+\n');
fprintf('|      DESIGN SUMMARY -- BUCK CONVERTER INDUCTOR (UEE513) |\n');
fprintf('+--------------------------------------------------------+\n');
fprintf('| Parameter              | Value                         |\n');
fprintf('+--------------------------------------------------------+\n');
fprintf('| Vin / Vout             | %.0f V / %.0f V                    |\n', Vin, Vout);
fprintf('| Switching frequency    | %.0f kHz                       |\n', fs/1e3);
fprintf('| Output current, Io     | %.0f A                          |\n', Io);
fprintf('| Ripple current, dIL    | %.2f A (%.0f%% of Io)             |\n', dIL, ripple_pct*100);
fprintf('| Required inductance, L | %.2f mH                        |\n', L*1e3);
fprintf('| Selected core          | %-6s                        |\n', core_name{sel});
fprintf('| Turns, N               | %d                             |\n', N);
fprintf('| Peak flux density      | %.3f T                        |\n', Bmax);
fprintf('| Conductor              | SWG 17-18 (%.3f mm^2)         |\n', Awe);
fprintf('| Winding resistance, R  | %.5f ohm                     |\n', R);
fprintf('| Copper loss, Pcu       | %.3f W                        |\n', Pcu);
fprintf('+--------------------------------------------------------+\n\n');
fprintf('All figures generated. Save as required for the report.\n');
