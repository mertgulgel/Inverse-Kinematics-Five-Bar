import math
posEFx = 3.58
posEFy = 18.94
posXMotor1 = 0.0
posYMotor1 = 0.0
motorDist = 20.0
posXMotor2 = 20.0
posYMotor2 = 0.0
lengthLeftSidedFloatingLink = 13.0
lengthRightSidedFloatingLink = 14.5
lengthLeftSidedDrivingLink = 16.0
lengthRightSidedDrivingLink = 12.0

c1 = math.sqrt((posEFx - posXMotor1)**2 + (posEFy - posYMotor1)**2)
c2 = math.sqrt((posEFx - posXMotor2)**2 + (posEFy - posYMotor2)**2)

alphlengthLeftSidedDrivingLink = math.acos(posEFx / c1)
alphlengthRightSidedDrivingLink = math.acos((-posEFx + motorDist) / (c2) )

betlengthLeftSidedDrivingLink = math.acos((lengthLeftSidedFloatingLink**2 - lengthLeftSidedDrivingLink**2 - c1**2) / (-2*lengthLeftSidedDrivingLink*c1))
betlengthRightSidedDrivingLink = math.acos((lengthRightSidedFloatingLink**2 - lengthRightSidedDrivingLink**2 - c2**2) / (-2*lengthRightSidedDrivingLink*c2))

alpha = alphlengthLeftSidedDrivingLink + betlengthLeftSidedDrivingLink
beta = alphlengthRightSidedDrivingLink + betlengthRightSidedDrivingLink

mu1 = math.atan((posEFy - lengthLeftSidedDrivingLink*math.sin(alpha))/(abs(lengthLeftSidedDrivingLink*math.cos(alpha)) + posEFx))
mu2 = math.atan((posEFy - lengthRightSidedDrivingLink*math.sin(beta))/((20 - posEFx) - (math.cos(beta)*lengthRightSidedDrivingLink)))

print("Left Sided Motor's Angle = %f"%(math.degrees(alpha)))
print("Right Sided Motor's Angle = %f"%(180 - math.degrees(beta)))
