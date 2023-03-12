import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Default Position Values of End-Efector
posEFx = 3.58
posEFy = 18.94

# Constraints
posXMotor1 = 0.0
posYMotor1 = 0.0
motorDist = 20.0
posXMotor2 = 20.0
posYMotor2 = 0.0
lengthLeftSidedFloatingLink = 13.0
lengthRightSidedFloatingLink = 14.5
lengthLeftSidedDrivingLink = 16.0
lengthRightSidedDrivingLink = 12.0

# Setting the Figure
fig = plt.figure()
ax = fig.subplots()
plt.subplots_adjust(bottom=0.25)
plt.subplots_adjust(left=0.25)
plt.title('5-Bar Linkage')

# Positioning the Sliders
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.04])
yx_slider = plt.axes([0.1, 0.25, 0.04, 0.65])

# Adding Sliders to Given Position
xVar = Slider(ax_slider, 'X-Value', valmin=-10, valmax=25, valinit=posEFx, valstep=1)
yVar = Slider(yx_slider, 'Y-Value', valmin=-5, valmax=21, valinit=posEFy, valstep=1, orientation="vertical")

# Calculating Motors' Angles and Driving-Floating Link Angles
def calc_Angles(posEFx, posEFy):  
    c1 = math.sqrt((posEFx - posXMotor1)**2 + (posEFy - posYMotor1)**2)
    c2 = math.sqrt((posEFx - posXMotor2)**2 + (posEFy - posYMotor2)**2)
    
    alpha1 = math.acos(posEFx / c1)
    alpha2 = math.acos((-posEFx + motorDist) / (c2) )
    
    beta1 = math.acos((lengthLeftSidedFloatingLink**2 - lengthLeftSidedDrivingLink**2 - c1**2) / (-2*lengthLeftSidedDrivingLink*c1))
    beta2 = math.acos((lengthRightSidedFloatingLink**2 - lengthRightSidedDrivingLink**2 - c2**2) / (-2*lengthRightSidedDrivingLink*c2))
    
    alpha = alpha1 + beta1
    beta = alpha2 + beta2
    
    mu1 = math.atan((posEFy - lengthLeftSidedDrivingLink*math.sin(alpha))/(abs(lengthLeftSidedDrivingLink*math.cos(alpha)) + posEFx))
    mu2 = math.atan((posEFy - lengthRightSidedDrivingLink*math.sin(beta))/((20 - posEFx) - (math.cos(beta)*lengthRightSidedDrivingLink)))
    
    return(alpha, beta, mu1, mu2)

# Plotting Motor Driving Links and Floating Links
def plotting_arms(alpha, beta, posEFx, posEFy, muu1, muu2):
    # Calculating the length of Left Sided Driving Link
    p1 = (lengthLeftSidedDrivingLink*math.cos(alpha), lengthLeftSidedDrivingLink*math.sin(alpha))
    
    # Calculating the length of Right Sided Driving Link
    p2 = (motorDist + lengthRightSidedDrivingLink*math.cos(math.pi - beta), lengthRightSidedDrivingLink*math.sin(math.pi - beta))
    
    # Calculating the length of Left Sided Floating Link
    p3 = (lengthLeftSidedFloatingLink*math.cos(muu1), lengthLeftSidedFloatingLink*math.sin(muu1))
    
    # Calculating the length of Right Sided Floating Link
    p4 = (lengthRightSidedFloatingLink*math.cos(math.pi- muu2), lengthRightSidedFloatingLink*math.sin(muu2))
    
    # Clearing the figure after change
    ax.cla()
    
    # Plotting the Left Sided Driving Link and it's angle
    ax.plot([0, p1[0]], [0, p1[1]], 'ko-')
    ax.text(0+0.3,0+0.3,"%f"%(math.degrees(alpha)))
    
    # Plotting the Right Sided Driving Link and it's angle
    ax.plot([motorDist, p2[0]], [0, p2[1]], 'ko-')
    ax.text(motorDist+0.3,0+0.3,"%f"%(180 - math.degrees(beta)))
    
    # Plotting the Left Sided Floating Link
    ax.plot([p1[0], p1[0]+p3[0]], [p1[1], p1[1]+p3[1]], 'co-')
    
    # Plotting the Right Sided Floating Link
    ax.plot([p2[0], p2[0]+p4[0]], [p2[1], p2[1]+p4[1]], 'go-')
    
    # Showing if the structural error occurs
    if (abs(posEFy - (p3[1]+p1[1])) > 0.01):
        ax.text(posEFx,posEFy,"Structural Error")
    if (abs(posEFy - (p4[1]+p2[1])) > 0.01):
        ax.text(posEFx,posEFy,"Structural Error")
    if (abs(posEFx - (p3[0]+p1[0])) > 0.01):
        ax.text(posEFx,posEFy,"Structural Error")
    if (abs(posEFx - (p4[0]+p2[0])) > 0.01):
        ax.text(posEFx,posEFy,"Structural Error")
    
    # Plotting the desired coordinates
    ax.plot(posEFx, posEFy, 'ro')
    ax.plot(p1[0],p1[1], 'yo')
    ax.plot(p2[0],p2[1], 'co')

# The Plotting Function   
def plotting(posEFx, posEFy):
    s1, s2, muu1, muu2 = calc_Angles(posEFx, posEFy)
    plotting_arms(s1, s2, posEFx, posEFy, muu1, muu2)
    plt.show()
 
# Figure Updating Function to changes on the Sliders   
def update(val):
    current_vx = xVar.val
    current_vy = yVar.val
    plotting(current_vx, current_vy)
    
xVar.on_changed(update)
yVar.on_changed(update)

plotting(posEFx,posEFy)
