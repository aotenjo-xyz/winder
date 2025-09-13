# Create text objects to display the slot numbers in a circular pattern in Blender
# This way you can see the stator positions and which slot the machine is currently winding at.
import bpy
import math


# Remove existing text objects first (optional cleanup)
for obj in bpy.data.objects:
    if obj.type == "FONT":
        bpy.data.objects.remove(obj, do_unlink=True)

# Parameters
radius = 36 / 2  # diameter → radius
z_height = 18
count = 24
text_size = 4.0

for i in range(count):
    angle = (2 * math.pi / count) * i  # angle in radians
    # x = radius * math.cos(angle)
    x = -radius * math.cos(angle)  # Invert X to reverse direction
    y = radius * math.sin(angle)

    # Create text object
    bpy.ops.object.text_add(location=(x, y, z_height))
    text_obj = bpy.context.object
    text_obj.data.body = str(i)

    # Set text size and center the text geometry
    text_obj.data.size = text_size
    text_obj.data.align_x = "CENTER"
    text_obj.data.align_y = "CENTER"

    # Rotate so text faces outward
    text_obj.rotation_euler[0] = math.radians(90)  # stand upright
    # text_obj.rotation_euler[2] = angle + math.pi/2  # face outward
    text_obj.rotation_euler[2] = -(
        angle + math.pi / 2
    )  # face outward and reverse direction
