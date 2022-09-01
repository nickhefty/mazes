from unittest import loader
from PIL import Image, ImageDraw
import numpy as np
import cv2
from random import random


def show_maps(arrays, size=6, delay=100, save=False):

    img = Image.new("RGB", (size,size), "white") # create a new image
    pixels = img.load() # create the pixel map

    black_2 = []
    for i in range(img.size[0]):
        if i % 2 == 0:
            black_2.append(i)

    black_1 = [i-1 for i in black_2 if i > 0]
    if img.size[0] % 2 == 0:
        black_1.append(img.size[0]-1)


    for i in black_1:
        for j in range(0, size, 2):
            pixels[i,j] = (0,0,0)

    for k in black_2:
        for l in range(1, size+1, 2):
            pixels[k,l] = (0,0,0)
    
    bg = img.resize((size*100, size*100), Image.BOX)

        
    def adjacent(p1, p2):
        if abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) == 1: 
            return True


    locations = [i+50 for i in range(0, size*100, 100)]
    arr = [[(x, y) for x in locations] for y in locations]
    arr = np.array(arr)
    for map in arrays:
        bg1 = bg.copy()
        
        line_layer = ImageDraw.Draw(bg1)
        #last_point = (arr[path[0]][0], arr[path[0]][1])

        path = np.where(map == 1)
        all_points = [i for i in zip(path[0], path[1])]

        #put the points in order
        ordered_points = [all_points.pop(0)]
        while all_points:
            for i, _ in enumerate(all_points):
                if adjacent(ordered_points[-1], all_points[i]):
                    ordered_points.append(all_points.pop(i))
        

        last_point = arr[ordered_points[0]][0], arr[ordered_points[0]][1] - 50
        for p in ordered_points[1:]:
            
            next_point = arr[p][0], arr[p][1]
            shape = [last_point, next_point]
            line_layer.line(shape, fill='green', width=30)
            line_layer.ellipse(((next_point[0]-14, next_point[1]-14), (next_point[0]+14, next_point[1]+14)), fill='green')
            last_point = next_point[0], next_point[1]
        next_point = arr[ordered_points[-1]][0], arr[ordered_points[-1]][1] + 50
        shape = [last_point, next_point]
        line_layer.line(shape, fill='green', width=30)

        #add a 30 px border
        w, h = bg1.size
        bg2 = Image.new('RGB', (w+60, h+60), color='gray')
        bg2.paste(bg1, (30, 30))

        #round the ends of the line
        line_layer = ImageDraw.Draw(bg2)
        line_layer.ellipse(((next_point[0]+17, next_point[1]+17), (next_point[0]+44, next_point[1]+44)), fill='green')
        next_point = arr[ordered_points[0]][0], arr[ordered_points[0]][1] - 50
        line_layer.ellipse(((next_point[0]+17, next_point[1]+17), (next_point[0]+44, next_point[1]+44)), fill='green')

        # save ouput images
        if save == True: bg2.save(r'output/render_maze'+str(random())+'.png')
        
        #display the image for the set number of miliseconds
        board = bg2.convert('RGB')
        open_cv_image = np.array(board)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        cv2.imshow("Generated Maps", open_cv_image)

        cv2.waitKey(delay)
    

    cv2.destroyAllWindows() 
