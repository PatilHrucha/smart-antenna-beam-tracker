from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    frequency = float(data['frequency'])
    num_elements = int(data['num_elements'])
    steering_angle = float(data['steering_angle'])
    
    # Antenna beam pattern calculation
    theta = np.linspace(-90, 90, 1000)
    theta_rad = np.radians(theta)
    steering_rad = np.radians(steering_angle)
    
    # Array factor calculation
    d = 0.5  # element spacing (wavelengths)
    psi = 2 * np.pi * d * (np.sin(theta_rad) - np.sin(steering_rad))
    
    AF = np.abs(np.sin(num_elements * psi / 2) / 
                (num_elements * np.sin(psi / 2 + 1e-10)))
    
    AF = AF / np.max(AF)  # Normalize
    AF_dB = 20 * np.log10(AF + 1e-10)  # Convert to dB
    
    return jsonify({
        'theta': theta.tolist(),
        'AF': AF_dB.tolist()
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, use_reloader=False)