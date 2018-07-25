from PIL import Image, ImageOps
import math
import os
import shutil

class TiledImage(object):
    def __init__(self):
        self.tiles=[]
        self.tile_coords = []
        self.image = None
        self.tile_size=0

    @staticmethod
    def createFromImage(image,tileSize):
        '''creates nonoverlapping square tiles of size tileSize from image.
          Inputs:
            image: PIL image that is to be tiled
            tileSize: size of tiles.  Must be less than image
        If tile size is greater than the length of the x or y dimension
        of image throw error.  If the tiles do not crop the enitre image evenly
        pad with zeros until it does such that all tiles are the same size.  Returns
        a TiledImage object.'''

        tiledImage = TiledImage()
        tiledImage.image = image
        tiledImage.tile_size = tileSize;
        tiledImage.tiles, tiledImage.tile_coords = ImageTiler(image,tileSize)
        
        return tiledImage


    def viewStiched(self):
        '''views the stitched image'''
        if self.image:
            self.image.show()
        else:
            raise ValueError("tiled image has not been created")

    def __getitem__(self,key):
        if len(key) == 1:
            return self.tiles[key[0]]
        elif len(key) == 2:
            return self.tiles[key[0]][key[1]]
        else:
            raise IndexError("Too many dimensions")


    def save(self,outdir,prefix="Tile"):
        '''Saves tiles to files.  The tiles are saved in the following format "[prefix]_###_###.png" where
        the first hashes represent the row the tile belongs in and the second hashes represent the column.
        Parameters:
            prefix: prefix that is included before the tile row and column number in image file name
            outdir: the directory to output the images into'''
        try:
            os.makedirs(outdir)
        except FileExistsError:
            pass

        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                tile_name = "Tile_{:03d}_{:03d}.png".format(row,col)
                path = os.path.join(outdir,tile_name)
                self.tiles[row][col].save(path)

    @staticmethod
    def loadFromDirectory(directory,gridSize,tile_name_pattern = "Tile_{:03d}_{:03d}.png",indexStart=0,image_size=(900,900)):
        '''loads tiles from folder'''
        tile_names = generateTileGridNames(gridSize, tile_name_pattern, indexStart=0)
        
        rows, columns = gridSize[0],gridSize[1]

        idx = 0
        tiles = []
        for row in range(rows):
            tile_row = []
            for column in range(columns):
                image_path = os.path.join(directory,tile_names[idx].format(row,column))
                idx+=1
                if os.path.exists:
                    t = Image.open(image_path)
                    tile_row.append(t)
                else:
                    raise FileExistsError("Could not find {}".format(image_path))
            tiles.append(tile_row)
        img = TiledImage()
        img.tiles = tiles
        img.tileSize = tiles[0][0].width, tiles[0][0].height
        img.image = stitchTiles(tiles,image_size)
        img.tile_coords = computeTileCoords(tiles)
        return img

def computeTileCoords(tiles):
    tile_width,tile_height = tiles[0][0].size

    x_pos = 0
    y_pos = 0

    tile_coords = []
    for row in tiles:
        x_pos = 0
        for tile in row:
            tile_coords.append((x_pos,y_pos))
            x_pos += tile_width
        y_pos += tile_height
    return tile_coords

def stitchTiles(tiles,image_size=None):
    num_rows = len(tiles)
    num_col = len(tiles[0])
    tile_height = tiles[0][0].height
    tile_width = tiles[0][0].width

    # if image size is not defined then image_size is imputed 
    # from the size of the tile and number of rows/columns
    if not image_size:
        image_size = (tile_width*num_col, tile_height*num_rows)

    stitched_image = Image.new(tiles[0][0].mode,image_size)

    x_pos = 0
    y_pos = 0
    for row in tiles:
        x_pos = 0
        for tile in row:
            stitched_image.paste(tile,(x_pos,y_pos))
            x_pos += tile_width
        y_pos += tile_height

    return stitched_image

def generateTileGridNames(gridSize,tile_pattern_name="Tile_{:03d}-{:03d}-000_0-000.png",indexStart=0):
    names = [];
    num_rows, num_columns = gridSize[0], gridSize[1]
    for i in range(num_rows):
        for j in range(num_columns):
            names.append(tile_pattern_name.format(i+indexStart,j+indexStart))
    return names


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
    tiledImage = TiledImage.createFromImage(img,512)
    
    #shutil.rmtree('out')
    tiledImage.save('out')
    
    
    loaded = TiledImage.loadFromDirectory('out',(2,2))
    loaded.viewStiched()
    




if __name__ == '__main__':
    main()