class Graduates:
	def __init__(self):
		self.data = [] # data is the list of rows that included in the table.
			
	
	def ins_data(self):
		self.data = [
			['B10101', 'Eleni', 'Mika','CS', 10],
			['A10250', 'Maria', 'Papadopoulou','EC', 10],
			['T15510', 'Dimitra', 'Gewrgouli','DS', 10],
			['P51515', 'Athanasia', 'Mosxouli', 'EC', 9],
			['R51515', 'Marios', 'Mpekas', 'CS', 9],
			['E55111', 'Kwstas', 'Paulou', 'DS', 8],
			['Y15151', 'Paulos', 'Mpratis', 'CS', 8],
			['E21021', 'Xristina', 'Ferentinos', 'MS', 8],
			['V45151', 'Giorgos', 'Skoulos', 'RLAW', 8],
			['W22515', 'Nikos', 'Menegakis', 'THEOL', 8],
			['B55151', 'Iasonas', 'Iwannou', 'PHYL', 7],
			['E51511', 'Katerina', 'Iwsifidou', 'EDU', 7],
			['N55151', 'Iliana', 'Iwakim', 'THEOL', 7],
			['Q55155', 'Stevi', 'Kasimath', 'HS', 7],
			['X55115', 'Petros', 'Mpikas', 'PS', 7],
			['J15151', 'Vasiliki', 'Giannakopoulou', 'RLAW', 7],
			['M51515', 'Aggelos', 'Karafwtis', 'EDU', 6]
		]

#Create Graduates object			
gr = Graduates()
#Fill in the data table
gr.ins_data()


