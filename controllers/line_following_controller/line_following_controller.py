from controller import Robot

# Create robot
robot = Robot()

# Simulation time step
timestep = int(robot.getBasicTimeStep())

# Maximum motor speed
MAX_SPEED = 6.28

# Get motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

# Use velocity control
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# Get e-puck distance sensors
ps = []

ps_names = [
    "ps0", "ps1", "ps2", "ps3",
    "ps4", "ps5", "ps6", "ps7"
]

# Enable all distance sensors
for name in ps_names:
    sensor = robot.getDevice(name)
    sensor.enable(timestep)
    ps.append(sensor)

# Obstacle detection threshold
obstacle_threshold = 80.0

# Start robot movement
left_motor.setVelocity(0.5 * MAX_SPEED)
right_motor.setVelocity(0.5 * MAX_SPEED)

# Main control loop
while robot.step(timestep) != -1:

    # Read sensor values
    ps_values = []

    for sensor in ps:
        ps_values.append(sensor.getValue())

    # Left and right obstacle sensors
    left_sensor = ps_values[7]
    right_sensor = ps_values[0]

    # Display obstacle detection status
    if left_sensor > obstacle_threshold or right_sensor > obstacle_threshold:
        print("Obstacle detected")
    else:
        print("Path clear")

    # Obstacle avoidance
    if left_sensor > obstacle_threshold and right_sensor > obstacle_threshold:
        # Obstacle detected on both sides
        left_motor.setVelocity(0.5 * MAX_SPEED)
        right_motor.setVelocity(-0.5 * MAX_SPEED)

    elif left_sensor > obstacle_threshold:
        # Obstacle detected on the left
        left_motor.setVelocity(0.5 * MAX_SPEED)
        right_motor.setVelocity(-0.2 * MAX_SPEED)

    elif right_sensor > obstacle_threshold:
        # Obstacle detected on the right
        left_motor.setVelocity(-0.2 * MAX_SPEED)
        right_motor.setVelocity(0.5 * MAX_SPEED)

    else:
        # No obstacle
        left_motor.setVelocity(0.5 * MAX_SPEED)
        right_motor.setVelocity(0.5 * MAX_SPEED)