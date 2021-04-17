import pandas as pd
import numpy as np
import os

def tutorial():
    start = input("Do you need a tutorial? (y/n): ")
    if ((start == "Y") or (start == 'y') or (start == 'yes') or (start == 'Yes')):
        print("1. Input the entire ID only Excel file path. It must not have surrounding quotations. Ex. C:\\documents\\mircore\\example.xlsx")
        print("2. Using the same format, input the path of the Excel file containing IDs and Gene Symbols.")
        print('3. Press enter and wait for the program to say "Done!"')
        print("4. Navigate to the directory (folder) with this program")
        print("5. The file you are looking for should be named the original file plus symboled.csv. Ex. example_symboled.csv")
        print("6. To run the program again, close the window and re-start the program")
        print("Have fun!")
        print("")
    else:
        print("")
        pass

def user_input():
    file1 = input("Insert file path for ID only file (full): ")
    file2 = input("Insert file path for ID and Gene Symbol file (full): ")

    df1 = pd.read_csv(file1, delim_whitespace=True)
    df2 = df = pd.read_csv(file2, delim_whitespace=True)

    return df1, df2, file1

def establish(df1):
    df_final = df1
    
    x, y = df1.shape
    col2 = []

    for num in range(x): #add second column as NaN
       col2.append(np.nan)

    df_final["Gene.symbol"] = col2
    return df_final

def iterate(df2, df_final):
	x, y = df2.shape
	z, w = df_final.shape
	lower = 0
	upper = x-1
	bounds = [lower, upper]
	reset_bounds = bounds
	reset_bool = False
	for r in range(z):
		comp = df_final.loc[r, "ID"]
		#if reset_bool is true
		if reset_bool:
			lower = 0
			upper = x-1
			bounds = [lower, upper]
			reset_bool = False
		#create sub loop
		while not reset_bool: 
			#adjust the upper and lower bounds
			if comp == df2.loc[bounds[0], "ID"]:
				df_final.loc[r, 'Gene.symbol'] = df2.loc[bounds[0], "GENE_SYMBOL"]
				reset_bool = True
			elif comp == df2.loc[bounds[1], "ID"]:
				df_final.loc[r, 'Gene.symbol'] = df2.loc[bounds[1], "GENE_SYMBOL"]
				reset_bool = True
			elif comp == df2.loc[bounds[0]+1, "ID"]:
				df_final.loc[r, 'Gene.symbol'] = df2.loc[bounds[0]+1, "GENE_SYMBOL"]
				reset_bool = True
			elif comp == df2.loc[(bounds[1]+bounds[0])//2, "ID"]:
				df_final.loc[r, 'Gene.symbol'] = df2.loc[(bounds[1]+bounds[0])//2, "GENE_SYMBOL"]
				reset_bool = True
			elif df2.loc[bounds[0]+1, "ID"] == df2.loc[bounds[1], "ID"]: #!need to add more specificity
				reset_bool = True
			elif comp < df2.loc[(bounds[1]+bounds[0])//2, "ID"]: #higher (than upper) on the df - 2 enters here
				bounds = [bounds[0],(bounds[1]+bounds[0])//2]
			elif comp > df2.loc[(bounds[1]+bounds[0])//2, "ID"]: #lower (than lower) on the df
				bounds = [(bounds[1]+bounds[0])//2, bounds[1]]

	return df_final


def goodbye(file):
    x = ''
    final = ''
    for letter in file:
        if (letter != "."):
            x = x + letter
        else:
           break 
    newPath = x.replace(os.sep, '/')
    for letter in newPath:
        if (letter != "/"):
            final = final + letter
        else:
            final = ''
    final = final + "_symboled"

    df_final.to_csv(f'{final}.csv', index=False) 
    print("done!")	


if __name__ == "__main__":
    tutorial()
    df1, df2, file2 = user_input()
    df_final = establish(df1)
    df_final = iterate(df2, df_final)
    goodbye(file2)