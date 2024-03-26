from flask import Flask, request, jsonify, send_file
from gradient_descent_module import gradient_descent  
from polynomial_functions import format_polynomial, create_polynomial_function_from_string, calculate_derivative  # Import your polynomial-related functions
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/gradient-descent', methods=['POST'])
def perform_gradient_descent_with_visualization():
    data = request.get_json()
    print("we are here")

    function_text = data.get('functionString', '')
    
    
    polynomial_function = create_polynomial_function_from_string(function_text)

    
    range_input = data.get('rangeInput', [])
    range_values= tuple(map(float, range_input))
    learning_rate_type = data.get('learningRateType', 'regular')
    learning_rate = float(data.get('learningRate', 0.001))
    epsilon = float(data.get('epsilon', 0.001))
    max_iter = int(data.get('maxIter', 10000))

    print(f"Received request with function: {function_text}")
    print(f"Learning Rate Type: {learning_rate_type}")
    print(f"Learning Rate: {learning_rate}")
    print(f"Epsilon: {epsilon}")
    print(f"Max Iterations: {max_iter}")
    
    
    
     
    no_iterations,starting_x,points_gradient,x_values,y_values  = gradient_descent(polynomial_function,  learning_rate_type=learning_rate_type,
                                 learning_rate=learning_rate, epsilon=epsilon, max_iter=max_iter, range_values=range_values)

    
    result = {
        'noIterations': no_iterations,
        'pointsGradient': points_gradient,
        'xValues': x_values.tolist(),
        'yValues': y_values.tolist(),
        
    }

    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
