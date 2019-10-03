import sys


class Vertex(object):
    def __init__(self, coord):
        self.pvertex_tbl = {}
        self.ivertex_tbl = {}
        self.nvertex_tbl = {}
        self.svertex_tbl = {}
        self.coord = coord
        self.element_num = 0

    def get_street(self):
        return list(self.pvertex_tbl)

    def get_pvertex(self, street_name=None):
        if street_name in self.pvertex_tbl.keys():
            return self.pvertex_tbl[street_name]
        else:
            return None

    def get_nvertex(self, street_name=None):
        if street_name in self.nvertex_tbl.keys():
            return self.nvertex_tbl[street_name]
        else:
            return None

    def add_element(self, street_name=None, vertex_prev=None, vertex_next=None):
        # check if street_id is set first
        if street_name is None or self is vertex_prev or self is vertex_next:
            return
        if street_name not in self.ivertex_tbl:
            self.ivertex_tbl[street_name] = False
        if street_name not in self.svertex_tbl:
            self.svertex_tbl[street_name] = False
        self.pvertex_tbl[street_name] = vertex_prev
        self.nvertex_tbl[street_name] = vertex_next

    def set_intersect(self, street_name=None, intersect=False):
        self.ivertex_tbl[street_name] = intersect

    def set_streetvertex(self, street_name=None, svertex=False):
        self.svertex_tbl[street_name] = svertex

    def remove_element(self, street_name=None):
        if street_name in self.pvertex_tbl:
            self.pvertex_tbl.pop(street_name)
            self.ivertex_tbl.pop(street_name)
            self.svertex_tbl.pop(street_name)
            self.nvertex_tbl.pop(street_name)
        return len(self.svertex_tbl)

    def check_intersect(self):
        for intersect in self.ivertex_tbl.values():
            if intersect:
                return True
        return False

    def check_streetvertex(self):
        for svertex in self.svertex_tbl.values():
            if svertex:
                return True
        return False


def line_vector(coord1, coord2):
    try:
        slope = (float(coord2[1]) - float(coord1[1])) / (float(coord2[0]) - float(coord1[0]))
    except ZeroDivisionError:
        slope = float('INF')
        offset = coord2[0]  # set to x position if the line is vertical
    else:
        offset = float(coord1[1]) - (float(slope) * float(coord1[0]))
    return slope, offset


def find_intercept(lvector1, lvector2):
    slope = 0
    offset = 1
    if lvector1[slope] == lvector2[slope]:
        raise Exception
    else:
        if lvector1[slope] == float('INF'):
            int_x = float(lvector1[offset])
            int_y = float(lvector2[slope]) * float(int_x) + float(lvector2[offset])
        elif lvector2[slope] == float('INF'):
            int_x = float(lvector2[offset])
            int_y = float(lvector1[slope]) * float(int_x) + float(lvector1[offset])
        else:
            int_x = (float(lvector2[offset]) - float(lvector1[offset])) / (
                    float(lvector1[slope]) - float(lvector2[slope]))
            int_y = float(lvector1[slope]) * float(int_x) + float(lvector1[offset])
    int_x = round(int_x, 2)
    int_y = round(int_y, 2)
    if int_x.is_integer():
        int_x = int(int_x)
    if int_y.is_integer():
        int_y = int(int_y)
    return int_x, int_y


