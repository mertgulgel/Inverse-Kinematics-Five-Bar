import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox

# Default Position Values of End-Efector
posEFx = 7.5
posEFy = 20

# Constraints
posXMotor1 = 0.0
posYMotor1 = 0.0
motorDist = 15.0
posXMotor2 = 15.0
posYMotor2 = 0.0
lengthfloatinglinks = 15.0
lengthdrivinglinks = 15.0


# Setting the Figure
fig = plt.figure()
ax = fig.subplots()
plt.subplots_adjust(bottom=0.3)
plt.subplots_adjust(left=0.3)
plt.title('5-Bar Linkage')

# Slider ve TextBoxların koordinatlarının tanımlanması
drivingaxbox = plt.axes([0.25, 0.08, 0.65, 0.04])
floatingaxbox = plt.axes([0.25, 0.15, 0.65, 0.04])
motordistaxbox = plt.axes([0.25, 0.01, 0.65, 0.04])
yx_slider = plt.axes([0.1, 0.3, 0.04, 0.65])

# Slider ve TextBoxları ayarlanması
yVar = Slider(yx_slider, 'Y-Value', valmin=0, valmax=110, valinit=posEFy, valstep=1, orientation="vertical")
drivinglinks_text_box = TextBox(drivingaxbox, "Driving", textalignment='center')
floatinglinks_text_box = TextBox(floatingaxbox, "Floating", textalignment='center')
motordist_text_box = TextBox(motordistaxbox, "Ground", textalignment='center')

# Calculating Motors' Angles and Driving-Floating Link Angles
def calc_Angles(posEFx, posEFy):
    global lengthdrivinglinks
    global motorDist
    global lengthfloatinglinks 
    c1 = math.sqrt((posEFx - posXMotor1)**2 + (posEFy - posYMotor1)**2)
    c2 = math.sqrt((posEFx - posXMotor2)**2 + (posEFy - posYMotor2)**2)
    
    alpha1 = math.acos(posEFx / c1)
    alpha2 = math.acos((-posEFx + motorDist) / (c2) )
    
    beta1 = math.acos((lengthfloatinglinks**2 - lengthdrivinglinks**2 - c1**2) / (-2*lengthdrivinglinks*c1))
    beta2 = math.acos((lengthfloatinglinks**2 - lengthdrivinglinks**2 - c2**2) / (-2*lengthdrivinglinks*c2))
    
    alpha = alpha1 + beta1
    beta = alpha2 + beta2
    
    mu1 = math.atan((posEFy - lengthdrivinglinks*math.sin(alpha))/(abs(lengthdrivinglinks*math.cos(alpha)) + posEFx))
    mu2 = math.atan((posEFy - lengthdrivinglinks*math.sin(beta))/((20 - posEFx) - (math.cos(beta)*lengthdrivinglinks)))
    return(alpha, beta, mu1, mu2)

# Plotting Motor Driving Links and Floating Links
def plotting_arms(alpha, beta, posEFx, posEFy, muu1, muu2):
    global lengthdrivinglinks
    global lengthfloatinglinks
    global motorDist 
    # Calculating the length of Left Sided Driving Link
    p1 = (lengthdrivinglinks*math.cos(alpha), lengthdrivinglinks*math.sin(alpha))
    
    # Calculating the length of Right Sided Driving Link
    p2 = (motorDist + lengthdrivinglinks*math.cos(math.pi - beta), lengthdrivinglinks*math.sin(math.pi - beta))
    
    # Calculating the length of Left Sided Floating Link
    p3 = (lengthfloatinglinks*math.cos(muu1), lengthfloatinglinks*math.sin(muu1))
    
    # Calculating the length of Right Sided Floating Link
    p4 = (lengthfloatinglinks*math.cos(math.pi- muu2), lengthfloatinglinks*math.sin(muu2))

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
    ax.plot([p2[0], p2[0]+p4[0]], [p2[1], p2[1]+p4[1]], 'co-')
    
    # Driving Linklerin Groundlarına olan uzaklığı
    ax.text(lengthdrivinglinks*math.cos(alpha), lengthdrivinglinks*math.sin(alpha), lengthdrivinglinks*math.cos(alpha))
    ax.text(motorDist + lengthdrivinglinks*math.cos(math.pi - beta) , lengthdrivinglinks*math.sin(math.pi - beta), lengthdrivinglinks*math.cos(math.pi - beta))
    
    # Hesaplanan mafsal noktalarının konumları
    ax.plot(posEFx, posEFy, 'ro')
    ax.plot(p1[0],p1[1], 'go')
    ax.plot(p2[0],p2[1], 'go')

# The Plotting Function   
def plotting(posEFx, posEFy):
    s1, s2, muu1, muu2 = calc_Angles(posEFx, posEFy)
    plotting_arms(s1, s2, posEFx, posEFy, muu1, muu2)
    plt.show()
 
# Figure Updating Function to changes on the Slider   
def update(val):
    global current_vy
    current_vy = yVar.val
    plotting(posEFx , current_vy)

# TextBoxlardan grafiği updatelemek için kullanılan fonksiyonlar
def submit_drivinglinks(expression):
    global lengthdrivinglinks
    lengthdrivinglinks = int(expression)
    plotting(posEFx, current_vy)

def submit_floatinglinks(expression):
    global lengthfloatinglinks
    lengthfloatinglinks = int(expression)
    plotting(posEFx, current_vy)

def submit_groundlink(expression):
    global motorDist, posXMotor2, posEFx
    posEFx = int(expression)/2
    motorDist = int(expression)
    posXMotor2 = int(expression)
    plotting(posEFx, current_vy)

yVar.on_changed(update)
drivinglinks_text_box.on_submit(submit_drivinglinks)
floatinglinks_text_box.on_submit(submit_floatinglinks)
motordist_text_box.on_submit(submit_groundlink)

plotting(posEFx,posEFy)