import pygame
import quaternion
import numpy as np

# pygame setup
pygame.init()
YMAX = 180
XMAX = 360
screen = pygame.display.set_mode((2*XMAX, 2*YMAX))
clock = pygame.time.Clock()
running = True
dt = 0

#init pointpos, a list of spheres to draw using the draw.circle from pygame       x, y, z // right, deep, up
pointpos = [pygame.Vector3(0,10,0),pygame.Vector3(5,10,0) ]
ballrad = 3

#init wireframe a list of lists holding the positions by which a wireframe will pass using the draw.line from pygame
#this ones for a cube
wireframe = [[[10, 10, 0], [15, 10, 0],[10, 10, 5], [10, 15, 0],[10, 10, 0], [10, 10, 5],[15, 10, 5], [15, 15, 0],[15, 15, 0], [15, 15, 5],[15, 10, 5], [15, 10, 0],[15, 15, 0], [10, 15, 5],[15, 15, 5],[10, 10, 5],[10, 15, 5],[10, 15, 0],[15, 15, 0],[10, 10, 0]]]

class camera:

    def __init__(self):
        self.focal_length = 360
        self.scaling_factor = 2
        self.focuspos = pygame.Vector3(0.0,0.0,0.0)
        self.orientation = np.quaternion(1, 0, 0, 0)
        self.rotation_matrix = np.identity(3)
        self.update_matrix
        

    def update_matrix(self):
        self.rotation_matrix = quaternion.as_rotation_matrix(self.orientation)


    def move(self, velocity:list):
        # velocity: [right, forwards, up]
        self.focuspos += self.rotation_matrix[0] * velocity[0] * dt  # right
        self.focuspos += self.rotation_matrix[2] * velocity[2] * dt  # up
        self.focuspos += self.rotation_matrix[1] * velocity[1] * dt  # forward


    def rotate_matrix(self, axis: np.ndarray, angle: float):
        q_delta = quaternion.from_rotation_vector(axis * angle)
        self.orientation = q_delta * self.orientation
        self.update_matrix()


    def updatepos(self):
        turnspeed = 1
        movespeed = 5
        keys = pygame.key.get_pressed()
        if keys[pygame.K_l]:
            self.rotate_matrix(np.array([0, 0, 1]), turnspeed * dt)
        if keys[pygame.K_j]:
            self.rotate_matrix(np.array([0, 0, 1]), -turnspeed * dt)
        if keys[pygame.K_u]:
            self.rotate_matrix(np.array([0, 1, 0]), turnspeed * dt)
        if keys[pygame.K_o]:
            self.rotate_matrix(np.array([0, 1, 0]), -turnspeed * dt)
        if keys[pygame.K_i]:
            self.rotate_matrix(np.array([1, 0, 0]), -turnspeed * dt)
        if keys[pygame.K_k]:
            self.rotate_matrix(np.array([1, 0, 0]), turnspeed * dt)
        if keys[pygame.K_a]:
            self.move([0, 0, movespeed])
        if keys[pygame.K_e]:
            self.move([0, 0,-movespeed])
        if keys[pygame.K_d]:
            self.move([ movespeed, 0, 0])
        if keys[pygame.K_q]:
            self.move([-movespeed, 0, 0])
        if keys[pygame.K_s]:
            self.move([0, -movespeed, 0])
        if keys[pygame.K_z]:
            self.move([0, movespeed, 0])



    def project(self, point:pygame.Vector3):

        #assigning relative coords
        x, y, z, radius = point[0], point[1], point[2], ballrad
        x, y, z = x - self.focuspos[0], y - self.focuspos[1], z - self.focuspos[2]

        xyzmat = np.array([[x], [y], [z]])
        rotated = self.rotation_matrix @ xyzmat
        x, y, z = rotated.flatten()

        screenx = (x * self.focal_length) / y
        screeny = (z * self.focal_length) / y

        if y > 0:
            radius = self.focal_length / y * radius
        else:
            radius = 0  # or skip drawing

        x = screenx
        y = screeny
        
        #fixing the coords for pygame
        x, y = x * self.scaling_factor, y * self.scaling_factor
        x += XMAX
        y = -y + YMAX
        
        return [x, y, radius]


#cam params
camera1 = camera()


while running:

    #check if ya clicked on x or alt f4'd
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    camera1.updatepos()

    screen.fill("black")

    #renders balls
    for i in range(len(pointpos)):
        camera1.project(pointpos[i])
        pygame.draw.circle(screen, "white", pygame.Vector2(camera1.project(pointpos[i])[0],camera1.project(pointpos[i])[1]), camera1.project(pointpos[i])[2])

    #renders wireframes
    for i in wireframe:
        for j in range(len(i)-1):
            pygame.draw.line(screen, "red", camera1.project(i[j])[:2], camera1.project(i[j+1])[:2], 2)

    #renders polygons   TODO

    pygame.display.flip()

    dt = clock.tick(60) / 1000



pygame.quit()
