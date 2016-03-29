from Thing import *


class Block(Thing):
    blocks = list()

    @staticmethod
    def read_table():
        dom_tree = minidom.parse("textures.xml")
        c_nodes = dom_tree.childNodes

        types_of_block = list()

        # walkable[0] = false, walkable[1] = true
        for i in range(2):
            Block.blocks.append(list())
            types_of_block.append(list())

        i = 0
        for texture in c_nodes[0].getElementsByTagName("texture"):
            type_of_block = texture.getAttribute("type")
            walkable = texture.getAttribute("walkable")

            if walkable == 'True':
                walkable = 1
            else:
                walkable = 0

            if types_of_block[walkable].count(type_of_block) == 0:  # if type has not exist yet
                types_of_block[walkable].append(type_of_block)
                Block.blocks[walkable].append(list())
                index = len(Block.blocks[walkable]) - 1
                Block.blocks[walkable][index].append(Block(i))
            else:
                index = types_of_block[walkable].index(type_of_block)
                Block.blocks[walkable][index].append(Block(i))
            i += 1

    def __init__(self, appearance):
        Thing.__init__(self, appearance)

Block.read_table()
