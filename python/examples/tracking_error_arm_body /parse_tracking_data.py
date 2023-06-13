import pickle
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import bosdyn
import bosdyn.client
import bosdyn.client.util
from bosdyn.util import timestamp_to_sec






class Given_traj:
    def __init__(self):
        self.positions =[]
        self.velocities = []
        self.times = []
class Planned_traj:
    def __init__(self):
        # self.response_time= []
        self.feedback = []
        

class Encoder_traj:
    def __init__(self):
        # self.snap_time = []
        # self.joint_states =[]
        self.robot_state = []
        
        
class Data:
    def __init__(self):
        self.ref_time= None
        self.given_traj = Given_traj()
        self.planned_traj = Planned_traj()
        self.encoder_traj = Encoder_traj()

class Arm_data:
    def __init__(self): 
        self.position = []
        self.velocity = []
        self.acceleration = []
        self.load = []

class Parsed_data:
    def __init__(self):
        self.times = []
        self.sh0 = Arm_data()
        self.sh1 = Arm_data()       
        self.el0 = Arm_data()
        self.el1 = Arm_data()
        self.wr0 = Arm_data()
        self.wr1 = Arm_data()



def query_arm_joint_trajectory(t):
    """
    Given a time t in the trajectory, return the joint angles and velocities.
    This function can be modified to any arbitrary trajectory, as long as it
    can be sampled for any time t in seconds
    """
    # Move our arm joint poses around a nominal pose
    nominal_pose = np.array([0, -0.8, 1.8, 0, -0.9, 0]).reshape(6,1)

    print(t.shape[0])
    # Nominal oscillation period in seconds
    T = 5.0
    w = 2 * math.pi / T

    joint_positions = np.zeros((6,t.shape[0]))
    # Have a few of our joints oscillate
    # joint_positions[0,:] = nominal_pose[0] + 0.8 * np.cos(w * t)
    # joint_positions[1,:] = nominal_pose[1] + 0.4 * np.sin( w * t)
    # joint_positions[2,:] = nominal_pose[2] + 0.2 * np.sin(2 * w * t)
    # joint_positions[3,:] = nominal_pose[3] + 0.3 * np.cos(3 * w * t)
    # joint_positions[4,:] = nominal_pose[4] + 0.5 * np.sin(2 * w * t)
    # joint_positions[5,:] = nominal_pose[5] + 1.0 * np.cos(4 * w * t)

    # # Take the derivative of our position trajectory to get our velocities
    # joint_velocities = np.copy(joint_positions)
    # joint_velocities[0,:] = -0.8 * w * np.sin(w * t)
    # joint_velocities[1,:] = 0.4 * w * np.cos( w * t)
    # joint_velocities[2,:] = 0.2 * 2 * w * np.cos(2 * w * t)
    # joint_velocities[3,:] = -0.3 * 3 * w * np.sin(3 * w * t)
    # joint_velocities[4,:] = 0.5 * 2 * w * np.cos(2 * w * t)
    # joint_velocities[5,:] = -1.0 * 4 * w * np.sin(4 * w * t)

    joint_positions[0,:] = nominal_pose[0] + 0.8* np.cos(w * t)
    joint_positions[1,:] = nominal_pose[1] + 0.5 * np.sin( w * t)
    joint_positions[2,:] = nominal_pose[2] + 0.5 * np.sin(2 * w * t)
    joint_positions[3,:] = nominal_pose[3] + 0.7 * np.cos(3 * w * t)
    joint_positions[4,:] = nominal_pose[4] + 0.7 * np.sin(2 * w * t)
    joint_positions[5,:] = nominal_pose[5] + 0.7 * np.cos(4 * w * t)


    # joint_velocities = [0, 0, 0, 0, 0, 0]
    joint_velocities = np.copy(joint_positions)

    joint_velocities[0,:] = -0.8 * w * np.sin(w * t)
    joint_velocities[1,:] = 0.5 * w * np.cos( w * t)
    joint_velocities[2,:] = 0.5 * 2 * w * np.cos(2 * w * t)
    joint_velocities[3,:] = -.7 * 3 * w * np.sin(3 * w * t)
    joint_velocities[4,:] = .7 * 2 * w * np.cos(2 * w * t)
    joint_velocities[5,:] = -.7 * 4 * w * np.sin(4 * w * t)

    # Return the joint positions and velocities at time t in our trajectory
    return joint_positions, joint_velocities




def fill_joint_data(joint, data):
    joint.position.append(data.position.value)
    joint.velocity.append(data.velocity.value)
    joint.acceleration.append(data.acceleration.value)
    joint.load.append(data.load.value)
    return joint

