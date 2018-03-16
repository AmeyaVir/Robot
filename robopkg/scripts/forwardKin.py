#!/usr/bin/env python
import math
MATH_L1=0
MATH_L2=0
MATH_L3=14
MATH_L4=15.20
MATH_TRANS = 57.2958
def fwdKine(theta_1,theta_2,theta_3):
		coord=[0,1,2,3]
		g_l3_1 = MATH_L3 * math.cos(theta_2/MATH_TRANS)
		g_l4_1 = MATH_L4 * math.cos(theta_3 / MATH_TRANS);
  		g_l5 = (MATH_L2 + MATH_L3*math.cos(theta_2 / MATH_TRANS) + MATH_L4*math.cos(theta_3 / MATH_TRANS));

		coord[1] = -math.cos(abs(theta_1 / MATH_TRANS))*g_l5;
		coord[2] = -math.sin(abs(theta_1 / MATH_TRANS))*g_l5;
		coord[3] = MATH_L1 + MATH_L3*math.sin(abs(theta_2 / MATH_TRANS))-MATH_L4*math.sin(abs(theta_3 / MATH_TRANS));
		return coord

coordin=fwdKine(0,15,30)
print(coordin)
