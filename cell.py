
CLEARED_CELL = -1
#Text based cells

def cellIsFilled(cell):
    return cell != CLEARED_CELL

#def cellCollides(cell1, cell2):
#    return cellIsFilled(cell1) and cellIsFilled(cell2)


#Class based cells
# class Cell():
#
#     def __init__(self):
#         self.filled = False
#         self.type = "X"
#
#     def simpleCopy(self):
#         cell = Cell()
#         if self.filled:
#             cell.fillWithType(self.type)
#         return cell
#
#     def fill(self):
#         self.filled = True
#
#     def fillWithType(self, type):
#         self.type = type
#         self.fill()
#
#     def clear(self):
#         self.filled = False
#
#     def collides(self, otherCell):
#         return self.filled and otherCell.filled