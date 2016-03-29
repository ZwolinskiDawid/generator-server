from Block import *
from xml.etree.ElementTree import *


class Container:
    def __init__(self):
        self.size = self.read_size()
        self.segmentSize = self.read_segment_size()
        self.map = list()

        self.map_of_obstacles = list()
        self.create_map_of_obstacles()

        self.segments = list()
        self.read_segments()

        self.generate_map()
        self.generate_obstacles()

    def create_map_of_obstacles(self):
        for i in range(self.size):
            self.map_of_obstacles.append(list())
            for j in range(self.size):
                self.map_of_obstacles[i].append(None)

    @staticmethod
    def read_segment_size():
        dom_tree = minidom.parse('init.xml')
        nodes = dom_tree.childNodes
        return int(nodes[0].getElementsByTagName("segmentSize")[0].childNodes[0].toxml())

    @staticmethod
    def read_size():
        dom_tree = minidom.parse('init.xml')
        nodes = dom_tree.childNodes
        return int(nodes[0].getElementsByTagName("size")[0].childNodes[0].toxml())

    def read_segments(self):
        dom_tree = minidom.parse('segments.xml')
        nodes = dom_tree.childNodes
        for i in nodes[0].getElementsByTagName("segment"):
            self.segments.append(i.childNodes[0].toxml())

    def generate_map(self):
        for i in range(self.size):
            self.map.append(list())
            for j in range(self.size):

                options = list()

                if i - 1 < 0 and j - 1 < 0:
                    options.append(random.choice(random.choice(Block.blocks[1])))

                elif i - 1 < 0:
                    block = self.map[i][j - 1]
                    options.append(random.choice(Block.blocks[1][block.type_of_block]))

                elif j - 1 < 0:
                    block = self.map[i - 1][j]
                    options.append(random.choice(Block.blocks[1][block.type_of_block]))

                else:
                    block = self.map[i][j - 1]
                    options.append(random.choice(Block.blocks[1][block.type_of_block]))

                    block = self.map[i - 1][j]
                    options.append(random.choice(Block.blocks[1][block.type_of_block]))

                    block = self.map[i - 1][j - 1]
                    options.append(random.choice(Block.blocks[1][block.type_of_block]))

                if len(options) == 0 or random.randint(1, 10) < 3:
                    block = random.choice(random.choice(Block.blocks[1]))
                else:
                    block = random.choice(options)

                self.map[i].append(block)

    def generate_obstacles(self):
        for i in range(int(self.size / self.segmentSize)):
            for j in range(int(self.size / self.segmentSize)):

                #  random segment
                segment = random.choice(self.segments)

                for k in range(self.segmentSize):
                    for l in range(self.segmentSize):

                        #  reading one field of segment
                        if segment[k * self.segmentSize + l] == 'x':

                            options = []

                            if i * self.segmentSize + (k - 1) < 0 and j * self.segmentSize + (l - 1) < 0:
                                options.append(random.choice(random.choice(Block.blocks[0])))

                            elif i * self.segmentSize + (k - 1) < 0:
                                block = self.map[i * self.segmentSize + k][j * self.segmentSize + (l - 1)]
                                if block.walkable == 0:
                                    options.append(random.choice(Block.blocks[0][block.type_of_block]))

                            elif j * self.segmentSize + (l - 1) < 0:
                                block = self.map[i * self.segmentSize + (k - 1)][j * self.segmentSize + l]
                                if block.walkable == 0:
                                    options.append(random.choice(Block.blocks[0][block.type_of_block]))

                            else:
                                block = self.map[i * self.segmentSize + k][j * self.segmentSize + (l - 1)]
                                if block.walkable == 0:
                                    options.append(random.choice(Block.blocks[0][block.type_of_block]))

                                block = self.map[i * self.segmentSize + (k - 1)][j * self.segmentSize + l]
                                if block.walkable == 0:
                                    options.append(random.choice(Block.blocks[0][block.type_of_block]))

                                block = self.map[i * self.segmentSize + (k - 1)][j * self.segmentSize + (l - 1)]
                                if block.walkable == 0:
                                    options.append(random.choice(Block.blocks[0][block.type_of_block]))

                            if len(options) == 0 or random.randint(1, 10) < 3:
                                block = random.choice(random.choice(Block.blocks[0]))
                            else:
                                block = random.choice(options)

                            self.map_of_obstacles[i * self.segmentSize + k][j * self.segmentSize + l] = block

    def save_to_xml(self):

        container = Element('container')
        container.set('size', str(self.size))

        background = SubElement(container, 'background')

        for i in range(self.size):
            tmp = list()
            for j in range(self.size):
                tmp.append(str(self.map[i][j].appearance))

            line = SubElement(background, 'line')
            line.text = ''.join(tmp)

        foreground = SubElement(container, 'foreground')

        for i in range(self.size):
            tmp = list()
            for j in range(self.size):
                if self.map_of_obstacles[i][j] is not None:
                    tmp.append(str(self.map_of_obstacles[i][j].appearance))
                else:
                    tmp.append('n')

            line = SubElement(foreground, 'line')
            line.text = ''.join(tmp)

        file = open("container.xml", "w")
        file.write(tostring(container).decode("utf-8") )
        file.close()

C = Container()
C.save_to_xml()



