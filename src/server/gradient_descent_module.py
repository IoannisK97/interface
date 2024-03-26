import random
import math
import numpy as np
import matplotlib.pyplot as plt

from polynomial_functions import calculate_derivative


def gradient_descent(function, L=None, learning_rate_type="regular" , learning_rate=None, epsilon=0.001,max_iter=10000,starting_x=None,range_values=(-10,10)):
    
    derivative=calculate_derivative(function)
    
    x_values=np.arange(range_values[0],range_values[1],0.01)
    y_values=function(x_values)
    if (starting_x==None):
        starting_x=random.uniform(range_values[0], range_values[1])
        
    starting_point=(starting_x,function(starting_x))
    point=starting_point
    points = [starting_point] 
    
    if learning_rate_type=="regular":
        if learning_rate==None:
            learning_rate=0.01
    if (learning_rate_type=="lipshcitz" and L!= None):
        h=1/L
    
    if (learning_rate_type=="adaptive"):
        if learning_rate==None:
            learning_rate=0.5

    if (learning_rate_type=="armijo"):
        if learning_rate==None:
            learning_rate=0.01
        
    h=learning_rate

    print(type(max_iter))
    for i in range(max_iter):
        if (learning_rate_type=="armijo"):
                alpha = 0.1 
                beta = 0.5
                h=armijo_rule(point,function,derivative,alpha,beta,)
                
        if (learning_rate_type=="adaptive"):
            h=learning_rate/(math.sqrt(i+1))
            
        new_x=point[0]-h*derivative(point[0])
        new_y=function(new_x)
        point=(new_x,new_y)
        points.append(point)
        if (abs(derivative(new_x))<epsilon):
            break

        if (new_x <range_values[0] or new_x>range_values[1]):
            print(range_values)
            print("Outside range")
            print(new_x)
            break

    #print("The optima is", point)
    print("it needed "+ str(i) +" iterations for epsilon being "+ str(epsilon) )
    #print()
    return i+1, starting_x,points,x_values,y_values


def armijo_rule(point,function, gradient, alpha, beta,initial_h=0.1, max_iter=10):
    h = initial_h
    for _ in range(max_iter):
        new_x = point[0] - h * gradient(point[0])
        
        #Condition 1.2.16
        condition1 = function(point[0]) - function(new_x) >= alpha * h * np.dot(gradient(point[0]), (point[0] - new_x))
        
        #Condition 1.2.17
        condition2 = np.dot(gradient(point[0]), (point[0] - new_x)) >= beta * np.dot(gradient(point[0]), (point[0] - new_x))
        
        if condition1 and condition2:
            return h
        else:
            h *= beta
    return h