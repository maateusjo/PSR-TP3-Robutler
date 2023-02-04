#!/usr/bin/env python3

import random

import rospy
import rospkg
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose, Point, Quaternion

rospy.init_node('insert_object',log_level=rospy.INFO)

# get an instance of RosPack with the default search paths
rospack = rospkg.RosPack()
package_path = rospack.get_path('psr_apartment_description') + '/description/models/'

num_objects=input('How many objects do you want to spawn? Select a number between 1 and 7: ')
if int(num_objects) > 7:
  rospy.logerr('Too many objects. Please select a number between 1 and 7')
  exit()
  
#Add here mode poses
placements = []
placements.append({'pose':Pose(position=Point(x=-5.69, y=4.37, z=0.6), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'large_bedroom', 'place': 'bed'})
placements.append({'pose':Pose(position=Point(x=-7.33, y=5.29, z=0.58), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'large_bedroom', 'place': 'bedside_cabinet'})
            #   adicionar mais sitios
placements.append({'pose':Pose(position=Point(x=-1.7, y=4.0, z=0.37), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'second_bedroom', 'place': 'fridge_cabinet'})
placements.append({'pose':Pose(position=Point(x=-2, y=-5, z=0.4), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'living_room', 'place': 'sofa'})
placements.append({'pose':Pose(position=Point(x=1, y=-3, z=0), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'outside', 'place': 'car_spot'})
placements.append({'pose':Pose(position=Point(x=-6, y=-2, z=0.765), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'living_room', 'place': 'cafe_table'})
placements.append({'pose':Pose(position=Point(x=1.74, y=-0.7, z=0.5), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'bathroom', 'place': 'toilet'})
placements.append({'pose':Pose(position=Point(x=-2.5, y=5, z=0), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'second_bedroom', 'place': 'ground'})
placements.append({'pose':Pose(position=Point(x=0, y=5, z=0), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'office', 'place': 'ground'})
placements.append({'pose':Pose(position=Point(x=0.5, y=1.5, z=0), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'first_bathroom', 'place': 'ground'})
placements.append({'pose':Pose(position=Point(x=-3, y=1.5, z=0), orientation=Quaternion(x=0,y=0,z=1,w=1)),
'room':'corridor', 'place': 'ground'})
placements.append({'pose':Pose(position=Point(x=-7.5, y=-0.5, z=0), orientation=Quaternion(x=0,y=0,z=0,w=1)),
'room':'ouside_corridor', 'place': 'ground'})
placements.append({'pose':Pose(position=Point(x=-1.7, y=-0.5, z=0.8), orientation=Quaternion(x=0,y=0,z=0,w=1)),
'room':'kitchen', 'place': 'counter'})
placements.append({'pose':Pose(position=Point(x=-4.5, y=-2, z=0), orientation=Quaternion(x=0,y=0,z=1,w=1)),
'room':'living_room', 'place': 'ground'})
placements.append({'pose':Pose(position=Point(x=-1, y=-5, z=0), orientation=Quaternion(x=0,y=0,z=0,w=1)),
'room':'living_room', 'place': 'corner'})
              

# cant do shrek
model_names = ['sphere_v','stop_sign','person_standing','beer','bowl','person_walking','fire_hydrant']

# Add here several models. All should be added to the robutler_description package
for i in range(0, int(num_objects)):
  model_name = random.choice(model_names)
  # model_name = model_names[-1]
  
  f = open( package_path + model_name + '/model.sdf' ,'r')
  sdff = f.read()

  rospy.wait_for_service('gazebo/spawn_sdf_model')
  spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
  
  model_placement = random.choice(placements)
  placements.remove(model_placement)
  # model_placement = placements[14]

  name = model_name + '_in_' + model_placement['place'] + '_of_' + model_placement['room']
  spawn_model_prox(name, sdff, model_name, model_placement['pose'], "world")
  rospy.loginfo(name)
  i+=1