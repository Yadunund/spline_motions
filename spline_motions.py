#!/usr/bin/env python3

def compute_coefficients(initial_position, final_position, initial_velocity, final_velocity, initial_time, final_time):
    td = final_time-initial_time
    x0 = initial_position
    x1 = final_position
    v0 = initial_velocity
    v1 = final_velocity
    w0 = v0/td
    w1 = v1/td
    
    a = w1 + w0 -2*x1 + 2*x0
    b = -w1 - 2*w0 +3*x1 -3*x0
    c = w0
    d = x0
    
    return [a,b,c,d]

def get_coefficients(knots):
    '''
    This function takes a list of dictionaries representing knots of segments in a trajectory.
    It returns a list of dictionaries containing the a,b,c,d coefficients of the 
    x, y and th spline-motions between successive knots
    
    x(t) = a_x*s(t)^3 + b_x*s(t)^2 + c_x*s(t) + d_x 
    y(t) = a_y*s(t)^3 + b_y*s(t)^2 + c_y*s(t) + d_x 
    th(t) = a_th*s(t)^3 + b_th*s(t)^2 + c_th*s(t) + d_x 

    s(t) = (t- t_i)/(t_f - t_i)
    t, t_i and t_f are all in same units 
    
    Example knots
    knots = [ {"x":[5,8,0],"v": [1,0,0],"t":0} , {"x":[0,0,0], "v": [0,0,0], "t":10} ]

    '''
    coefficients = []
    for i in range(len(knots)-1):
        d = {}
        knot_i = knots[i]
        knot_f = knots[i+1]
        x_coeffs = compute_coefficients(knot_i["x"][0], knot_f["x"][0], knot_i["v"][0], knot_f["v"][0], knot_i["t"], knot_f["t"])
        y_coeffs = compute_coefficients(knot_i["x"][1], knot_f["x"][1], knot_i["v"][1], knot_f["v"][1], knot_i["t"], knot_f["t"])
        th_coeffs = compute_coefficients(knot_i["x"][2], knot_f["x"][2], knot_i["v"][2], knot_f["v"][2], knot_i["t"], knot_f["t"])
        
        d["x_coeffs"] = x_coeffs
        d["y_coeffs"] = y_coeffs
        d["th_coeffs"] = th_coeffs
        d["t_i"] = knot_i["t"]
        d["t_f"] = knot_f["t"]
        
        coefficients.append(d)
        
    return coefficients
        
def st(t, t_i,t_f):
    return (t-t_i)/(t_f-t_i)

def get_position(t, coefficients):
    spline_index = -1
    for coeff in coefficients:
        if (t>=coeff["t_i"] and t<=coeff["t_f"]):
            spline_index = coefficients.index(coeff)
    
    if(spline_index!=-1):
        x_coeff = coefficients[spline_index]["x_coeffs"]
        y_coeff = coefficients[spline_index]["y_coeffs"]
        th_coeff = coefficients[spline_index]["th_coeffs"]
        t_i = coefficients[spline_index]["t_i"]
        t_f = coefficients[spline_index]["t_f"]
    else:
        return -1;
    
    t= st(t,t_i,t_f)    
    x = x_coeff[0]*(t**3) + x_coeff[1]*(t**2) + x_coeff[2]*(t) + x_coeff[3]
    y = y_coeff[0]*(t**3) + y_coeff[1]*(t**2) + y_coeff[2]*(t) + y_coeff[3]
    th = th_coeff[0]*(t**3) + th_coeff[1]*(t**2) + th_coeff[2]*(t) + th_coeff[3]
    
    return [x,y,th]



        
    
def main():
  #time is passed in nanoseconds 
  time_1 = 110773622239122
  duration_in_sec = 400
  time_2 = time_1 + (10**9) * duration_in_sec; 
  knots = [ {"x":[5,8,0],"v": [1,0,0],"t":time_1} , {"x":[0,0,0], "v": [0,0,0], "t":time_2} ]
  coefficients = get_coefficients(knots)

  # Then a position at time t can be computed as below
  position = get_position(time_1,coefficients)
  print(position)

if __name__ == '__main__':
  main()

