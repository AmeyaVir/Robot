import math
MATH_L1=0.0821+3.0028
MATH_L2=1.3132
MATH_L3=13.97
MATH_L4=15.2
MATH_L43=MATH_L4/MATH_L3
MATH_TRANS = 57.2958

class Uarm(object):
	
    
	uarm = None
	kAddrOffset = 90
	kAddrAandB = 60

	uarm_status = 0
	pin2_status = 0
	coord = {}
	g_interpol_val_arr = {}
	angle = {}
    
	def fwdKine(self,theta_1,theta_2,theta_3):
		coord=[0,1,2,3]
		g_l3_1 = MATH_L3 * math.cos(theta_2/MATH_TRANS)
		g_l4_1 = MATH_L4 * math.cos(theta_3 / MATH_TRANS);
		g_l5 = -(MATH_L2 + MATH_L3*math.cos(theta_2 / MATH_TRANS) + MATH_L4*math.cos(theta_3 / MATH_TRANS));
		coord[1] = -math.cos(abs(theta_1 / MATH_TRANS))*g_l5;
		coord[2] = -math.sin(abs(theta_1 / MATH_TRANS))*g_l5;
		coord[3] = MATH_L1 + MATH_L3*math.sin(abs(theta_2 / MATH_TRANS))+MATH_L4*math.sin(abs(theta_3 / MATH_TRANS));
		return coord
    
	def ivsKine(self, x, y, z):
		if z > (MATH_L1 + MATH_L3):
			z = MATH_L1 + MATH_L3 
		if z < (MATH_L1 - MATH_L4):
			z = MATH_L1 - MATH_L4

		g_x_in = (-x-MATH_L2)/MATH_L3
		g_z_in = (z - MATH_L1) / MATH_L3
		g_right_all = (1 - g_x_in*g_x_in - g_z_in*g_z_in - MATH_L43*MATH_L43) / (2 * MATH_L43)
		g_sqrt_z_x = math.sqrt(g_z_in*g_z_in + g_x_in*g_x_in)

		if y == -3:
			# Calculate value of theta 1
			g_theta_1 = 90;
			# Calculate value of theta 3
			if g_z_in == 0:
				g_phi = 90
			else:
				g_phi = math.atan(-g_x_in / g_z_in)*MATH_TRANS
			if g_phi > 0:
				g_phi = g_phi - 180
				g_theta_3 = math.asin(g_right_all / g_sqrt_z_x)*MATH_TRANS - g_phi

	    		if g_theta_3<0:
				g_theta_3 = 0
			# Calculate value of theta 2
	    		g_theta_2 = math.asin((z + MATH_L4*math.sin(g_theta_3 / MATH_TRANS) - MATH_L1) / MATH_L3)*MATH_TRANS
		else:
			# Calculate value of theta 1
			g_theta_1 = math.atan(y / x)*MATH_TRANS
			if (y/x) > 0:
				g_theta_1 = g_theta_1
			if (y/x) < 0:
				g_theta_1 = g_theta_1 + 180
			if y == 0:
				if x > 0:
					g_theta_1 = 180
				else: 
					g_theta_1 = 0
			# Calculate value of theta 3
			g_x_in = (-x / math.cos(g_theta_1 / MATH_TRANS) - MATH_L2) / MATH_L3;
			if g_z_in == 0:  
				g_phi = 90
			else:
				g_phi = math.atan(-g_x_in / g_z_in)*MATH_TRANS
			if g_phi > 0:
				g_phi = g_phi - 180 

			g_sqrt_z_x = math.sqrt(g_z_in*g_z_in + g_x_in*g_x_in)

			g_right_all_2 = -1 * (g_z_in*g_z_in + g_x_in*g_x_in + MATH_L43*MATH_L43 - 1) / (2 * MATH_L43)
			g_theta_3 = math.asin(g_right_all_2 / g_sqrt_z_x)*MATH_TRANS
			g_theta_3 = g_theta_3 - g_phi

			if g_theta_3 <0 :
				g_theta_3 = 0
			# Calculate value of theta 2
			g_theta_2 = math.asin(g_z_in + MATH_L43*math.sin(abs(g_theta_3 / MATH_TRANS)))*MATH_TRANS

		g_theta_1 = abs(g_theta_1);
		g_theta_2 = abs(g_theta_2);
		print(g_theta_1,g_theta_2,g_theta_3)

		if g_theta_3 < 0 :
			pass
		else:
			coord=self.fwdKine(g_theta_1,g_theta_2, g_theta_3)
			print(coord)
			if (coord[2]>y+0.1) or (coord[2]<y-0.1):
				g_theta_2 = 180 - g_theta_2

		if(math.isnan(g_theta_1) or math.isinf(g_theta_1)):
			g_theta_1 = self.readAngle(1)
		if(math.isnan(g_theta_2) or math.isinf(g_theta_2)):
			g_theta_2 = self.readAngle(2)
		if(math.isnan(g_theta_3) or math.isinf(g_theta_3) or (g_theta_3<0)):
			g_theta_3 = self.readAngle(3)
		
		self.angle[1] = g_theta_1
		self.angle[2] = g_theta_2
		self.angle[3] = g_theta_3
		self.angle[3]=self.angle[2]+self.angle[3]
		self.angle[2]=-self.angle[2]
		return self.angle

		pass
