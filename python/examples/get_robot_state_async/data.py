import pickle
PIK = "data.dat"

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

data = Data()
with open(PIK, "rb") as f:
    data =  pickle.load(f)

print(data.encoder_traj.robot_state)
