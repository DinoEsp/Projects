## INPUTS ##

y = 2026 # Year
W_airframe = 0.5*32000 # Structural weight (lbs) = 40-50% of empty weight
V_Max = 1030 # Max Level airspeed in KTAS (knots true airspeed)
Q = 500 # Number of aircrafts to be produced
Q_M = 3 # Number of aircrafts produced in one month
Q_proto = 3 # Number of prototype aircraft to be produced
CPI = 1.26 # Inflation (approximate from 2020 to 2025)
N = 2 # Number of engines
K = 520 # Change to K = 436 for Turbojets OR K = 520 for Turbofans
T = 17700 # Static sea level thrust in lbf

CER_Category = 0
# Change the number above depending on the category you want to calculate
# 0. Engineering Cost
# 1. Tooling Cost
# 2. Manufacturing Cost
# 3. Development Support Cost
# 4. Flight Test Operations Cost
# 5. Quality Control Cost
# 6. Materials Cost

## END OF INPUTS ##

# For CER Table
F_cert = [0.67, 1, 0.75, 0.50, 0.50, 0.50, 0.75]
F_Comp = [2, 2, 1.25, 1.5, 1, 1.5, 1]
F_taper = [1, 0.95, 1, 1, 1, 1, 1]
F_cf = [1.03, 1.02, 1.01, 1.01, 1, 1, 1.02]
F_Press = [1.03, 1.01, 1, 1.03, 1, 1, 1.01]
# F_HyE = [1.33, 1.1, 1.1, 1.05, 1.5, 1.5, 1.05]
F_HyE = [1, 1, 1, 1, 1, 1, 1] # Replaced it with 1's to remove the coefficient

Cost_factor = F_cert[CER_Category] * F_Comp[CER_Category] * F_taper[CER_Category] * F_cf[CER_Category] * F_Press[CER_Category] * F_HyE[CER_Category]

# Hourly rates from lecture slides
R_T = 2.883*y-5666 # Tooling
R_E = 2.576*y-5058 # Engineering
R_QC = 2.60*y-5112 # Quality Check
R_M = 2.316*y-4552 # Manufacturing

# R = [R_E, R_T, R_M, 1, 1, R_QC, 1] 

# Recommended hourly rates from Finger's thesis
# I multiplied it by inflation since the numbers Finger gave is from 2020
# 1 means that the category equation doesn't consider hourly rates
R = [92*CPI, 61* CPI, 53*CPI, 1, 1, 1, 1]


# For the factor at the beginning of the equation
factor = [0.083, 2.1036, 20.2588, 0.06458, 0.009646, 0.13, 24.896]

# For exponent of W_airframe
W_exp = [0.791, 0.764, 0.74, 0.873, 1.16, 0, 0.689]

# For exponent of V_Max
V_exp = [1.521, 0.899, 0.543, 1.89, 1.3718, 0, 0.624]

# For exponent of Q
Q_exp = [0.183, 0.178, 0.524, 0.346, 0, 0, 0.792]

# For exponent of Q_proto
Q_proto_exp = [0, 0, 0, 0.346, 1.281, 0, 0]

# For exponent of Q_M
Q_M_exp = [0, 0.066, 0, 0, 0, 0, 0]

# Cost of quality control needs cost of manufacturing in its equation
x = CER_Category

if x == 5:
    y = 2
    Cost_factor_mfg = F_cert[y] * F_Comp[y] * F_taper[y] * F_cf[y] * F_Press[y] * F_HyE[y]
    C_mfg = factor[y] * (W_airframe**W_exp[y]) * (V_Max**V_exp[y]) * (Q**Q_exp[y]) * (Q_M**Q_M_exp[y]) * (Q_proto**Q_proto_exp[y]) * Cost_factor_mfg * R[y] * CPI
    C_eng = factor[x] * C_mfg * (W_airframe**W_exp[x]) * (V_Max**V_exp[x]) * (Q**Q_exp[x]) * (Q_M**Q_M_exp[x]) * (Q_proto**Q_proto_exp[x]) * Cost_factor * R[x] * CPI
    print(f"Chosen Man Cost: ${C_eng:,}")
