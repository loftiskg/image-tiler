from PIL import Image, ImageOps
import math

class TiledImage(object):
    def __init__(self):
        self.tiles=[]
        self.tile_coords = []
    def create(self,image,tileSize):
        '''creates nonoverlapping square tiles of size tileSize from image.
          Inputs:
            image: PIL image that is to be tiled
            tileSize: size of tiles.  Must be less than image
        If tile size is greater than the length of the x or y dimension
        of image throw error.  If the tiles do not crop the enitre image evenly
        pad with zeros until it does such that all tiles are the same size.  Returns
        a TiledImage object.'''
        self.tiles,self.tile_coords=ImageTiler(image,tile_size)
        pass
    def view():
        '''views image'''
        #TODO
        pass
    def save():
        '''saves tiles'''
        #TODO
        pass
    def load():
        '''loads tiles for folder'''
        #TODO
        pass

def ImageTiler(image, tileSize):
    if tileSize > image.width or tileSize > image.height:
        raise ValueError("tileSize is greater than at least one of the image dimensions")
    #calculate number of tiles
    num_x_tiles = computeNumberOfTiles(image.width,tileSize)
    num_y_tiles = computeNumberOfTiles(image.height,tileSize)

    #calculate amount of padding
    pad_x = computePadding(image.width,tileSize)
    pad_y = computePadding(image.height,tileSize)

    # (left,top,right,bottom)
    pad_boarder = (0,0,pad_x,pad_y)

    image = ImageOps.expand(image,pad_boarder,fill=0)

    tiles = []
    tile_coords = []
    for y in range(num_y_tiles):
        tileRow = []
        tile_coordsRow = []
        for x in range(num_x_tiles):
            crop_rect = (x*tileSize,y*tileSize,(x*tileSize+tileSize),(y*tileSize+tileSize))
            tileRow.append(image.crop(crop_rect))
            tile_coordsRow.append(crop_rect)
        tiles.append(tileRow)
        tile_coords.append(tile_coordsRow)

    return tiles,tile_coords


def computeNumberOfTiles(image_size,tile_size):
    if tile_size > image_size:
        raise ValueError("image size must be greater than tile_size")
    return math.ceil(image_size/tile_size)

def computePadding(image_size,tile_size):
    if tile_size > image_size:
        raise ValueError("image size must be greater than tile_size")
    if (image_size % tile_size) == 0:
        return 0
    return tile_size - (image_size % tile_size)



def main():
    img = Image.open("img/img.jpg")
    tiles = ImageTiler(img,80);
    print(len(tiles))
    print(len(tiles[0]))
    tiles[0][11].show()




if __name__ == '__main__':
    main()