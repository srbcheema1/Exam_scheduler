from srblib import Tabular

class WorkRatio:
    def __init__(self,filepath):
        matrix = Tabular()
        matrix.load_xls(filepath,strict=True)
        matrix = matrix.matrix[1:]
        self.ratio = {}
        self.credits = {0:999999}
        for x in matrix:
            self.ratio[int(x[0])] = float(x[1])

        if not 1 in self.ratio: self.ratio[1] = 100
        for x in matrix:
            self.credits[int(x[0])] = self._credits_calc(int(x[0]))


    def _credits_calc(self,rank):
        return (100*self.ratio[1])/self.ratio[rank]

    def credits_calc(self,rank):
        rank = int(rank)
        return self.credits[rank]