else:
    #Cost for the selected category
    C_eng = factor[x] * (W_airframe**W_exp[x]) * (V_Max**V_exp[x]) * (Q**Q_exp[x]) * (Q_M**Q_M_exp[x]) * (Q_proto**Q_proto_exp[x]) * Cost_factor * R[x] * CPI
    print(f"Chosen Category Cost: ${C_eng:,}")

# CALCULATING TOTAL RDT&E, PRODUCTION, AND UNIT COST

# Total Cost for RDT&E

rdte = [0,3,4] # Numbers corresponding to the CER categories that are considered RDT&E
C_rdte = [ ]

for i in rdte:
    Cost_factor = F_cert[i] * F_Comp[i] * F_taper[i] * F_cf[i] * F_Press[i] * F_HyE[i]
    C_category = factor[i] * (W_airframe**W_exp[i]) * (V_Max**V_exp[i]) * (Q**Q_exp[i]) * (Q_M**Q_M_exp[i]) * (Q_proto**Q_proto_exp[i]) * Cost_factor * R[i] * CPI
    C_rdte.append(C_category)

C_rdte_tot = sum(C_rdte)

# Total production cost 

prod = [1,2,5,6] # Numbers corresponding to the CER categories that are considered production
C_prod = [ ]

for i in prod:
    if i == 5:
        y = 2
        Cost_factor_mfg = F_cert[y] * F_Comp[y] * F_taper[y] * F_cf[y] * F_Press[y] * F_HyE[y]
        C_mfg = factor[y] * (W_airframe**W_exp[y]) * (V_Max**V_exp[y]) * (Q**Q_exp[y]) * (Q_M**Q_M_exp[y]) * (Q_proto**Q_proto_exp[y]) * Cost_factor_mfg * R[y] * CPI
        Cost_factor = F_cert[i] * F_Comp[i] * F_taper[i] * F_cf[i] * F_Press[i] * F_HyE[i]
        C_category = factor[i] * C_mfg * (W_airframe**W_exp[i]) * (V_Max**V_exp[i]) * (Q**Q_exp[i]) * (Q_M**Q_M_exp[i]) * (Q_proto**Q_proto_exp[i]) * Cost_factor * R[i] * CPI
        C_prod.append(C_category)
    else:
        Cost_factor = F_cert[i] * F_Comp[i] * F_taper[i] * F_cf[i] * F_Press[i] * F_HyE[i]
        C_category = factor[i] * (W_airframe**W_exp[i]) * (V_Max**V_exp[i]) * (Q**Q_exp[i]) * (Q_M**Q_M_exp[i]) * (Q_proto**Q_proto_exp[i]) * Cost_factor * R[i] * CPI
        C_prod.append(C_category)

C_prod_tot = sum(C_prod)


# Total Engine cost
# Finger did not give an engine cost equation, so I'm using the one from the slides

CPI_eng = 2.01 # CPI from 1998 to 2025
engine_cost = N*K*(T**0.8356)*CPI_eng

# Total price
C_tot = C_prod_tot + C_rdte_tot
C_unit = ((C_rdte_tot+C_prod_tot)/Q)
C_unit_2 = C_unit + engine_cost

print(f"Total RDT&E Cost: ${C_rdte_tot:,}")
print(f"Total Production Cost: ${C_prod_tot:,}")
print(f"Total Cost of RDT&E and Production Combined: ${C_tot:,}\n") 
print(f"Total Engine Cost: ${engine_cost:,}")
print(f"Per Unit Cost w/o Engine: ${C_unit:,}")
print(f"Per Unit Cost w Engine: ${C_unit_2:,}")