class VertexCoverPy(object):
    vertex_id_tbl = {}  # stores the vertex name (based on the location) and pointer to the vertex
    street_id_tbl = {}  # stores the street name and pointer to last street vertex
    __vertex_list_tbl = []
    __edge_list_tbl = []
    __user_input_list = []
    __street_name = ''
    __coordinate_matrix = []

    def __init__(self):
        return

    def process_message(self, user_input=''):
        if user_input == '':
            return
        self.__user_input_list = user_input.replace('\n', '')
        self.__user_input_list = self.__user_input_list.split('"')  # split the input string by quotation mark
        try:
            if len(self.__user_input_list[0]) == 1 and self.__user_input_list[0][0] != 'g':
                print("Error: INVALID COMMAND")
                return
            cmd = self.__user_input_list[0][0]
        except:
            print("Error: INVALID COMMAND")
        else:
            if len(self.__user_input_list) > 3:
                print("Error: EXTRA QUOTATION DETECTED IN USER INPUT")
                return
            if cmd in self.__cmd_tbl:
                method_run = self.__cmd_tbl[cmd]
                method_run(self)
            else:
                print("Error: UNRECOGNIZED COMMAND")

    def __decode_street_name(self):
        STREET_NAME = 1
        try:
            self.__street_name = self.__user_input_list[STREET_NAME].replace('"', '')
        except IndexError:
            print("Error: INVALID STREET NAME")
            return False
        else:
            self.__street_name = self.__street_name.upper()

        streetNameCheck = self.__street_name.replace(' ', '')

        if str.isalpha(streetNameCheck) is False:
            print("Error: INVALID CHARACTER DETECTED IN STREET NAME")
            return False

        return True

    def __decode_coordinate(self):
        COORDINATE = 2
        self.__coordinate_matrix = []
        if self.__user_input_list[COORDINATE][0] != ' ':
            print("Error: MISSING SPACE AFTER QUOTATION")
            return
        cID_list = self.__user_input_list[COORDINATE].replace('  ', ' ')
        cID_list = cID_list.split(' ')
        cID_list = filter(None, cID_list)
        for list_index in range(0, len(cID_list) - 1):
            try:
                if cID_list[list_index][-1].isdigit() and cID_list[list_index + 1][0].isdigit():
                    print("Error: EXTRA SPACE BETWEEN NUMBER IN COORDINATE")
                    return
            except:
                pass

        self.__user_input_list[COORDINATE] = self.__user_input_list[COORDINATE].replace(' ', '')
        try:
            if self.__user_input_list[COORDINATE][0] != "(" or self.__user_input_list[COORDINATE][-1] != ")":
                print("Error: MISSING CLOSING BRACKET IN COORDINATE")
                return
        except:
            pass

        self.__user_input_list[COORDINATE] = self.__user_input_list[COORDINATE][1:-1]
        cID_list = self.__user_input_list[COORDINATE].split(')(')
        for list_index in range(len(cID_list)):
            self.__coordinate_matrix.append(cID_list[list_index].split(','))
            # check if all coordinate string can be convert into integer, if it cant, then it is in invalid format
            try:
                self.__coordinate_matrix[list_index] = [int(x) for x in self.__coordinate_matrix[list_index]]
            except:
                print("Error: INVALID COORDINATE")
                return False

        coordList = []
        for coord_i in range(len(self.__coordinate_matrix)):
            coord = self.__coordinate_matrix[coord_i][0], self.__coordinate_matrix[coord_i][1]
            if coord in coordList:
                print("Error: INTERSECTING STREET DUE TO MULTIPLE OF SAME COORDINATE")
                return False;
            coordList.append(coord)
        return True

    def __remove_vertex(self):
        # Look for the coordinate in the dictionary
        try:
            rvertex = self.street_id_tbl[self.__street_name]
        except KeyError:
            print("Error: STREET DOES NOT EXIST")
        else:
            # remove the vertex for that street
            while rvertex is not None:
                pvertex = rvertex.get_pvertex(self.__street_name)
                nelement = rvertex.remove_element(self.__street_name)
                if nelement <= 0:
                    self.vertex_id_tbl.pop(rvertex.coord, None)
                    del rvertex
                elif nelement == 1 and rvertex.check_intersect() is True:
                    rstreet = rvertex.get_street()[0]
                    rvertex.set_intersect(rstreet, False)
                    if rvertex.check_streetvertex() is False:
                        nvertex_r = rvertex.get_nvertex(rstreet)
                        pvertex_r = rvertex.get_pvertex(rstreet)
                        if nvertex_r is not None:
                            nvertex_r.add_element(rstreet, pvertex_r, nvertex_r.get_nvertex(rstreet))
                        if pvertex_r is not None:
                            pvertex_r.add_element(rstreet, pvertex_r.get_pvertex(rstreet), nvertex_r)
                        self.vertex_id_tbl.pop(rvertex.coord)
                        del rvertex
                rvertex = pvertex

    def __add_vertex(self):
        VPrev, VNext, st = None, None, self.__street_name
        NVertex = []

        # Create a new vertex object for each new coordinate.
        for coord_i in range(len(self.__coordinate_matrix)):
            coord = (self.__coordinate_matrix[coord_i][0], self.__coordinate_matrix[coord_i][1])
            if coord in self.vertex_id_tbl:
                NVertex.append(self.vertex_id_tbl[coord])  # if the vertex already exist
            else:
                NVertex.append(Vertex(coord))  # create a new vertex object
                self.vertex_id_tbl[coord] = NVertex[-1]  # update the vertex table

        # Link the new vertices together.
        NVertex.append(None)
        NVertex.insert(0, None)
        for v_i in range(1, len(NVertex) - 1):
            NVertex[v_i].add_element(st, NVertex[v_i - 1], NVertex[v_i + 1])
            NVertex[v_i].set_streetvertex(st, True)
            self.street_id_tbl[self.__street_name] = NVertex[v_i]

        # Iterate through existing vertices to find intersections.
        NVertex = [NVertex[-3], NVertex[-2], NVertex[-1]]

        while NVertex[0] is not None and NVertex[1] is not None:
            line1 = line_vector(NVertex[0].coord, NVertex[1].coord)
            for pstreet in self.street_id_tbl:
                if pstreet == st:
                    continue
                try:
                    JVertex = [self.street_id_tbl[pstreet].get_pvertex(pstreet), self.street_id_tbl[pstreet], None]
                except:
                    continue

                while JVertex[0] is not None and JVertex[1] is not None:
                    line2 = line_vector(JVertex[1].coord, JVertex[0].coord)
                    if line1[0] != line2[0]:
                        intersect = find_intercept(line1, line2)  # in case division by 0 due to parallel lines
                        seq_x1 = sorted(list(zip(intersect, NVertex[1].coord, NVertex[0].coord)[0]))
                        seq_y1 = sorted(list(zip(intersect, NVertex[1].coord, NVertex[0].coord)[1]))
                        seq_x2 = sorted(list(zip(intersect, JVertex[1].coord, JVertex[0].coord)[0]))
                        seq_y2 = sorted(list(zip(intersect, JVertex[1].coord, JVertex[0].coord)[1]))
                        if intersect[0] == seq_x1[1] == seq_x2[1] and intersect[1] == seq_y1[1] == seq_y2[1]:
                            if intersect in self.vertex_id_tbl:
                                IVertex = self.vertex_id_tbl[intersect]
                            else:
                                IVertex = Vertex(intersect)
                                self.vertex_id_tbl[intersect] = IVertex

                            IVertex.add_element(st, NVertex[0], NVertex[1])
                            NVertex[1].add_element(st, IVertex, NVertex[1].get_nvertex(st))
                            NVertex[0].add_element(st, NVertex[0].get_pvertex(st), IVertex)
                            IVertex.add_element(pstreet, JVertex[0], JVertex[1])
                            JVertex[1].add_element(pstreet, IVertex, JVertex[1].get_nvertex(pstreet))
                            JVertex[0].add_element(pstreet, JVertex[0].get_pvertex(pstreet), IVertex)
                            IVertex.set_intersect(pstreet, True)
                            IVertex.set_intersect(st, True)

                            NVertex[0] = NVertex[1].get_pvertex(st)

                    elif line1 == line2:
                        seq_c = sorted([NVertex[0].coord, NVertex[1].coord, JVertex[0].coord, JVertex[1].coord])
                        seq_v = [self.vertex_id_tbl[seq_c[0]], self.vertex_id_tbl[seq_c[1]],
                                 self.vertex_id_tbl[seq_c[2]], self.vertex_id_tbl[seq_c[3]]]
                        iSpace1 = abs(seq_c.index(NVertex[1].coord) - seq_c.index(NVertex[0].coord))
                        iSpace2 = abs(seq_c.index(JVertex[1].coord) - seq_c.index(JVertex[0].coord))
                        if seq_c[1] == seq_c[2]:
                            seq_v[1].set_intersect(pstreet, True)
                            seq_v[1].set_intersect(st, True)
                        elif iSpace1 == 2 and iSpace2 == 2:
                            seq_z = [NVertex[1], JVertex[1]]
                            seq_st = [st, pstreet]
                            for v in range(len(seq_z)):
                                i = seq_v.index(seq_z[v])
                                mul = 1
                                if i == 2 or i == 3:
                                    mul = -1
                                seq_v[i].add_element(seq_st[v], seq_v[i+(mul*1)], seq_v[i].get_nvertex(seq_st[v]))
                                seq_v[i+(mul*1)].add_element(seq_st[v], seq_v[i+(mul*2)], seq_v[i])
                                seq_v[i+(mul*2)].add_element(seq_st[v], seq_v[i+(mul*2)].get_pvertex(seq_st[v]), seq_v[i+(mul*1)])
                                seq_v[1].set_intersect(seq_st[v], True)
                                seq_v[2].set_intersect(seq_st[v], True)

                    JVertex[1] = JVertex[1].get_pvertex(pstreet)
                    JVertex[0] = JVertex[1].get_pvertex(pstreet)
                    JVertex[2] = JVertex[1].get_nvertex(pstreet)
            NVertex[1] = NVertex[1].get_pvertex(st)
            NVertex[0] = NVertex[1].get_pvertex(st)
            NVertex[2] = NVertex[1].get_nvertex(st)

    def __create_vertex_list(self):
        self.__vertex_list_tbl = []
        for pstreet in self.street_id_tbl:
            cvertex = self.street_id_tbl[pstreet]
            while cvertex is not None:
                nvertex = cvertex.get_nvertex(pstreet)
                pvertex = cvertex.get_pvertex(pstreet)
                iPrev = False
                iNext = False
                iCurr = cvertex.check_intersect()
                if pvertex is not None:
                    iPrev = pvertex.check_intersect()
                if nvertex is not None:
                    iNext = nvertex.check_intersect()
                if cvertex.coord not in self.__vertex_list_tbl:
                    if iNext or iPrev or iCurr:
                        self.__vertex_list_tbl.append(cvertex.coord)
                cvertex = cvertex.get_pvertex(pstreet)
        self.__vertex_list_tbl.sort()

    def __create_edge_list(self):
        self.__edge_list_tbl = []
        for pstreet in self.street_id_tbl:
            cvertex = self.street_id_tbl[pstreet]
            while cvertex is not None:
                nvertex = cvertex.get_nvertex(pstreet)
                iNext = False
                iCurr = cvertex.check_intersect()
                if nvertex is not None:
                    iNext = nvertex.check_intersect()
                if iNext or iCurr and nvertex is not None:
                    if cvertex.coord < nvertex.coord:
                        edge = '<' + str(self.__vertex_list_tbl.index(cvertex.coord) + 1)
                        edge += ',' + str(self.__vertex_list_tbl.index(nvertex.coord) + 1)
                    else:
                        edge = '<' + str(self.__vertex_list_tbl.index(nvertex.coord) + 1)
                        edge += ',' + str(self.__vertex_list_tbl.index(cvertex.coord) + 1)
                    edge += '>'
                    if edge not in self.__edge_list_tbl:
                        self.__edge_list_tbl.append(edge)
                cvertex = cvertex.get_pvertex(pstreet)

    def __add_street(self):
        if self.__decode_street_name():
            # check if street name already exist
            if self.__street_name in self.street_id_tbl:
                print("Error: STREET NAME ALREADY EXIST")
                return
            elif self.__decode_coordinate():
                self.__add_vertex()

    def __change_street(self):
        if self.__decode_street_name():
            if self.__street_name not in self.street_id_tbl:
                print("Error: CANNOT CHANGE STREET, STREET DOES NOT EXIST")
            elif self.__decode_coordinate():
                self.__remove_vertex()
                self.__add_vertex()

    def __remove_street(self):
        if self.__decode_street_name():
            if self.__street_name not in self.street_id_tbl:
                print("Error: CANNOT REMOVE STREET, STREET DOES NOT EXIST")
            else:
                self.__remove_vertex()

    def __graph(self):
        self.__create_vertex_list()
        self.__create_edge_list()

        print('V = {')
        for index in range(len(self.__vertex_list_tbl)):
            id_string = str(index + 1) + ': '
            coord_string = str(self.__vertex_list_tbl[index])
            coord_string = coord_string.replace(' ', '')
            print(' ' + id_string + coord_string)
        print('}')
        print('E = {')
        for edge_index in range(len(self.__edge_list_tbl)):
            print(' ' + str(self.__edge_list_tbl[edge_index]))
        print('}')

    # constant structure defines
    __cmd_tbl = {
        'a': __add_street,
        'c': __change_street,
        'r': __remove_street,
        'g': __graph
    }


def main():
    vertex_cover = VertexCoverPy()
    while True:
        line = sys.stdin.readline()
        vertex_cover.process_message(line)

        if line == '':
            break


if __name__ == '__main__':
    main()
