import hashlib
import switchMode as switch

class main():
    def __init__(self):
        #self.godGuide2 = {}
        self.godGuide = {'avl': {}, 'b': {}, 'bplus': {}, 'dict': {}, 'isam': {}, 'json': {}, 'hash': {}}
        self.guiaModos = {}
        self.fk = {}
        self.Betzy = {}
        self.index = {}
        self.listMode = ['avl', 'hash', 'b', 'bplus', 'dict', 'isam', 'json']
        self.listEncoding = ['ascii', 'iso-8859-1', 'utf8']

    #---------------------FUNCIONES DE UNIFICACION DE MODOS DE ALMACENAMIENTO----------------------#

    # CREAR BASE DE DATOS

    def createDatabase(self, database, mode, encoding='ascii'):
        if self.identify(str(database)):
            if self.verifyMode(mode):
                if not self.searchDB2(database):
                    if self.verifyEncoding(encoding):
                        try:
                            self.godGuide[mode][database] = [{}, encoding]
                            self.guiaModos[database] = mode
                            switch.switchMode(mode).createDatabase(database)
                            return 0
                        except:
                            return 1
                    return 4
                return 2
            return 3
        return 1

    # ---------------------FUNCIONES DE ADMINISTRACION DEL MODO DE ALMACENAMIENTO----------------------#

    # CAMBIA EL MODO DE UNA TABLA

    def alterTableMode(self, database, table, mode):
        if self.identify(str(database)):
            if self.verifyMode(mode):
                if self.searchDB2(database):
                    if self.searchTB(database, table):
                        try:
                            if database in switch.switchMode(mode).showDatabases():
                                if table not in switch.switchMode(mode).showTables(database):
                                    for i in self.listMode:
                                        if database in self.godGuide[i].keys():
                                            if table in self.godGuide[i][database][0].keys():
                                                lis = self.godGuide[i][database][0].pop(table)
                                    self.godGuide[mode][database][0][table] = lis
                                    tabla = self.extTB(database, table)
                                    self.delTB(database, table)
                                    switch.switchMode(mode).createTable(database, table, lis[0])
                                    for i in tabla:
                                        switch.switchMode(mode).insert(database, table, i)
                                else:
                                    return 1
                            else:
                                for i in self.listMode:
                                    if database in self.godGuide[i].keys():
                                        if table in self.godGuide[i][database][0].keys():
                                            encoding = self.godGuide[i][database][1]
                                            lis = self.godGuide[i][database][0].pop(table)
                                self.godGuide[mode][database] = [{}, encoding]
                                self.godGuide[mode][database][0][table] = lis

                                #self.createDatabase(database, mode, encoding)
                                switch.switchMode(mode).createDatabase(database)
                                tabla = self.extTB(database, table)
                                self.delTB(database, table)
                                switch.switchMode(mode).createTable(database, table, lis[0])
                                for i in tabla:
                                    switch.switchMode(mode).insert(database, table, i)
                            return 0
                        except:
                            return 1
                    return 3
                return 2
            return 4
        return 1

    # CAMBIA EL MODO DE UNA BASE DE DATOS

    def alterDatabaseMode(self, database, mode):
        if self.identify(str(database)):
            if self.verifyMode(mode):
                if self.searchDB2(database):
                    try:
                        for i in self.listMode:
                            if i != mode:
                                if database in switch.switchMode(i).showDatabases():
                                    if len(switch.switchMode(i).showTables(database)) == 0:
                                        modoA = i
                                        lis = self.godGuide[modoA].pop(database)
                                        self.guiaModos[database] = mode
                                        self.godGuide[mode][database] = lis
                                        #self.createDatabase(database, mode, lis[1])
                                        switch.switchMode(mode).createDatabase(database)
                                    else:
                                        modoA = i
                                        self.guiaModos[database] = mode
                                        for j in switch.switchMode(i).showTables(database):
                                            self.alterTableMode(database, j, mode)
                                        self.godGuide[modoA].pop(database)
                                        #self.godGuide[mode][database] = lis
                                    switch.switchMode(i).dropDatabase(database)
                        return 0
                    except:
                        return 1
                return 2
            return 4
        return 1

    # ---------------------FUNCIONES DE ADMINISTRACION DE INDICES----------------------#

    # AGREGAR LISTA DE LLAVES FORANEAS A UNA TABLA

    def alterTableAddFK(self, database, table, indexName, columns,  tableRef, columnsRef):
        try:
            if table == tableRef:
                return 1
            c1 = 0
            c2 = 0
            clave = False
            for i in self.listMode:
                if self.searchDB(database,i):
                    clave = True
            if clave:
                if self.searchTB(database,table) and self.searchTB(database,tableRef):
                    if len(columnsRef)>= 1 and len(columns)>= 1:
                        if len(columnsRef)==len(columns):
                            c1 = self.getNumColumns(database,table)
                            c2 = self.getNumColumns(database,table)                      
                            for a in columns:
                                if a>c1 or a<0:
                                    return 5
                            for c in columnsRef:
                                if c>c2 or a<0:
                                    return 5
                            if database not in self.fk.keys():
                                self.fk[database] = {table:{indexName:[columns,columnsRef,tableRef]}}
                            elif table not in self.fk[database].keys():
                                self.fk[database][table] ={indexName: [columns,columnsRef,tableRef]} 
                            elif indexName not in self.fk[database][table].keys():
                                self.fk[database][table][indexName] = [columns,columnsRef,tableRef]
                            else:
                                return 1
                            return 0
                        else:
                            return 4
                    else:
                        return 4
                else:
                    return 3
            else:
                return 2
        except:
            return 1
    
    # ELIMINAR LLAVES FORANEAS A UNA TABLA

    def alterTableDropFK(self,database, table, indexName):
        try:
            clave = False
            for i in self.listMode:
                if self.searchDB(database,i):
                    clave = True
            if clave:
                if self.searchTB(database,table):
                    if database in self.fk.keys():
                        if table in self.fk[database].keys():
                            if indexName in self.fk[database][table].keys():
                                self.fk[database][table].pop(indexName)
                                return 0
                    return 4
                return 3
            else:
                return 2
        except:
            return 1
    
    # AGREGAR UN IDENTIFICADOR UNICO A UNA TABLA

    def alterTableAddUnique(self, database, table, indexName, columns):
        try:
            clave = False
            for i in self.listMode:
                if self.searchDB(database,i):
                    clave = True
            if clave:
                if self.searchTB(database,table):
                    c1 = self.getNumColumns(database,table)
                    for i in columns:
                        if i > c1 or i < 0:
                            return 5                  
                    if database not in self.Betzy.keys():
                        self.Betzy[database] = {table:{indexName:[columns]}}
                    elif table not in self.Betzy[database].keys():
                        self.Betzy[database][table] ={indexName: [columns]} 
                    elif indexName not in self.Betzy[database][table].keys():
                        self.Betzy[database][table][indexName] = [columns]
                    else:
                        return 1
                    return 0
                return 3
            else:
                return 2
        except:
            return 1
    
    # ELIMINAR EL INDENTIFICADOR UNICO A UNA TABLA

    def alterTableDropUnique(self, database, table, indexName):
        try:
            clave = False
            for i in self.listMode:
                if self.searchDB(database,i):
                    clave = True
            if clave:
                if self.searchTB(database,table):
                    if database in self.Betzy.keys():
                        if table in self.Betzy[database].keys():
                            if indexName in self.Betzy[database][table].keys():
                                self.Betzy[database][table].pop(indexName)
                                return 0
                    return 4
                return 3
            else:
                return 2
        except:
            return 1

    # AGREGAR UN INDICE A UNA TABLA

    def alterTableAddIndex(self, database, table, indexName, columns):
        try:
            clave = False
            for i in self.listMode:
                if self.searchDB(database,i):
                    clave = True
            if clave:
                if self.searchTB(database,table):
                    c1 = self.getNumColumns(database,table)
                    for i in columns:
                        if i > c1 or i < 0:
                            return 5
                    if database not in self.index.keys():
                        self.index[database] = {table:{indexName:columns}}
                        return 0
                    elif table not in self.index[database].keys():
                        self.index[database][table] = {indexName:columns}
                    elif indexName not in self.index[database][table].keys():
                        self.index[database][table][indexName] = [columns]
                    else:
                        return 1
                    return 0                  
                return 3
            else:
                return 2
        except:
            return 1

    # ELIMINAR UN INDICE A UNA TABLA
    
    def alterTableDropIndex(self, database, table, indexName):
        try:
            clave = False
            for i in self.listMode:
                if self.searchDB(database,i):
                    clave = True
            if clave:
                if self.searchTB(database,table):
                    if database in self.index.keys():
                        if table in self.index[database].keys():
                            if indexName in self.index[database][table].keys():
                                self.index[database][table].pop(indexName)
                                return 0
                    return 4
                return 3
            else:
                return 2
        except:
            return 1

    # ---------------------FUNCIONES DE ADMINISTRACION DE LA CODIFICACION----------------------#

    def alterDatabaseEncoding(self, dataBase, codi):
        try:
            if codi == '' or codi == None:
                codi = 'ascii'
            leLlave = []
            for i in self.listMode: #para saber si existe la base
                if self.searchDB(dataBase, i):
                    if self.verifyEncoding(codi):
                        tb = self.showTables(dataBase)
                        if tb != []: #saber si tiene o no tablas la base
                            for j in tb: #para cod los nombres de las tablas
                                tp = self.extractTable(dataBase, j) #jalar las tuplas
                                if tp != []: #para codificar tuplas
                                    llave = self.godGuide[i][dataBase][0][j][1]
                                    for k in range(0,len(tp)):
                                        leTP = []
                                        for l in tp[k]:
                                            #para saber si viene codificado ya
                                            if type(l) is bytes:
                                                x = l.decode(self.godGuide[i][dataBase][0][j][2])
                                                leTP += [str(x).encode(encoding= codi, errors= 'backslashreplace')]
                                            else:
                                                leTP += [str(l).encode(encoding= codi, errors= 'backslashreplace')]
                                        for h in llave:
                                            leLlave.append(tp[k][h])
                                        leNewtp = {}
                                        for n in range(0,len(leTP)):
                                            leNewtp[n] = leTP[n]
                                        self.update(dataBase,j,leNewtp,leLlave)
                                        leLlave = []
                        self.godGuide[i][dataBase][0][j][2] = codi
                        return 0
                    else:
                        return 3
            return 2
        except:
            return 1

    # ---------------------FUNCIONES DE GENERACION DEL CHECKSUM----------------------#

    # GENERA EL CHECKSUM DE TODAS LAS TABLAS DE UNA BASE DE DATOS

    def checksumDatabase(self, database, mode):
        modos = ['MD5', 'SHA256']
        tablas = self.showTables(database)
        tuplas = []
        tmp = ""
        try:
            if mode not in modos:
                return None
            for i in tablas:
                for j in self.extractTable(database, i):
                    tuplas.append(j)
            for i in tuplas:
                for j in i:
                    tmp += str(j)
            for i in self.listMode:
                if database in self.godGuide[i].keys():
                    encoding = self.godGuide[i][database][1]
            if mode == 'MD5':
                hash = hashlib.md5(tmp.encode(encoding))
            elif mode == 'SHA256':
                hash = hashlib.sha256(tmp.encode(encoding))
            hash = hash.hexdigest()
            print(tmp)
            return hash
        except:
            return None

    # GENERA EL CHECKSUM DE UNA TABLA EN ESPECIFICO

    def checksumTable(self, database, table, mode):
        modos = ['MD5', 'SHA256']
        tmp = ""
        try:
            if mode not in modos:
                return None
            for i in self.listMode:
                for j in self.godGuide[i].keys():
                    if table in self.godGuide[i][j][0].keys() and j == database:
                        encoding = self.godGuide[i][j][0][table][2]
            tuplas = self.extractTable(database, table)
            for i in tuplas:
                for j in i:
                    tmp += str(j)
            if mode == 'MD5':
                hash = hashlib.md5(tmp.encode(encoding))
            elif mode == 'SHA256':
                hash = hashlib.sha256(tmp.encode(encoding))
            hash = hash.hexdigest()
            print(tmp)
            return hash
        except:
            return None

    # ---------------------FUNCIONES DE COMPRESION DE DATOS----------------------#
    
    def alterDatabaseCompress(self, database, level):
        if self.identify(str(database)):
            if self.searchDB2(database):
                if level in range(0,10):
                    try:
                        for i in self.showTables(database):
                            self.alterTableCompress(database, i, level)
                        return 0
                    except:
                        return 1
                return 4
            return 2
        return 1

    def alterDatabaseDecompress(self, database):
        if self.identify(str(database)):
            if self.searchDB2(database):
                try:
                    for i in self.showTables(database):
                            self.alterTableDecompress(database, i)
                    return 0
                except:
                    return 1
            return 2
        return 1

    def alterTableCompress(self, database, table, level):
        if self.identify(str(database)):
            if self.searchDB2(database):
                if self.searchTB(database, table):
                    if level in range(0,10):
                        mode = ""
                        for i in self.listMode:
                            for j in switch.switchMode(i).showDatabases():
                                if table in switch.switchMode(i).showTables(j):
                                    mode = i
                        try:
                            if not self.godGuide[mode][database][0][table][3]:
                                tabla = self.extTB(database, table)

                                for i in tabla:
                                    registro = []
                                    n = 0
                                    for j in i:
                                        if type(j) is str and not j.isdigit():
                                            # if mode == "json":
                                            compress = zlib.compress(j.encode("utf-8"), level)
                                            registro.append(compress.hex())
                                            # else:    
                                                # registro.append(zlib.compress(j.encode("utf-8"), level))
                                        else:
                                            registro.append(int(j))
                                        n += 1
                                    
                                    pk = []
                                    for j in self.godGuide[mode][database][0][table][1]:
                                        pk.append(i[j])

                                    self.delete2(database, table, pk)
                                    self.insert2(database, table, registro)
                                    self.godGuide[mode][database][0][table][3] = True
                            return 0
                        except:
                            return 1
                    return 4
                return 3
            return 2
        return 1

    def alterTableDecompress(self, database, table):
        if self.identify(str(database)):
            if self.searchDB2(database):
                if self.searchTB(database, table):
                    mode = ""
                    for i in self.listMode:
                        for j in switch.switchMode(i).showDatabases():
                            if table in switch.switchMode(i).showTables(j):
                                mode = i
                    if self.godGuide[mode][database][0][table][3]:
                        try:
                            tabla = self.extTB(database, table)
                               
                            for i in tabla:
                                registro2 = []
                                for j in i:
                                    if type(j) is not str and str(j).isdigit():
                                        registro2.append(j)
                                    else:
                                        # if mode == "json":
                                        registro2.append( zlib.decompress(bytes.fromhex(j)).decode("utf-8"))
                                        # else:
                                            # registro2.append(zlib.decompress(j).decode("utf-8"))

                                pk = []
                                for j in self.godGuide[mode][database][0][table][1]:
                                    pk.append(i[j])

                                self.delete2(database, table, pk)
                                self.insert2(database, table, registro2)
                                self.godGuide[mode][database][0][table][3] = False
                            return 0
                        except:
                            return 1
                    return 3
                return 4
            return 2
        return 1
   
    # ---------------------FUNCIONES DE SEGURIDAD----------------------#

    # ---------------------FUNCIONES DE GRAFOS----------------------#

    #---------------------FUNCIONES BASES DE DATOS (ANTERIORES)----------------------#

    # LISTA DE BASES DE DATOS ALMACENADAS

    def showDatabases(self):
        re = []
        for i in self.listMode:
            re = re + switch.switchMode(i).showDatabases()
        return re

    # CAMBIAR NOMBRE DE UNA BASE DE DATOS

    def alterDatabase(self, databaseOld, databaseNew):
        re = 1
        for i in self.listMode:
            if self.searchDB(databaseOld, i):
                for i in self.listMode:
                    if not self.searchDB2(databaseNew):
                        re = switch.switchMode(i).alterDatabase(databaseOld, databaseNew)
        if re == 0:

            ward = self.guiaModos.pop(databaseOld)
            self.guiaModos[databaseNew] = ward

            for i in self.listMode:
                if databaseOld in self.godGuide[i].keys():
                    ward = self.godGuide[i].pop(databaseOld)
                    self.godGuide[i][databaseNew] = ward
        return re

    # ELIMINAR BASE DE DATOS

    def dropDatabase(self, database):
        re = 1
        for i in self.listMode:
            if self.searchDB(database, i):
                re = switch.switchMode(i).dropDatabase(database)
        if re == 0:
            self.guiaModos.pop(database)
            for i in self.listMode:
                if database in self.godGuide[i].keys():
                    self.godGuide[i].pop(database)
        return re

    # ---------------------FUNCIONES TABLAS----------------------#

    # CREAR TABLA EN UNA DETERMINADA BASE DE DATOS

    def createTable(self, database, table, numberColumns):
        re = switch.switchMode(self.guiaModos[database]).createTable(database, table, numberColumns)
        if re == 0:
            mod = self.guiaModos[database]
            self.godGuide[mod][database][0][table] = [numberColumns, None, self.godGuide[self.guiaModos[database]][database][1], False]
        return re

    # LISTA DE TABLAS AGREGADAS A UNA BASE DE DATOS

    def showTables(self, database):
        re = []
        for i in self.listMode:
            if self.searchDB(database, i):
                re = re + switch.switchMode(i).showTables(database)
        return re

    # LISTA DE REGISTROS DE UNA TABLA EN UN BASE DE DATOS

    def extractTable(self, database, table):
        re = []
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    re = re + switch.switchMode(i).extractTable(database, table)
        return re

    #LISTA REGISTROS EN UN RANGO DE UNA TABLA

    def extractRangeTable(self, database, table, columnNumber, lower, upper):
        re = []
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    re = re + switch.switchMode(i).extractRangeTable(database, table, columnNumber, lower, upper)
        return re

    # AGREGAR LISTA DE LLAVES PRIMARIAS A UNA TABLA

    def alterAddPK(self, database, table, columns):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    re = switch.switchMode(i).alterAddPK(database, table, columns)
        if re == 0:
            for i in self.listMode:
                for j in self.godGuide[i].keys():
                    if table in self.godGuide[i][j][0].keys() and j == database:
                        self.godGuide[i][j][0][table][1] = columns
        return re

    # ELIMINAR LAS LLAVES PRIMARIAS DE UNA TABLA

    def alterDropPK(self, database, table):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    re = switch.switchMode(i).alterDropPK(database, table)
        if re == 0:
            for i in self.listMode:
                for j in self.godGuide[i].keys():
                    if table in self.godGuide[i][j][0].keys() and j == database:
                        self.godGuide[i][j][0][table][1] = None
        return re

    # CAMBIAR EL NOMBRE DE UNA TABLA

    def alterTable(self, database, tableOld, tableNew):
        for i in self.listMode:
            if self.searchDB(database, i):
                if tableOld in switch.switchMode(i).showTables(database):
                    re = switch.switchMode(i).alterTable(database, tableOld, tableNew)
        if re == 0:
            for i in self.listMode:
                for j in self.godGuide[i].keys():
                    if tableOld in self.godGuide[i][j][0].keys() and j == database:
                        ward = self.godGuide[i][j][0].pop(tableOld)
                        self.godGuide[i][j][0][tableNew] = ward
        return re

    # AGREGAR UN NUEVO REGISTRO A LAS TABLAS EXISTENTES

    def alterAddColumn(self, database,  table, default):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    re = switch.switchMode(i).alterAddColumn(database, table, default)
        if re == 0:
            for i in self.listMode:
                for j in self.godGuide[i].keys():
                    if table in self.godGuide[i][j][0].keys() and j == database:
                        self.godGuide[i][j][0][table][0] += 1
        return re

    # ELIMINAR UNA COLUMNA ESPECIFICA DE UNA TABLA

    def alterDropColumn(self, database, table, columnNumber):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    re = switch.switchMode(i).alterDropColumn(database, table, columnNumber)
        if re == 0:
            for i in self.listMode:
                for j in self.godGuide[i].keys():
                    if table in self.godGuide[i][j][0].keys() and j == database:
                        self.godGuide[i][j][0][table][0] -= 1
        return re

    # ELIMINAR UNA TABLA DE LA BASE DE DATOS

    def dropTable(self, database, table):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    re = switch.switchMode(i).dropTable(database, table)
        if re == 0:
            for i in self.listMode:
                for j in self.godGuide[i].keys():
                    if table in self.godGuide[i][j][0].keys() and j == database:
                        self.godGuide[i][j][0].pop(table)
        return re

    # ---------------------FUNCIONES TUPLAS----------------------#

    # AÑADIR REGISTROS A UNA TABLA

    def insert(self, database, table, register):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    return switch.switchMode(i).insert(database, table, register)

    # CARGA DE REGISTROS MEDIANTE UN CSV

    def loadCSV(self, file, database, table):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    return switch.switchMode(i).loadCSV(file, database, table)

    # REGISTRO SEGUN LLAVE PRIMARIA

    def extractRow(self, database, table, columns):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    return switch.switchMode(i).extractRow(database, table, columns)

    # MODIFICA UN REGISTRO EN ESPECIFICO

    def update(self, database, table, register, columns):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    return switch.switchMode(i).update(database, table, register, columns)

    # ELIMINA UN REGISTRO EN ESPECIFICO

    def delete(self, database, table, columns):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    return switch.switchMode(i).delete(database, table, columns)

    # ELIMINA TODOS LOS REGISTROS DE UNA TABLA

    def truncate(self, database, table):
        for i in self.listMode:
            if self.searchDB(database, i):
                if table in switch.switchMode(i).showTables(database):
                    return switch.switchMode(i).truncate(database, table)

    # -------------------------UTILIDADES-------------------------#

    def identify(self, id):
        id = str(id)
        if id[0].isalpha():
            return True
        else:
            if id[0].isdigit():
                return False
        return False

    def verifyMode(self, mode):
        if mode in self.listMode:
            return True
        return False

    def verifyEncoding(self, encoding):
        if encoding in self.listEncoding:
            return True
        return False

    def searchDB(self, key, mode):
        if key in switch.switchMode(mode).showDatabases():
            return True
        return False

    def searchDB2(self, key):
        for i in self.listMode:
            if key in switch.switchMode(i).showDatabases():
                return True
        return False

    def searchTB(self, database, table):
        for i in self.listMode:
            for j in switch.switchMode(i).showDatabases():
                if table in switch.switchMode(i).showTables(j):
                        return True
        return False

    def extTB(self, database, table):
        for i in self.listMode:
            for j in switch.switchMode(i).showDatabases():
                if table in switch.switchMode(i).showTables(j):
                        return switch.switchMode(i).extractTable(j, table)
    def getNumColumns(self,database,table):
        for i in self.listMode:
            for j in self.godGuide[i].keys():
                if table in self.godGuide[i][j][0].keys() and j == database:
                    return self.godGuide[i][j][0][table][0]

    def getPK(self,database,table):
        for i in self.listMode:
            for j in self.godGuide[i].keys():
                if table in self.godGuide[i][j][0].keys() and j == database:
                    return self.godGuide[i][j][0][table][1]
        for i in self.listMode:
            for j in self.godGuide[i].keys():
                if table in self.godGuide[i][j][0].keys() and j == database:
                    return self.godGuide[i][j][0][table][0]
                      
    def delTB(self, database, table):
        for i in self.listMode:
            for j in switch.switchMode(i).showDatabases():
                if table in switch.switchMode(i).showTables(j):
                    switch.switchMode(i).dropTable(j, table)
                    return None

