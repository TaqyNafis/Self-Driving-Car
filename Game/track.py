import pygame
from abc import ABC, abstractmethod
from utils import scale_image

class AbstractTrack(ABC):
    def __init__(self):
        self.track = self.load_track()
        self.track_border_mask = pygame.mask.from_surface(self.track)
        self.track_dimension = self.get_track_dimension()
        
        self.training_weight = self.get_training_weight()

        self.finish = self.load_finish()
        self.finish_pos = self.get_finish_pos()
        self.finish_mask = pygame.mask.from_surface(self.finish)

        self.start_pos = self.get_start_pos()
        self.checkpoints = self.get_checkpoints()


        

    @abstractmethod
    def load_track(self):
        pass

    @abstractmethod
    def get_track_dimension(self):
        pass

    @abstractmethod
    def load_finish(self):
        pass

    @abstractmethod
    def get_finish_pos(self):
        pass

    @abstractmethod
    def get_start_pos(self):
        pass

    @abstractmethod
    def get_checkpoints(self):
        pass

    @abstractmethod
    def get_training_weight(self):
        pass



class Track1(AbstractTrack):
    def load_track(self):
        track = scale_image(pygame.image.load("asset/Track_Folder/track1.png"),1)

        # Make white pixels transparent
        for x in range(track.get_width()):
            for y in range(track.get_height()):
                if track.get_at((x, y))[:3] == (255, 255, 255):
                    track.set_at((x, y), (255, 255, 255, 0))

        return track

    def get_track_dimension(self):
        height = self.track.get_height()
        width = self.track.get_width()
        return (width, height)

    def  get_training_weight(self):
        return 1

    def load_finish(self):
        finish = pygame.image.load("asset/finish.png")

        return pygame.transform.scale(finish, (150, finish.get_height()))

    def get_finish_pos(self):
        return (50,424)

    def get_start_pos(self):
        return (125, 450, 0)

    def get_checkpoints(self):
        checkpoint_data = [
        ((61,400), (170,5)),
        ((61,165), (170,5)),
        ((243,16), (5,150)),
        ((301,31), (5,150)),      
        ((310,165), (190,5)),
        ((400,250), (130,5)),
        ((392,345), (170,5)),
        ((546,356), (5,150)),
        ((616,358), (5,150)),
        ((630,345), (140,5)),
        ((630,214), (140,5)),
        ((774,26), (5,200)),
        ((812,20), (5,200)),
        ((820,214), (170,5)),
        ((830,389), (160,5)),
        ((772,533), (190,5)),
        ((722,558), (5,140)),
        ((496,584), (5,140)),
        ((239,515), (5,170)),
        ((51,491), (190,5))
        ]

        checkpoints = []

        for i, (position, dimension) in enumerate(checkpoint_data, start=1):
            checkpoints.append({
                "rect" : pygame.Rect(position,dimension),
                "number" : i
            })
    
        return checkpoints

class Track2(AbstractTrack):
    def load_track(self):
        track = scale_image(pygame.image.load("asset/Track_Folder/track2.png"),1)

        # Make white pixels transparent
        for x in range(track.get_width()):
            for y in range(track.get_height()):
                if track.get_at((x, y))[:3] == (255, 255, 255):
                    track.set_at((x, y), (255, 255, 255, 0))

        return track

    def get_track_dimension(self):
        height = self.track.get_height()
        width = self.track.get_width()
        return (width, height)

    def  get_training_weight(self):
        return 0.5

    def load_finish(self):
        finish = pygame.image.load("asset/finish.png")

        finish = pygame.transform.scale(
            finish,
            (200, finish.get_height())
        )

        finish = pygame.transform.rotate(finish, 90)

        return finish
    
    def get_finish_pos(self):
        return (399,480)

    def get_start_pos(self):
        return (490, 579, 90)

    def get_checkpoints(self):
        checkpoint_data = [
        ((290,470), (5,200)),
        ((61,450), (210,5)),
        ((77,340), (200,5)),
        ((77,227), (200,5)),
        ((269,63), (5,200)),
        ((518,63), (5,200)),
        ((722,63), (5,200)),
        ((732,235), (200,5)),
        ((732,340), (210,5)),
        ((732,479), (200,5)),
        ((722,470), (5,200)),
        ((518,470), (5,200)),
        ]

        checkpoints = []

        for i, (position, dimension) in enumerate(checkpoint_data, start=1):
            checkpoints.append({
                "rect" : pygame.Rect(position,dimension),
                "number" : i
            })
    
        return checkpoints

class Track3(AbstractTrack):
    def load_track(self):
        track = scale_image(pygame.image.load("asset/Track_Folder/track3.png"),1)

        # Make white pixels transparent
        for x in range(track.get_width()):
            for y in range(track.get_height()):
                if track.get_at((x, y))[:3] == (255, 255, 255):
                    track.set_at((x, y), (255, 255, 255, 0))

        return track

    def get_track_dimension(self):
        height = self.track.get_height()
        width = self.track.get_width()
        return (width, height)

    def  get_training_weight(self):
        return 2

    def load_finish(self):
        finish = pygame.image.load("asset/finish.png")

        return pygame.transform.scale(finish, (150, finish.get_height()))

    def get_finish_pos(self):
        return (50,424)

    def get_start_pos(self):
        return (115, 475, 0)

    def get_checkpoints(self):
        checkpoint_data = [
        ((61,300), (150,5)),
        ((292,40), (5,95)),
        ((315,130), (150,3)),
        ((305,132), (5,110)),
        ((201,277), (150,5)),
        ((364,317), (5,130)),
        ((495,271), (150,5)),
        ((710,48), (5,100)),
        ((724,146), (150,5)),
        ((668,240), (150,5)),
        ((780,355), (180,5)),
        ((709,474), (150,5)),
        ((687,584), (5,100)),
        ((284,584), (5,100)),
        ((57,514), (150,5)),
        ]

        checkpoints = []

        for i, (position, dimension) in enumerate(checkpoint_data, start=1):
            checkpoints.append({
                "rect" : pygame.Rect(position,dimension),
                "number" : i
            })
    
        return checkpoints