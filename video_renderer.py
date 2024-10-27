import pygame as pg
import cv2
import numpy as np

class ASCIIArtConverter:
    def __init__(self, video_path, font_size=12, color_levels=8):
        pg.init()
        self.video_path = video_path
        self.font_size = font_size
        self.color_levels = color_levels
        self.ascii_characters = '.",:;!~+-xmo*#W&8@'
        self.ascii_coefficient = 255 // (len(self.ascii_characters) - 1)
        self.char_step = int(font_size * 0.6)
        self.palette, self.color_coefficient = self.create_palette()

        self.video_capture = cv2.VideoCapture(self.video_path)
        if not self.video_capture.isOpened():
            raise ValueError(f"Could not open video: {self.video_path}")

        self.width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.surface = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()

    def create_palette(self):
        color_levels, color_coeff = np.linspace(0, 255, num=self.color_levels, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in color_levels for g in color_levels for b in color_levels]
        palette = dict.fromkeys(self.ascii_characters, None)
        color_coeff = int(color_coeff)

        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color // color_coeff)
                char_palette[color_key] = pg.font.SysFont('Courier', self.font_size, bold=True).render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coeff

    def draw_ascii_image(self, gray_image, color_image):
        char_indices = gray_image // self.ascii_coefficient
        color_indices = color_image // self.color_coefficient
        for x in range(0, self.width, self.char_step):
            for y in range(0, self.height, self.char_step):
                char_index = char_indices[x, y]
                if char_index:
                    char = self.ascii_characters[char_index]
                    color = tuple(color_indices[x, y])
                    self.surface.blit(self.palette[char][color], (x, y))

    def run(self):
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            transposed_image = cv2.transpose(frame)
            rgb_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
            gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)

            self.surface.fill('black')
            self.draw_ascii_image(gray_image, rgb_image)
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.video_capture.release()
                    pg.quit()
                    exit()

            self.clock.tick(30)  

        self.video_capture.release()

if __name__ == '__main__':
    app = ASCIIArtConverter(video_path='output.mp4')  
    app.run()
