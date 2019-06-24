import Utils
import rospy

rospy.init_node("flight")

ir = Utils.IR()

desription = {
    "6897":"Noose through Ring", 
    "9867":"Noose through Gate", 
    "b04f":"Fly to start point with purple led and landing", 
    "30cf":"Fly to start point with blue led and landing", 
    "18e7":"Fly to payload zone with yellow led and landing"
}
ir_cmds = ["6897", "9867", "b04f", "30cf", "18e7"]

ccc = ir.waitData(ir_cmds)
print(desription[ccc])
rospy.sleep(0.2)