#start parsing here
# time_skew_sec = 137 + 1e-9*(645598263)
# time_skew_sec = 137 + 1e-9*(354692317)
def parse_data(data):
    time_zero = data.ref_time
    # print(time_zero)
    encoder_data = Parsed_data()
    for i in range(len(data.encoder_traj.robot_state)):
        encoder_data.times.append(timestamp_to_sec(data.encoder_traj.robot_state[i].acquisition_timestamp) - time_zero)
        encoder_data.sh0  = fill_joint_data(encoder_data.sh0 ,data.encoder_traj.robot_state[i].joint_states[12+0])
        encoder_data.sh1  = fill_joint_data(encoder_data.sh1,data.encoder_traj.robot_state[i].joint_states[12+1])
        encoder_data.el0  = fill_joint_data(encoder_data.el0,data.encoder_traj.robot_state[i].joint_states[12+3])
        encoder_data.el1  = fill_joint_data(encoder_data.el1,data.encoder_traj.robot_state[i].joint_states[12+4])
        encoder_data.wr0  = fill_joint_data(encoder_data.wr0,data.encoder_traj.robot_state[i].joint_states[12+5])
        encoder_data.wr1  = fill_joint_data(encoder_data.wr1 , data.encoder_traj.robot_state[i].joint_states[12+6])

    return encoder_data


encoder_data_all_traj = []

for i in range(15):
    PIK = "trackingData_2/tracking_data_2_final_%d.dat"%(i+1)
    data = Data()
    with open(PIK, "rb") as f:
        data =  pickle.load(f)
    encoder_data_all_traj.append(parse_data(data))





    
joints = ['sh0','sh1','el0','el1','wr0','wr1']
fig, axs = plt.subplots(6)

# time = np.linspace(0,20,4000) 

for i in range(6) : 
    for j in range(15):
        joint_pos, joint_velo = query_arm_joint_trajectory(np.array(encoder_data_all_traj[j].times))
        axs[i].plot(np.array(encoder_data_all_traj[j].times)[25:], np.fabs(getattr(encoder_data_all_traj[j], str(joints[i])).position - joint_pos[i,:])[25:], color = 'r')
    axs[i].set_title(joints[i])
    axs[i].set_xlabel('time (sec)')
    axs[i].set_ylabel('Angle (rads/sec)')
    axs[i].set_ylim(0,0.08)
    axs[i].set_yticks([0,0.02,0.04,0.06,0.08])
    # axs[i].legend(fontsize = 9, loc = 4)
# for i in range(6) : 
#     axs[i].plot(np.array(encoder_data.times), getattr(encoder_data, str(joints[i])).position - joint_pos[i,:],  color = 'b', label="Error")
#     axs[i].legend(fontsize = 9, loc = 4)
fig.suptitle(' Error Plot: Position 15 Trajectories', fontsize=17)
plt.show()


# print(data.given_traj.times)


print(data.ref_time)
print(timestamp_to_sec(data.encoder_traj.robot_state[0].acquisition_timestamp))
# print(timestamp_to_sec(data.encoder_traj.robot_state[0].acquisition_timestamp)- timestamp_to_sec(data.ref_time))

# print(data.planned_traj.feedback[0].feedback.synchronized_feedback.arm_command_feedback.arm_joint_move_feedback.planned_points)
# print(data.planned_traj.feedback[3].feedback.synchronized_feedback.arm_command_feedback.arm_joint_move_feedback.planned_points[0])
# # print(data.planned_traj.feedback[8].feedback.synchronized_feedback.arm_command_feedback.arm_joint_move_feedback.planned_points[0])
# print(data.encoder_traj.robot_state[9].joint_states[0])
# print(data.encoder_traj.robot_state[0].joint_states[14].velocity.value)
# print(data.encoder_traj.robot_state[500].joint_states[14].velocity.value)
# print(data.encoder_traj.robot_state[1000].joint_states[14].velocity.value)
# print(data.encoder_traj.robot_state[9].joint_states[0].velocity)
# print(data.encoder_traj.robot_state[9].joint_states[0].acceleration)
# print(data.encoder_traj.robot_state[9].joint_states[0].load)

# print(data.ref_time)
# print(data.encoder_traj.robot_state[0].acquisition_timestamp)
# for i in range(len(data.encoder_traj.robot_state[9].joint_states)):
#     print(data.encoder_traj.robot_state[9].joint_states[i].name)
# # print(data.encoder_traj.robot_state[0].joint_states[0].name)
# print(len(data.given_traj.times)) 
# print(len(data.planned_traj.feedback))


