#!/usr/bin/env python3

"""
Copyright (c) 2011, Willow Garage, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Willow Garage, Inc. nor the names of its
      contributors may be used to endorse or promote products derived from
      this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import print_function
# from spawn_object import *
import rospy
import yaml
from interactive_markers.interactive_marker_server import *
from interactive_markers.menu_handler import *
from visualization_msgs.msg import *
from geometry_msgs.msg import PoseStamped
# from spawn_object import models_spawned,room_of_model_spawned,places_of_models_spawned

server = None
marker_pos = 0

menu_handler = MenuHandler()

h_first_entry = 0
h_mode_last = 0


def enableCb( feedback ):
    handle = feedback.menu_entry_id
    state = menu_handler.getCheckState( handle )

    if state == MenuHandler.CHECKED:
        menu_handler.setCheckState( handle, MenuHandler.UNCHECKED )
        rospy.loginfo("Hiding first menu entry")
        menu_handler.setVisible( h_first_entry, False )
    else:
        menu_handler.setCheckState( handle, MenuHandler.CHECKED )
        rospy.loginfo("Showing first menu entry")
        menu_handler.setVisible( h_first_entry, True )

    menu_handler.reApply( server )
    rospy.loginfo("update")
    server.applyChanges()

def modeCb(feedback):
    global h_mode_last
    menu_handler.setCheckState( h_mode_last, MenuHandler.UNCHECKED )
    h_mode_last = feedback.menu_entry_id
    menu_handler.setCheckState( h_mode_last, MenuHandler.CHECKED )

    rospy.loginfo("Switching to menu entry #" + str(h_mode_last))
    menu_handler.reApply( server )
    print("DONE")
    server.applyChanges()

def makeBox( msg ):
    marker = Marker()

    marker.type = Marker.CUBE
    marker.scale.x = msg.scale * 0.45
    marker.scale.y = msg.scale * 0.45
    marker.scale.z = msg.scale * 0.45
    marker.color.r = 0.5
    marker.color.g = 0.5
    marker.color.b = 0.5
    marker.color.a = 0.0

    return marker

def makeBoxControl( msg ):
    control = InteractiveMarkerControl()
    control.always_visible = True
    control.markers.append( makeBox(msg) )
    msg.controls.append( control )
    return control

def makeEmptyMarker( dummyBox=True ):
    global marker_pos
    int_marker = InteractiveMarker()
    int_marker.header.frame_id = "base_link"
    int_marker.pose.position.y = -3.0 * marker_pos
    marker_pos += 1
    int_marker.scale = 1
    return int_marker

def makeMenuMarker( name ):
    int_marker = makeEmptyMarker()
    int_marker.name = name

    control = InteractiveMarkerControl()

    control.interaction_mode = InteractiveMarkerControl.BUTTON
    control.always_visible = True

    control.markers.append( makeBox( int_marker ) )
    int_marker.controls.append(control)

    server.insert( int_marker )

def deepCb( feedback ):
    rospy.loginfo("The deep sub-menu has been found.")

def initMenu():
    global h_first_entry, h_mode_last

#ver yaml file e configurar o menu certo
    with open("/home/lclem0/catkin_ws/src/PSR_TP3/Robutler_psr/psr_apartment_description/src/apartment_spots.yaml", 'r') as file:
        pose = yaml.load(file, Loader=yaml.FullLoader)
    
        divisions = []
        for i in range(0, len(pose)):
            division = pose[i]["room"]
            divisions.append(division)
        divisions_list = list(set(divisions))
    h_first_entry = menu_handler.insert( "Go To" )
    entry = menu_handler.insert( "Apartment Divisions", parent=h_first_entry)

    for i in range(0, len(divisions_list)):
        h_mode_last = menu_handler.insert( str(divisions_list[i]), parent=entry, callback=modeCb )
        menu_handler.setCheckState( h_mode_last, MenuHandler.UNCHECKED)
        # check the very last entry
    menu_handler.setCheckState( h_mode_last, MenuHandler.CHECKED )

    #tried to check the last division and print it but it doesnt work 
    # for i in range(0, len(divisions_list)):
    #     h_mode_last = menu_handler.insert(str(divisions_list[i]), parent=entry, callback=modeCb)
    # if menu_handler.getCheckState(h_mode_last) == MenuHandler.CHECKED:
    #     checked_division = divisions_list[i]
    #     print("Checked Division:", str(checked_division))


if __name__=="__main__":
    rospy.init_node("menu")
    # rospy.init_node("move_robot")
    
    server = InteractiveMarkerServer("menu")
    #how to go to each division coordinates from yaml file

    initMenu()
    # sub = rospy.Subscriber("move_base_simple/goal", PoseStamped, callback=modeCb)

    makeMenuMarker( "marker1" )
    # makeMenuMarker( "marker2" )

    menu_handler.apply( server, "marker1" )
    # menu_handler.apply( server, "marker2" )
    server.applyChanges()
    # rospy.loginfo("Going to" + str(h_mode_last))

    rospy.spin()

