from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import PIL.ImageFont

from cell import cellIsFilled
from field import Field
from piece import getColorForCell


class FieldPainter:

    WIDTH = 600
    HEIGHT = 1700
    SQUARE_WIDTH = int(WIDTH / Field.WIDTH)
    RECENT_PIECE_START_X = int((2* Field.WIDTH) / 3)
    RECENT_PIECE_START_Y = HEIGHT - 300
    RECENT_TEXT_START_X = RECENT_PIECE_START_X
    RECENT_TEXT_START_Y = RECENT_PIECE_START_Y + 150
    SCORE_TEXT_START_X = RECENT_TEXT_START_X
    SCORE_TEXT_START_Y = RECENT_TEXT_START_Y - 200

    def __init__(self, gameType):
        self.__gameType = gameType
        im = Image.new('RGB', (FieldPainter.WIDTH, FieldPainter.HEIGHT), (200, 200, 200))
        draw = ImageDraw.Draw(im)

        self.fig, ax = plt.subplots(figsize=(3, 5))
        self.im = ax.imshow(im)
        plt.tight_layout()
        plt.ion()
        plt.show(block=False)
        plt.pause(0.1)
        self.font = PIL.ImageFont.truetype("arial.ttf", 60)


    def paintField(self, field, score):
        im = Image.new('RGB', (FieldPainter.WIDTH, FieldPainter.HEIGHT), (210, 210, 210))
        draw = ImageDraw.Draw(im)

        # Score
        draw.text(xy=(FieldPainter.SCORE_TEXT_START_X, FieldPainter.SCORE_TEXT_START_Y),
                  text=f"Score:",
                  fill=(0, 0, 0), font=self.font)
        draw.text(xy=(FieldPainter.SCORE_TEXT_START_X + 400, FieldPainter.SCORE_TEXT_START_Y),
                  text=f"{score}",
                  fill=(0, 0, 0), font=self.font)

        #Draw recent piece
        if field.lastPieceAdded is not None:

            for cell in field.lastPieceAdded.cells:
                x = cell[0]
                y = cell[1]
                draw.rectangle((((FieldPainter.RECENT_PIECE_START_X + x) * FieldPainter.SQUARE_WIDTH,
                                 FieldPainter.RECENT_PIECE_START_Y + (y * FieldPainter.SQUARE_WIDTH)),
                                ((x + 1 + FieldPainter.RECENT_PIECE_START_X) * FieldPainter.SQUARE_WIDTH,
                                 FieldPainter.RECENT_PIECE_START_Y + ((y + 1) * FieldPainter.SQUARE_WIDTH))),
                               fill=field.lastPieceAdded.color,
                               outline=(0, 0, 0))

            draw.text(xy=(FieldPainter.RECENT_TEXT_START_X, FieldPainter.RECENT_TEXT_START_Y), text="Last piece:",
                      fill=(0, 0, 0), font=self.font)
            draw.text(xy=(FieldPainter.RECENT_TEXT_START_X, FieldPainter.RECENT_TEXT_START_Y + 90), text="Cleared lines:",
                      fill=(0, 0, 0), font=self.font)
            draw.text(xy=(FieldPainter.RECENT_TEXT_START_X + 400, FieldPainter.RECENT_TEXT_START_Y + 90), text=f"{field.rowsCleared}",
                      fill=(0, 0, 0), font=self.font)

        for y, rows in enumerate(field.field):
            for x, cell in enumerate(rows):
                if cellIsFilled(cell):
                    draw.rectangle(((x * FieldPainter.SQUARE_WIDTH, y* FieldPainter.SQUARE_WIDTH),
                                    ((x+1) * FieldPainter.SQUARE_WIDTH, (y+1) * FieldPainter.SQUARE_WIDTH)),
                                   fill=getColorForCell(cell, self.__gameType),
                                   outline=(0,0,0))
                else:
                    if y < Field.HEIGHT - Field.LOSE_HEIGHT:
                        color = (255,0,0)
                    else:
                        color = (210,210,210)
                    draw.rectangle(((x * FieldPainter.SQUARE_WIDTH, y* FieldPainter.SQUARE_WIDTH),
                                    ((x+1) * FieldPainter.SQUARE_WIDTH, (y+1) * FieldPainter.SQUARE_WIDTH)),
                                   fill=color,
                                   outline=(0,0,0))

        self.im.set_data(im)
        plt.pause(0.1)
