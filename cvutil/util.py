import cv2

def draw_sprite(frame, sprite, x_offset, y_offset):
    """ Draw sprite over image (dealing with alpha channel as well) """
    (h,w) = (sprite.shape[0], sprite.shape[1])
    (imgH,imgW) = (frame.shape[0], frame.shape[1])

    if y_offset+h >= imgH: #if sprite gets out of image in the bottom
        sprite = sprite[0:imgH-y_offset,:,:]

    if x_offset+w >= imgW: #if sprite gets out of image to the right
        sprite = sprite[:,0:imgW-x_offset,:]

    if x_offset < 0: #if sprite gets out of image to the left
        sprite = sprite[:,abs(x_offset)::,:]
        w = sprite.shape[1]
        x_offset = 0

    #for each RGB chanel
    for c in range(3):
            #chanel 4 is alpha: 255 is not transpartne, 0 is transparent background
            frame[y_offset:y_offset+h, x_offset:x_offset+w, c] =  \
            sprite[:,:,c] * (sprite[:,:,3]/255.0) +  frame[y_offset:y_offset+h, x_offset:x_offset+w, c] * (1.0 - sprite[:,:,3]/255.0)
    
    return frame

def adjust_sprite_size(sprite, head_width, head_ypos):
    """ Adjust sprite size to match face region size """

    (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
    factor = 1.5*head_width/w_sprite
    sprite = cv2.resize(sprite, (0,0), fx=factor, fy=factor)
    (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
    y_orig =  head_ypos-h_sprite

    # Check if the head is not to close to the top of the image and the sprite would not fit in the screen
    if (y_orig < 0):
            sprite = sprite[abs(y_orig)::,:,:]
            y_orig = 0

    return (sprite, y_orig)

def add_sprite(image, sprite, w, x, y):
    """ Add sprite frame to image or frame """
    (sprite, y_final) = adjust_sprite_size(sprite, w, y)
    return draw_sprite(image, sprite, x, y_final + 20)