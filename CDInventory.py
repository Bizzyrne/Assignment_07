#------------------------------------------#
# Title: Assignment07.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# J. Byrne, 2021-Aug-15, Modified File (Addressed TODOs)
# J. Byrne, 2021-Aug-21, Modified File (Add struct. error handling & use binary files)
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dictionaries to hold data
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing the data to and from list in memory"""
    
    def add_to_table(cd_row):
        """Function that adds CD dictionary to main list of CD dictionaries
        
        Args:
            cd_row - dictionary containing information for one CD
        
        Returns:
            None.
        """
        lstTbl.append(cd_row)

    def del_from_table(cd_ID):
        """Deletes CD data from lstTbl with the same cd_ID provided
        
        Args:
            cd_ID - ID of the cd to be deleted
            
        Returns:
            None.
        """
        # search thru table and delete CD
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if int(row['ID']) == int(cd_ID):
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
            
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from file to a list of dictionaries

         Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            table:  Returns table so it can be assigned to list in memory.
        """
        table = []  # this clears existing data and allows to load data from file
        
        try:
            objFile = open(file_name, 'rb')
            table = pickle.load(objFile)
            objFile.close()
            return table
        
        except:
            print("File does not exist.")

    @staticmethod
    def write_file(file_name, Table):
        """Function to write data from list of dictionaries to file

        Writes data to [strFileName] from list of dictionaries lstTbl.  
        Each dictionary in list is written as one row in the file.

        Args:
            file_name: This is the name of the file to be created/written to
            Table: This variable imports the current list in memory to the function 
                    so it can be written to file.
        Returns:
            None.
        """
        objFile = open(file_name, 'wb')
        pickle.dump(Table, objFile)
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    def new_CD_data():
        """Asks user for new CD data
        
        Args:
            none
            
        Returns:
            new_CD_dic - dictionary containing new CD data
            
        """
        new_CD_dic = {}
        x = 0
        
        while x == 0:
            try:
                strID = input('Enter ID: ').strip()
                strID = int(strID)
                strTitle = input('What is the CD\'s title? ').strip()
                stArtist = input('What is the Artist\'s name? ').strip()
                new_CD_dic = {'ID': strID, 'Title': strTitle, 'Artist': stArtist}
                x = 1      
            except:
                print("CD ID must be an interger")
            
        return new_CD_dic
    
# 1. When program starts, read in the currently saved Inventory
try:    
    lstTbl = FileProcessor.read_file(strFileName)
except:
    print("--------No Saved Data--------\n\n")
    
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled:  ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = []
            lstTbl = FileProcessor.read_file(strFileName)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        new_cd = IO.new_CD_data()
        
        # 3.3.2 Add item to the table
        DataProcessor.add_to_table(new_cd)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        
        counter = 0
        
        while counter == 0:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                counter = 1
            except:
                print("\nPlease input an interger\n")
                
        DataProcessor.del_from_table(intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)

        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




