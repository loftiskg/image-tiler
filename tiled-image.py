from PIL import Image

class TiledImage(object):
    def __init__(self):
        self.tiles=[]
    def create(self,image,tileSize):
        '''creates nonoverlapping square tiles of size tileSize from image.
          Inputs:
            image: input image that is to be tiled
            tileSize: size of tiles.  Must be less than image
        If tile size is greater than the length of the x or y dimension
        of image throw error.  If the tiles do not crop the enitre image evenly
        pad with zeros until it does such that all tiles are the same size.  Returns
        a TiledImage object.'''
        #TODO
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

def main():
    t = TiledImage()
    t.create('','')

if __name__ == '__main__':
    main()