if(Number of Poles = 1, (4 W/ft * Length *25* if(Number of Poles = 1, True Load / (Voltage * 0.9), if(Number of Poles = 2, True Load / (2 * Voltage * 0.9), if(Number of Poles = 3, True Load / (sqrt(3) * Voltage * 0.9), 0 A)))/ (13.3 * Voltage) / 1 A,
if(Number of Poles = 2, (2 W/ft * Length *25* if(Number of Poles = 1, True Load / (Voltage * 0.9), if(Number of Poles = 2, True Load / (2 * Voltage * 0.9), if(Number of Poles = 3, True Load / (sqrt(3) * Voltage * 0.9), 0 A)))/ (13.3 * Voltage) / 1 A,
if(Number of Poles = 3, (2 W/ft * 1.732 *25* Length * if(Number of Poles = 1, True Load / (Voltage * 0.9), if(Number of Poles = 2, True Load / (2 * Voltage * 0.9), if(Number of Poles = 3, True Load / (sqrt(3) * Voltage * 0.9), 0 A))) / (13.3 * VLR_CONDUCTORES POR FASE * Voltage) / 1 A,
0))

