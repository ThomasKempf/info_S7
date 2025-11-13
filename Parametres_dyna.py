#♦ New filefor being able to modify every single parameters

class Train(Global):
    def __init__(self,num:int) -> None:
        super().__init__()
        self.titre = f'train_{num}'
        self.description =  {
            'global': Train_global(),
            'pignon': Engrenage(0),
            'roue': Engrenage(1)
        }
        self.description['pignon'].titre = 'pignon'
        self.description['roue'].titre = 'roue'
        self.unitee = None