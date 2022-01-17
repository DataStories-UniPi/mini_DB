from __future__ import annotations
import sys
from tokenize import group
from tabulate import tabulate
import pickle
import os
from misc import get_op, split_condition
from collections import OrderedDict
 
def search_between(s, first, last):
        '''
        Search in 's' for the substring that is between 'first' and 'last'
        '''
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
        except:
            return
        return s[start:end].strip()

class Table:
    '''
    Table object represents a table inside a database

    A Table object can be created either by assigning:
        - a table name (string)
        - column names (list of strings)
        - column types (list of functions like str/int etc)
        - primary (name of the primary key column)

    OR

        - by assigning a value to the variable called load. This value can be:
            - a path to a Table file saved using the save function
            - a dictionary that includes the appropriate info (all the attributes in __init__)

    '''

    

    def __init__(self, name=None, column_names=None, column_types=None, primary_key=None, load=None):

        if load is not None:
            # if load is a dict, replace the object dict with it (replaces the object with the specified one)
            if isinstance(load, dict):
                self.__dict__.update(load)
                # self._update()
            # if load is str, load from a file
            elif isinstance(load, str):
                self._load_from_file(load)

        # if name, columns_names and column types are not none
        elif (name is not None) and (column_names is not None) and (column_types is not None):

            self._name = name

            if len(column_names)!=len(column_types):
                raise ValueError('Need same number of column names and types.')

            self.column_names = column_names

            self.columns = []

            for col in self.column_names:
                if col not in self.__dir__():
                    # this is used in order to be able to call a column using its name as an attribute.
                    # example: instead of table.columns['column_name'], we do table.column_name
                    setattr(self, col, [])
                    self.columns.append([])
                else:
                    raise Exception(f'"{col}" attribute already exists in "{self.__class__.__name__} "class.')

            self.column_types = [eval(ct) if not isinstance(ct, type) else ct for ct in column_types]
            self.data = [] # data is a list of lists, a list of rows that is.

            # if primary key is set, keep its index as an attribute
            if primary_key is not None:
                self.pk_idx = self.column_names.index(primary_key)
            else:
                self.pk_idx = None

            self.pk = primary_key
            # self._update()

    # if any of the name, columns_names and column types are none. return an empty table object

    

    def column_by_name(self, column_name):
        return [row[self.column_names.index(column_name)] for row in self.data]


    def _update(self):
        '''
        Update all the available columns with the appended rows.
        '''
        self.columns = [[row[i] for row in self.data] for i in range(len(self.column_names))]
        for ind, col in enumerate(self.column_names):
            setattr(self, col, self.columns[ind])

    def _cast_column(self, column_name, cast_type):
        '''
        Cast all values of a column using a specified type.

        Args:
            column_name: string. The column that will be casted.
            cast_type: type. Cast type (do not encapsulate in quotes).
        '''
        # get the column from its name
        column_idx = self.column_names.index(column_name)
        # for every column's value in each row, replace it with itself but casted as the specified type
        for i in range(len(self.data)):
            self.data[i][column_idx] = cast_type(self.data[i][column_idx])
        # change the type of the column
        self.column_types[column_idx] = cast_type
        # self._update()


    def _insert(self, row, insert_stack=[]):
        '''
        Insert row to table.

        Args:
            row: list. A list of values to be inserted (will be casted to a predifined type automatically).
            insert_stack: list. The insert stack (empty by default).
        '''
        if len(row)!=len(self.column_names):
            raise ValueError(f'ERROR -> Cannot insert {len(row)} values. Only {len(self.column_names)} columns exist')

        for i in range(len(row)):
            # for each value, cast and replace it in row.
            # try:
            row[i] = self.column_types[i](row[i])
            # except:
            #     raise ValueError(f'ERROR -> Value {row[i]} of type {type(row[i])} is not of type {self.column_types[i]}.')

            # if value is to be appended to the primary_key column, check that it doesnt alrady exist (no duplicate primary keys)
            if i==self.pk_idx and row[i] in self.column_by_name(self.pk):
                raise ValueError(f'## ERROR -> Value {row[i]} already exists in primary key column.')

        # if insert_stack is not empty, append to its last index
        if insert_stack != []:
            self.data[insert_stack[-1]] = row
        else: # else append to the end
            self.data.append(row)
        # self._update()

    def _update_rows(self, set_value, set_column, condition):
        '''
        Update where Condition is met.

        Args:
            set_value: string. The provided set value.
            set_column: string. The column to be altered.
            condition: string. A condition using the following format:
                'column[<,<=,=,>=,>]value' or
                'value[<,<=,=,>=,>]column'.
                
                Operatores supported: (<,<=,=,>=,>)
        '''
        # parse the condition
        column_name, operator, value = self._parse_condition(condition)

        # get the condition and the set column
        column = self.column_by_name(column_name)
        set_column_idx = self.column_names.index(set_column)

        # set_columns_indx = [self.column_names.index(set_column_name) for set_column_name in set_column_names]

        # for each value in column, if condition, replace it with set_value
        for row_ind, column_value in enumerate(column):
            if get_op(operator, column_value, value):
                self.data[row_ind][set_column_idx] = set_value

        # self._update()
                # print(f"Updated {len(indexes_to_del)} rows")


    def _delete_where(self, condition):
        '''
        Deletes rows where condition is met.

        Important: delete replaces the rows to be deleted with rows filled with Nones.
        These rows are then appended to the insert_stack.

        Args:
            condition: string. A condition using the following format:
                'column[<,<=,==,>=,>]value' or
                'value[<,<=,==,>=,>]column'.
                
                Operatores supported: (<,<=,==,>=,>)
        '''
        column_name, operator, value = self._parse_condition(condition)

        indexes_to_del = []

        column = self.column_by_name(column_name)
        for index, row_value in enumerate(column):
            if get_op(operator, row_value, value):
                indexes_to_del.append(index)

        # we pop from highest to lowest index in order to avoid removing the wrong item
        # since we dont delete, we dont have to to pop in that order, but since delete is used
        # to delete from meta tables too, we still implement it.

        for index in sorted(indexes_to_del, reverse=True):
            if self._name[:4] != 'meta':
                # if the table is not a metatable, replace the row with a row of nones
                self.data[index] = [None for _ in range(len(self.column_names))]
            else:
                self.data.pop(index)

        # self._update()
        # we have to return the deleted indexes, since they will be appended to the insert_stack
        return indexes_to_del


    def aggregate_implementation(self,aggregate_functions,rows):
        elements_of_all_aggregate_functions = []
        aggregate_columns = []
        if aggregate_functions['max'] is not None:
                max_column = [i for i in aggregate_functions['max']]
                
                max_column_data = []
                for i in max_column:
                    max_column_data.append(self.column_by_name(i)) #gives all the data-rows(as a list) of the i column
                

                max_column_data = [[max_column_data[i][j] for j in rows] for i in range(len(max_column))] #keep only the rows selected above in condition
                max_element = [max(i) for i in max_column_data] #contains the max element of each column we are looking for max()
                
                elements_of_all_aggregate_functions += max_element
                aggregate_columns+=max_column
                #print(max_element)
                
                #print(max_element)
                '''for i in range(len(max_element)):
                    max_index.append([max_column_data[i].index( max_element[i])]) #contains each list's max element's index'''
        
        if aggregate_functions['min'] is not None:
                min_column = [i for i in aggregate_functions['min']]
                min_column_data = []
                for i in min_column:
                    min_column_data.append(self.column_by_name(i)) #gives all the data-rows(as a list) of the i column
                
                min_column_data = [[min_column_data[i][j] for j in rows] for i in range(len(min_column))] #keep only the rows selected above in condition

                min_element = [min(i) for i in min_column_data] #contains the min element of each column we are looking for min()
                elements_of_all_aggregate_functions += min_element
                aggregate_columns+=min_column
        if aggregate_functions['count'] is not None:
                count_column = [i for i in aggregate_functions['count']]
                count_column_data = []
                for i in count_column:
                    count_column_data.append(self.column_by_name(i)) #gives all the data-rows(as a list) of the i column
                
                count_column_data = [[count_column_data[i][j] for j in rows] for i in range(len(count_column))] #keep only the rows selected above in condition

                count_element = [len(i) for i in count_column_data] #contains the count element of each column we are looking for count()
                elements_of_all_aggregate_functions+= count_element
                aggregate_columns+=count_column
        if aggregate_functions['avg'] is not None:
                avg_column = [i for i in aggregate_functions['avg']]
                avg_column_data = []
                for i in avg_column:
                    avg_column_data.append(self.column_by_name(i)) #gives all the data-rows(as a list) of the i column
                
                avg_column_data = [[avg_column_data[i][j] for j in rows] for i in range(len(avg_column))] #keep only the rows selected above in condition

                avg_element = [sum(i)/len(i) for i in avg_column_data] #contains the avg element of each column we are looking for avg()
                elements_of_all_aggregate_functions+= avg_element
                aggregate_columns+=avg_column
        if aggregate_functions['sum'] is not None:
                sum_column = [i for i in aggregate_functions['sum']]
                sum_column_data = []
                for i in sum_column:
                    sum_column_data.append(self.column_by_name(i)) #gives all the data-rows(as a list) of the i column
                
                sum_column_data = [[sum_column_data[i][j] for j in rows] for i in range(len(sum_column))] #keep only the rows selected above in condition

                sum_element = [sum(i) for i in sum_column_data] #contains the sum element of each column we are looking for sum()
                elements_of_all_aggregate_functions+= sum_element
                aggregate_columns+=sum_column

                '''for key,value in self.__dict__.items():
                            if key=="data":
                                for k in range(len(max_index)):
                                    for i in return_cols:
                                            for j in max_index[k]:
                                                dict = { key: [self.data[j][i]] }       
                            else:
                                dict = {key:value}'''
        print(elements_of_all_aggregate_functions)
        #dict = {(key):([[self.data[i][j] for j in return_cols for i in max_index[k]] for k in range(len([max_index]))]  if key=="data" else value) for key,value in self.__dict__.items()}
        dict = {(key):([elements_of_all_aggregate_functions]if key=="data" else value) for key,value in self.__dict__.items()}
        #dict = {(key):([[self.data[i][j] for j in return_cols] for i in [elements_of_all_aggregate_functions]] if key=="data" else value) for key,value in self.__dict__.items()}
        
        return_cols = [self.column_names.index(col.strip()) for col in aggregate_columns]
        
        aggr_fun_col= []
        for key, value in aggregate_functions.items():
            if value is not None:
                for i in range(len(value)):
                    aggr_fun_col.append(key)
        #print(aggr_fun_col)
        
        dict['column_names'] = [aggr_fun_col[i]+"(" +self.column_names[j]+ ")" for i,j in enumerate(return_cols)]
        dict['column_types'] = [None for i in return_cols]
        dict['pk_idx'] = None
        dict['pk'] = None
        return dict


    def _select_where(self, return_columns, condition=None,group_by=None, order_by=None, desc=True, top_k=None):
        '''
        Select and return a table containing specified columns and rows where condition is met.

        Args:
            return_columns: list. The columns to be returned.
            condition: string. A condition using the following format:
                'column[<,<=,==,>=,>]value' or
                'value[<,<=,==,>=,>]column'.
                
                Operatores supported: (<,<=,==,>=,>)
            order_by: string. A column name that signals that the resulting table should be ordered based on it (no order if None).
            desc: boolean. If True, order_by will return results in descending order (False by default).
            top_k: int. An integer that defines the number of rows that will be returned (all rows if None).
        '''
        aggregate_functions = {
                'max': None,
                'min': None,
                'count': None,
                'avg': None,
                'sum': None,
                }
        found = False #if at least one aggregate function was found

        # if * return all columns, else find the column indexes for the columns specified
        if return_columns == '*':
            if not group_by:
                return_cols = [i for i in range(len(self.column_names))]
            else:
                sys.exit("\n you have to select the column you use for group by")
            #print(return_cols)
            #print(self.return_cols)
        else:
            
            splitted_columns=return_columns.split(",")
            splitted_columns= [x.replace(' ','') for x in splitted_columns]
            
            if group_by is not None and group_by not in splitted_columns:
                sys.exit("\n you have to select the column you use for group by") 
            #print(splitted_columns)
            
            
            
            for i in splitted_columns:
                for key, value in aggregate_functions.items():
                    in_parenthesis = search_between(i,key+"(",")")
                    if in_parenthesis is not None:
                        found = True #found at least one aggreagate function
                        #print("true")
                        splitted_columns[splitted_columns.index(i)] = in_parenthesis
                        if(value is None):
                            aggregate_functions[key]= [in_parenthesis]
                        else:
                            aggregate_functions[key].append(in_parenthesis) 
                        
                    
            #print(splitted_columns)
            
            #print(aggregate_functions)
            if not group_by:
                return_cols = [self.column_names.index(col.strip()) for col in splitted_columns]
            else:
                if not found:
                    return_cols = [self.column_names.index(group_by)]
                else:
                    return_cols = [self.column_names.index(col.strip()) for col in splitted_columns]
            
            #return_cols = [self.column_names.index(col.strip()) for col in splitted_columns]
            
            #print(splitted_columns)
            #print(self.column_names[return_cols[0]])
            #print(self.column_by_name("tot_cred"))
        #print(return_cols)   
        # if condition is None, return all rows
        # if not, return the rows with values where condition is met for value
        if condition is not None:
            column_name, operator, value = self._parse_condition(condition)
            column = self.column_by_name(column_name)
            rows = [ind for ind, x in enumerate(column) if get_op(operator, x, value)]
            #print(rows)
        else:
            rows = [i for i in range(len(self.data))]
            #print(self.data[0][2])
            
        
        if(found):
            if not group_by:
                dict = self.aggregate_implementation(aggregate_functions,rows)
                #print(dict)
            else:
                all_columns = [group_by]
                aggregate_all = []
                
                if aggregate_functions['max'] is not None:
                    max_column = [i for i in aggregate_functions['max']]
                    max_column_data = []
                    for i in max_column:
                        max_column_data.append(self.column_by_name(i)) #gives all the data-rows(as a list) of the i column
                    
                    max_column_data = [[max_column_data[i][j] for j in rows] for i in range(len(max_column))] #keep only the rows selected above in condition
                    group_by_column_data = self.column_by_name(group_by)
                    
                    group_data = list(sorted(set(group_by_column_data),key = group_by_column_data.index))
                    all_columns+=max_column
                    
                    for k in range(len(max_column_data)):
                        max =[None]*len(group_data)
                        for i in range(len(max_column_data[k])):
                            for j in range(len(group_data)):
                                if group_by_column_data[i]==group_data[j]:
                                    if max[j] is None:
                                        max[j] = max_column_data[k][i] 
                                    else:
                                        if max_column_data[k][i] > max[j]:
                                            max[j] = max_column_data[k][i] 
                        aggregate_all.append(max)
                    

                if aggregate_functions['min'] is not None:
                    min_column = [i for i in aggregate_functions['min']]
                    min_column_data = []
                    for i in min_column:
                        min_column_data.append(self.column_by_name(i)) #gives all the data-rows(as a list) of the i column
                    
                    min_column_data = [[min_column_data[i][j] for j in rows] for i in range(len(min_column))] #keep only the rows selected above in condition
                    group_by_column_data = self.column_by_name(group_by)
                    
                    group_data = list(sorted(set(group_by_column_data),key = group_by_column_data.index))
                    all_columns+=min_column
                    
                    for k in range(len(min_column_data)):
                        min =[None]*len(group_data)
                        for i in range(len(min_column_data[k])):
                            for j in range(len(group_data)):
                                if group_by_column_data[i]==group_data[j]:
                                    if min[j] is None:
                                        min[j] = min_column_data[k][i] 
                                    else:
                                        if min_column_data[k][i] < min[j]:
                                            min[j] = min_column_data[k][i] 
                        aggregate_all.append(min)

                if aggregate_functions['count'] is not None:
                    count_column = [i for i in aggregate_functions['count']]
                    count_column_data = []
                    for i in count_column:
                        count_column_data.append(self.column_by_name(i)) #gives all the data-rows(as a list) of the i column
                    
                    count_column_data = [[count_column_data[i][j] for j in rows] for i in range(len(count_column))] #keep only the rows selected above in condition
                    group_by_column_data = self.column_by_name(group_by)
                    
                    group_data = list(sorted(set(group_by_column_data),key = group_by_column_data.index))
                    all_columns+=count_column

                    count =[0]*len(group_data)

                    for i in group_by_column_data:
                        for j in range(len(group_data)):
                            if i==group_data[j]:
                                count[j]+=1
                    
                    aggregate_all.append(count)
                aggregate_all.insert(0,group_data)
                
                dict = {(key):(zip(*aggregate_all) if key=="data" else value) for key,value in self.__dict__.items()}
                return_cols = [self.column_names.index(col.strip()) for col in all_columns]
    
                aggr_fun_col= []
                for key, value in aggregate_functions.items():
                    if value is not None:
                        for i in range(len(value)):
                            aggr_fun_col.append(key)
                aggr_fun_col.insert(0,"")
                
                dict['column_names'] = [aggr_fun_col[i]+"(" +self.column_names[j]+ ")" if i!=0 else self.column_names[j]for i,j in enumerate(return_cols)]
                dict['column_types'] = [None for i in return_cols]
                dict['pk_idx'] = None
                dict['pk'] = None
                    

        else:
            # top k rows
            # rows = rows[:int(top_k)] if isinstance(top_k,str) else rows
            # copy the old dict, but only the rows and columns of data with index in rows/columns (the indexes that we want returned)
            dict = {(key):([[self.data[i][j] for j in return_cols] for i in rows] if key=="data" else value) for key,value in self.__dict__.items()}
            #print(dict)
            # we need to set the new column names/types and no of columns, since we might
            # only return some columns
            dict['column_names'] = [ self.column_names[i] for i in return_cols]
            dict['column_types'] = [self.column_types[i] for i in return_cols]

        
        s_table = Table(load=dict) 
        if order_by:
            s_table.order_by(order_by, desc)
        if group_by and not found:
            #print(s_table.column_names)
            s_table.group_by(group_by)

        s_table.data = s_table.data[:int(top_k)] if isinstance(top_k,str) else s_table.data
        
        return s_table


    def _select_where_with_btree(self, return_columns, bt, condition,group_by=None, order_by=None, desc=True, top_k=None):

        # if * return all columns, else find the column indexes for the columns specified
        if return_columns == '*':
            return_cols = [i for i in range(len(self.column_names))]
        else:
            return_cols = [self.column_names.index(colname) for colname in return_columns]


        column_name, operator, value = self._parse_condition(condition)

        # if the column in condition is not a primary key, abort the select
        if column_name != self.column_names[self.pk_idx]:
            print('Column is not PK. Aborting')

        # here we run the same select twice, sequentially and using the btree.
        # we then check the results match and compare performance (number of operation)
        column = self.column_by_name(column_name)

        # sequential
        rows1 = []
        opsseq = 0
        for ind, x in enumerate(column):
            opsseq+=1
            if get_op(operator, x, value):
                rows1.append(ind)

        # btree find
        rows = bt.find(operator, value)

        # same as simple select from now on
        rows = rows[:top_k]
        # TODO: this needs to be dumbed down
        dict = {(key):([[self.data[i][j] for j in return_cols] for i in rows] if key=="data" else value) for key,value in self.__dict__.items()}

        dict['column_names'] = [self.column_names[i] for i in return_cols]
        dict['column_types']   = [self.column_types[i] for i in return_cols]

        s_table = Table(load=dict) 
        if order_by:
            s_table.order_by(order_by, desc)
        if group_by:
            s_table.group_by(group_by)

        s_table.data = s_table.data[:int(top_k)] if isinstance(top_k,str) else s_table.data

        return s_table

    def order_by(self, column_name, desc=True):
        '''
        Order table based on column.

        Args:
            column_name: string. Name of column.
            desc: boolean. If True, order_by will return results in descending order (False by default).
        '''
        column = self.column_by_name(column_name)
        idx = sorted(range(len(column)), key=lambda k: column[k], reverse=desc)
        self.data = [self.data[i] for i in idx]
        # self._update()



    def group_by(self,column_name):
        column = self.column_by_name(column_name)
        #remove duplicate elements 
        #print(column)
        elements= []
        positions=[]
        for idx, val in enumerate(column):
            if val not in elements:
                elements.append(val)
                positions.append(idx)
        #print(positions)
        self.data = [self.data[i] for i in positions]
        #self.data = [self.data[i] for i in range(0,len(res)]

    def _inner_join(self, table_right: Table, condition):
        '''
        Join table (left) with a supplied table (right) where condition is met.

        Args:
            condition: string. A condition using the following format:
                'column[<,<=,==,>=,>]value' or
                'value[<,<=,==,>=,>]column'.
                
                Operatores supported: (<,<=,==,>=,>)
        '''
        # get columns and operator
        column_name_left, operator, column_name_right = self._parse_condition(condition, join=True)
        # try to find both columns, if you fail raise error
        try:
            column_index_left = self.column_names.index(column_name_left)
        except:
            raise Exception(f'Column "{column_name_left}" dont exist in left table. Valid columns: {self.column_names}.')

        try:
            column_index_right = table_right.column_names.index(column_name_right)
        except:
            raise Exception(f'Column "{column_name_right}" dont exist in right table. Valid columns: {table_right.column_names}.')

        # get the column names of both tables with the table name in front
        # ex. for left -> name becomes left_table_name_name etc
        left_names = [f'{self._name}.{colname}' if self._name!='' else colname for colname in self.column_names]
        right_names = [f'{table_right._name}.{colname}' if table_right._name!='' else colname for colname in table_right.column_names]

        # define the new tables name, its column names and types
        join_table_name = ''
        join_table_colnames = left_names+right_names
        join_table_coltypes = self.column_types+table_right.column_types
        join_table = Table(name=join_table_name, column_names=join_table_colnames, column_types= join_table_coltypes)

        # count the number of operations (<,> etc)
        no_of_ops = 0
        # this code is dumb on purpose... it needs to illustrate the underline technique
        # for each value in left column and right column, if condition, append the corresponding row to the new table
        for row_left in self.data:
            left_value = row_left[column_index_left]
            for row_right in table_right.data:
                right_value = row_right[column_index_right]
                no_of_ops+=1
                if get_op(operator, left_value, right_value): #EQ_OP
                    join_table._insert(row_left+row_right)

        return join_table


    def show(self, no_of_rows=None, is_locked=False):
        '''
        Print the table in a nice readable format.

        Args:
            no_of_rows: int. Number of rows.
            is_locked: boolean. Whether it is locked (False by default).
        '''
        output = ""
        # if the table is locked, add locked keyword to title
        if is_locked:
            output += f"\n## {self._name} (locked) ##\n"
        else:
            output += f"\n## {self._name} ##\n"

        # headers -> "column name (column type)"
        #headers = [f'{col} ({tp.__name__})' for col, tp in zip(self.column_names, self.column_types)]
        headers = [f'{col} ({tp.__name__})' if tp is not None else f'{col}' for col, tp in zip(self.column_names, self.column_types)]
        if self.pk_idx is not None:
            # table has a primary key, add PK next to the appropriate column
            headers[self.pk_idx] = headers[self.pk_idx]+' #PK#'
        # detect the rows that are no tfull of nones (these rows have been deleted)
        # if we dont skip these rows, the returning table has empty rows at the deleted positions
        non_none_rows = [row for row in self.data if any(row)]
        # print using tabulate
        print(tabulate(non_none_rows[:no_of_rows], headers=headers)+'\n')


    def _parse_condition(self, condition, join=False):
        '''
        Parse the single string condition and return the value of the column and the operator.

        Args:
            condition: string. A condition using the following format:
                'column[<,<=,==,>=,>]value' or
                'value[<,<=,==,>=,>]column'.
                
                Operatores supported: (<,<=,==,>=,>)
            join: boolean. Whether to join or not (False by default).
        '''
        # if both_columns (used by the join function) return the names of the names of the columns (left first)
        if join:
            return split_condition(condition)

        # cast the value with the specified column's type and return the column name, the operator and the casted value
        left, op, right = split_condition(condition)
        if left not in self.column_names:
            raise ValueError(f'Condition is not valid (cant find column name)')
        coltype = self.column_types[self.column_names.index(left)]

        return left, op, coltype(right)


    def _load_from_file(self, filename):
        '''
        Load table from a pkl file (not used currently).

        Args:
            filename: string. Name of pkl file.
        '''
        f = open(filename, 'rb')
        tmp_dict = pickle.load(f)
        f.close()

        self.__dict__.update(tmp_dict)

    
