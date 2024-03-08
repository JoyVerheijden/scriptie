from PIL import Image, ImageDraw, ImageFont
import json
import os

# # Draw bboxes and corresponding numbers given a list of bboxes
# def draw_bboxes(bboxes, text, blue, output_path):

#     # Find the maximum x2 and y2 values
#     max_x2 = max_y2 = 0


#     for i in range(len(bboxes)):
        

#         bboxes[i] = [coord for coord in bboxes[i]]
#         max_x2 = int(max(max_x2, bboxes[i][2]))
#         max_y2 = int(max(max_y2, bboxes[i][3]))

#     # Create a new image with the maximum size
#     image = Image.new('RGB', (max_x2 + 10, max_y2 + 10), (255, 255, 255))
#     draw = ImageDraw.Draw(image)

#     # Set the font size
#     font_size=12

#     # Draw BLEU score
#     #draw.text((max_x2 - 150, 20), "BLEU: "+str(blue), fill="blue", font=ImageFont.truetype('FreeSans.ttf', 20))

#     for i, (x1, y1, x2, y2) in enumerate(bboxes):
#         draw.rectangle([x1, y1, x2, y2], outline="red")
#         draw.text((x1, y1), str(text[i]), fill="black", font=ImageFont.truetype('FreeSans.ttf', font_size))

#     # Save the image
#     image.save(output_path)




# # draw bboxes and corresponding numbers given a dict 
# def draw_bboxes(bbox_to_index, output_path):
#     max_x2 = max(box[2] for box in bbox_to_index.keys())
#     max_y2 = max(box[3] for box in bbox_to_index.keys())

#     # Set image dimensions slightly larger than the max x2, y2 values
#     image_width = max_x2 + 10
#     image_height = max_y2 + 10

#     # Create an image with the calculated dimensions
#     img = Image.new('RGB', (image_width, image_height), color='white')

#     # Initialize the drawing context
#     draw = ImageDraw.Draw(img)

#     # Use PIL's default font
#     font = ImageFont.truetype('FreeSans.ttf', 12)

#     for box, number in bbox_to_index.items():
#         # Draw the rectangle
#         draw.rectangle(box, outline='black')
        
#         # Calculate text size to position it approximately in the center of the box
#         #text_size = draw.textsize(str(number), font=font)
#         text_x = box[0] + 2
#         text_y = box[1] + 2
        
#         # Draw the number inside the rectangle
#         draw.text((text_x, text_y), str(number), fill="black", font=font)

#     # Save or display the image
#     img.save(output_path)

# draw bboxes and corresponding numbers given a dict 
def draw_bboxes(bbox_to_index, output_path):
    max_x2 = max(box[2] for box in bbox_to_index.keys())
    max_y2 = max(box[3] for box in bbox_to_index.keys())

    # Set image dimensions slightly larger than the max x2, y2 values
    image_width = max_x2 + 10
    image_height = max_y2 + 10

    # Create an image with the calculated dimensions
    img = Image.new('RGB', (image_width, image_height), color='white')

    # Initialize the drawing context
    draw = ImageDraw.Draw(img)

    # Use PIL's default font
    font = ImageFont.truetype('FreeSans.ttf', 12)

    maxnumber = max(bbox_to_index.values())
    for box, number in bbox_to_index.items():

        # get gradient color
        gradient_perc = number / maxnumber
        color = (100-int(gradient_perc * 100), 100-int(gradient_perc * 100), 255-int(gradient_perc * 200))

        # Draw the rectangle (filled with color)
        draw.rectangle(box, fill=color)
        
        # Calculate text size to position it approximately in the center of the box
        #text_size = draw.textsize(str(number), font=font)
        text_x = box[0] + 2
        text_y = box[1] + 2
        
        textcolor = "white"

        # Draw the number inside the rectangle
        draw.text((text_x, text_y), str(number), fill=textcolor, font=font)

    # Save or display the image
    img.save(output_path)


def draw_preprocessed_bboxes():

    # number of json files to draw
    for i in range(1):

        print('Drawing json file: ', i+1)
        # open and read layout file
        with open('ReadingBank/temp_json/dataset-test-s2s-layout-m'+str(i+1)+'.json', 'r') as json_file:
            data = json.load(json_file)
            bboxes = data.get('src', [])

        # open and read text file
        with open('ReadingBank/temp_json/dataset-test-s2s-text-m'+str(i+1)+'.json', 'r') as json_file:
            data = json.load(json_file)
            text = data.get('src', [])

            bleu = 1
            #bleu = round(data.get('blue', []),3)

        text = text.split()
        draw_bboxes(bboxes, text, bleu, output_path='temp_output_drawbboxes/temp_json'+str(i+1)+'.png')


def draw_preprocessed_bboxes2():

    # number of json files to draw
    #for i in range(len(os.listdir('results_ids_cvs'))):
    
    
    for i in range(50):

        print('Drawing json file: ', i+1)
        # open and read layout file
        with open('resume_english_lr_output/'+str(i+1)+'.json', 'r') as json_file:
            data = json.load(json_file)
            bboxes = data.get('output_bboxes', [])
            text = data.get('output_sequence', [])

        
        text = text.split()

        # print("text", text)
        # print("bboxes", bboxes)


        bbox_to_index = {}
        for j, bbox in enumerate(bboxes):
            if not tuple(bbox) in bbox_to_index or j < bbox_to_index[tuple(bbox)]:
                bbox_to_index[tuple(bbox)] = j

        #print('bbox_to_index: ', bbox_to_index)
        #print('len(bbox_to_index): ', len(bbox_to_index))

        # bboxes, text = zip(*sorted(zip(bboxes, text), key=lambda x: bbox_to_index[tuple(x[0])]))

        # print('len(bboxes): ', len(bboxes))
        # print('len(text): ', len(text))

        #draw_bboxes(bboxes, text, bleu, output_path='temp_output_drawbboxes/temp_json'+str(i+1)+'.png')


        draw_bboxes(bbox_to_index, output_path='temp_output_drawbboxes/'+str(i+1)+'.png')





draw_preprocessed_bboxes2()



