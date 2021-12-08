from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        n = self.read_input()
        interval = int(n*2 / len(self.workers))

        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(-n + i * interval, -n + i * interval + interval, n))

        result = self.myreduce(mapped)
        self.write_output(result)

    @staticmethod
    @expose
    def mymap(a, b, r):
        res = 0
        for i in range(a, b):
            for j in range(-r, r):
                if Solver.is_inside(i, j, r):
                    res += 1
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = 0
        for x in mapped:
            output += int(x.value)
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()

    @staticmethod
    @expose
    def is_inside(x, y, r):
        if (x*x + y*y <= r*r):
 	        return True
        return False