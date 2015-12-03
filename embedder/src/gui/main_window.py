#!/usr/bin/env python

# -----------------------------------
# Name: maiMain Window widget for embedder application
# Author: Jake Retallick
# Created: 2015.11.25
# Modified: 2015.11.25
# Licence: Copyright 2015
# -----------------------------------

from PyQt4 import QtGui, QtCore

import os

import gui_settings as settings
from qca_widget import QCAWidget
from chimera_widget import ChimeraWidget
from core.classes import Embedding


class MainWindow(QtGui.QMainWindow):
    '''Main Window widget for embedder application'''

    def __init__(self):
        '''Create the Main Window widget'''

        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        '''Initialise the UI'''

        # default parameters
        self.qca_dir = os.getcwd()
        self.embed_dir = os.getcwd()
        self.chimera_dir = os.getcwd()
        
        # functionality parameters
        
        self.chimera_file = ''      # relative path to chimera file
        self.qca_active = False     # True when QCAWidget set
        self.full_adj = True        # True when using full adjacency
        self.use_dense = True       # True if using Dense Placement embedder
        
        self.embeddings = {}        # list of embeddings
        self.active_embedding = -1  # index of active embedding
        self.embedding_count = 0    # next embedding index
        self.embedding_actions = {}  
        self.embedding_menus = {}

        # main window parameters
        geo = [settings.WIN_X0, settings.WIN_Y0,
               settings.WIN_DX, settings.WIN_DY]
        self.setGeometry(*geo)
        self.setWindowTitle('QCA Embedder')

        self.statusBar()

        # build the menu
        self.init_menubar()

        # build the toolbar
        self.init_toolbar()

        # set up the main layout
        hbox = QtGui.QHBoxLayout()

        # QCA widget placeholder
        self.qca_widget = QCAWidget(self)

        # Chimera widget
        self.chimera_widget = ChimeraWidget(self)
        self.chimera_file = os.path.relpath(settings.CHIMERA_DEFAULT_FILE)

        hbox.addWidget(self.qca_widget, stretch=4)
        hbox.addWidget(self.chimera_widget, stretch=4)

        main_widget = QtGui.QWidget(self)
        main_widget.setLayout(hbox)
        self.setCentralWidget(main_widget)

    def init_menubar(self):
        ''' '''

        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')
        tool_menu = menubar.addMenu('&Tools')
        menubar.addSeparator()
        self.embeddings_menu = menubar.addMenu('&Embeddings')
        self.embeddings_menu.setEnabled(False)

#        view_menu = menubar.addMenu('&View')
#        help_menu = menubar.addMenu('&Help')

        # construct actions

        qcaFileAction = QtGui.QAction(
            QtGui.QIcon(settings.ICO_DIR+'qca_file.png'),
            'Open QCA file...', self)
        qcaFileAction.triggered.connect(self.load_qca_file)

        embedFileAction = QtGui.QAction(
            QtGui.QIcon(settings.ICO_DIR+'open_embed.png'),
            'Open EMBED file...', self)
        embedFileAction.triggered.connect(self.load_embed_file)

        chimeraFileAction = QtGui.QAction(
            QtGui.QIcon(settings.ICO_DIR+'chimera_file.png'),
            'Open chimera file...', self)
        chimeraFileAction.triggered.connect(self.load_chimera_file)
        
        self.action_save_embedding = QtGui.QAction('Save active embedding...', self)
        self.action_save_embedding.triggered.connect(self.save_active_embedding)
        self.action_save_embedding.setEnabled(False)
        
        self.action_save_all = QtGui.QAction('Save EMBED file...', self)
        self.action_save_all.triggered.connect(self.save_all_embeddings)
        self.action_save_all.setEnabled(False)
        
        self.action_export_coefs = QtGui.QAction('Export coef file...', self)
        self.action_export_coefs.triggered.connect(self.export_coefs)
        self.action_export_coefs.setEnabled(False)

        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+W')
        exitAction.triggered.connect(self.close)
        
        self.action_dense_embed_flag = QtGui.QAction('Dense', self)
        self.action_dense_embed_flag.triggered.connect(self.switch_embedder)
        self.action_dense_embed_flag.setEnabled(False)
        
        self.action_heur_embed_flag = QtGui.QAction('Heuristic', self)
        self.action_heur_embed_flag.triggered.connect(self.switch_embedder)
        self.action_heur_embed_flag.setEnabled(True)

        file_menu.addAction(qcaFileAction)
        file_menu.addAction(embedFileAction)
        file_menu.addAction(chimeraFileAction)
        file_menu.addSeparator()
        file_menu.addAction(self.action_save_embedding)
        file_menu.addAction(self.action_save_all)
        file_menu.addAction(self.action_export_coefs)
        file_menu.addSeparator()
        file_menu.addAction(exitAction)

        embedder_menu = tool_menu.addMenu('Embedding method')
        embedder_menu.addAction(self.action_dense_embed_flag)
        embedder_menu.addAction(self.action_heur_embed_flag)

    def init_toolbar(self):
        ''' '''

        toolbar = QtGui.QToolBar()
        toolbar.setIconSize(QtCore.QSize(settings.ICO_SIZE, settings.ICO_SIZE))
        self.addToolBar(QtCore.Qt.LeftToolBarArea, toolbar)

        # construct actions
        action_qca_file = QtGui.QAction(self)
        action_qca_file.setIcon(
            QtGui.QIcon(settings.ICO_DIR+'qca_file.png'))
        action_qca_file.setStatusTip('Open QCA file...')
        action_qca_file.triggered.connect(self.load_qca_file)

        action_embed_file = QtGui.QAction(self)
        action_embed_file.setIcon(
            QtGui.QIcon(settings.ICO_DIR+'embed_file.png'))
        action_embed_file.setStatusTip('Open embedding file...')
        action_embed_file.triggered.connect(self.load_embed_file)

        action_chimera_file = QtGui.QAction(self)
        action_chimera_file.setIcon(
            QtGui.QIcon(settings.ICO_DIR+'chimera_file.png'))
        action_chimera_file.setStatusTip('Open chimera file...')
        action_chimera_file.triggered.connect(self.load_chimera_file)
        
        self.action_switch_adj = QtGui.QAction(self)
        self.action_switch_adj.setIcon(
            QtGui.QIcon(settings.ICO_DIR+'lim_adj.png'))
        self.action_switch_adj.setStatusTip('Switch to Limited Adjacency...')
        self.action_switch_adj.triggered.connect(self.switch_adjacency)
        self.action_switch_adj.setEnabled(False)
        
        self.action_embed = QtGui.QAction(self)
        self.action_embed.setIcon(
            QtGui.QIcon(settings.ICO_DIR+'embed.png'))
        self.action_embed.setStatusTip('Embed diplayed circuit...')
        self.action_embed.triggered.connect(self.embed_circuit)
        self.action_embed.setEnabled(False)
        
        self.action_del_embed = QtGui.QAction(self)
        self.action_del_embed.setIcon(
            QtGui.QIcon(settings.ICO_DIR+'del-embed.png'))
        self.action_del_embed.setStatusTip('Delete active embedding...')
        self.action_del_embed.triggered.connect(self.removeEmbedding)
        self.action_del_embed.setEnabled(False)

        toolbar.addAction(action_qca_file)
#        toolbar.addAction(action_embed_file)
        toolbar.addAction(action_chimera_file)
        toolbar.addAction(self.action_switch_adj)
        toolbar.addAction(self.action_embed)
        toolbar.addAction(self.action_del_embed)
        
    def reset(self):
        '''Delete all embedding and reset counters'''
        
        for ind in self.embeddings:
            self.active_embedding = ind
            self.removeEmbedding()
        self.active_embedding = -1
        self.embedding_count = 0
        
    def switch_adjacency(self):
        ''' '''
        if self.qca_active:
            self.full_adj = not self.full_adj
            ico_file = 'lim_adj.png' if self.full_adj else 'full_adj.png'
            sub_message = 'Limited' if self.full_adj else 'Full'
            self.action_switch_adj.setIcon(
                QtGui.QIcon(settings.ICO_DIR+ico_file))
            self.action_switch_adj.setStatusTip(
                'Switch to {0} Adjacency...'.format(sub_message))
            self.qca_widget.setAdjacency(self.full_adj)
        
    def switch_embedder(self):
        '''Change between embedding algorithms and set menu enabling'''
        
        self.action_dense_embed_flag.setEnabled(self.use_dense)
        self.action_heur_embed_flag.setEnabled(not self.use_dense)
        self.use_dense = not self.use_dense
        
    def embed_circuit(self):
        '''Run embedding on displayed circuit into selected chimera 
        sub-graph'''
        
        print('Running embedding...')

        try:        
            # get chimera sub-graph
            M, N, chimera_adj, active_range = self.chimera_widget.getActiveGraph()
            
            # get qca parameters
            J, cells = self.qca_widget.prepareCircuit()
            
            # embedding object
            embedding = Embedding(self.qca_widget.filename)
            embedding.set_embedder(self.use_dense)
            embedding.set_chimera(chimera_adj, active_range, M, N)
            embedding.set_qca(J, cells, self.full_adj)
            
            # run embedding
            try:
                embedding.run_embedding()
            except Exception as e:
                if type(e).__name__ == 'KeyboardInterrupt':
                    print('Embedding interrupted...')
                return
        except:
            print('\nUnexpected crash in embedding... possible disjoint graph')
            return

        if embedding.good:
            self.addEmbedding(embedding)
        else:
            print('Embedding failed...')

    def addEmbedding(self, embedding):
        '''Add an embedding object'''
        
        # enable relevant actions
        if len(self.embeddings) == 0:
            self.embeddings_menu.setEnabled(True)
            self.action_save_all.setEnabled(True)
            self.action_export_coefs.setEnabled(True)

        # get label for embedding in embedding menu
        label = os.path.basename(embedding.qca_file)
    
        # create new sub-menu if needed
        if label not in self.embedding_menus:
            self.embedding_menus[label] = self.embeddings_menu.addMenu(label)
        
        # create action for menu
        ind = int(self.embedding_count)
        func = lambda: self.switchEmbedding(ind)
        action = QtGui.QAction(str(self.embedding_count), self)
        action.triggered.connect(func)
        
        # add action to sub-menu
        self.embedding_menus[label].addAction(action)
        
        # store action for access/deletion
        self.embedding_actions[self.embedding_count] = action
        
        # add embedding to list of embeddings
        self.embeddings[self.embedding_count] = embedding
        
        # add embedding to chimera
        self.chimera_widget.addEmbedding(embedding, self.embedding_count)

        # set as active embedding
        self.switchEmbedding(ind)

        # update embedding_count
        self.embedding_count += 1
        
    def removeEmbedding(self):
        ''' '''
        
        if self.active_embedding == -1:
            return
        
        ind = self.active_embedding
        
        if ind not in self.embeddings:
            print('Attempted to delete a non-existing embedding...')
            return

        # special case if active embedding
        if ind == self.active_embedding:
            self.active_embedding = -1
            self.action_del_embed.setEnabled(False)
        
        embedding = self.embeddings.pop(ind)
        label = os.path.basename(embedding.qca_file)
        
        # clean nodes of embedding
        self.chimera_widget.resetNodes(embedding)
        
        # delete embedding object
        del(embedding)
        
        # delete action from sub-menu
        self.embedding_menus[label].removeAction(self.embedding_actions[ind])
        
        # delete action
        self.embedding_actions.pop(ind)
        
        # delete sub-menu if no more elements
        if self.embedding_menus[label].isEmpty():
            menu_action = self.embedding_menus[label].menuAction()
            self.embeddings_menu.removeAction(menu_action)
            self.embedding_menus.pop(label)
        
        # disable embeddings_menu if no embeddings
        if len(self.embeddings) == 0:
            self.action_save_all.setEnabled(False)
            self.action_export_coefs.setEnabled(False)
            self.embeddings_menu.setEnabled(False)

    def switchEmbedding(self, ind, color=True):
        '''Switch active embedding'''

        if ind in self.embeddings:
            # reanable embedding action
            if self.active_embedding != -1:
                self.embedding_actions[self.active_embedding].setEnabled(True)
            else:
                self.action_save_embedding.setEnabled(True)
            
            # allow deletion of active embedding
            self.action_del_embed.setEnabled(True)

            # disable new active embedding action
            self.embedding_actions[ind].setEnabled(False)
            
            # update active embedding
            self.active_embedding = ind
            self.qca_widget.updateCircuit(self.embeddings[ind].qca_file,
                                          self.embeddings[ind].full_adj)
            if self.embeddings[ind].full_adj != self.full_adj:
                self.switch_adjacency()
            if self.embeddings[ind].use_dense != self.use_dense:
                self.switch_embedder()
            
            # default coloring
            if color:
                # color nodes, no cell selected (assume no -1 cell)
                self.chimera_widget.selectNodes(self.embeddings[ind], -1)

    # FILE IO
    
    def create_embed_file(self, fname):
        '''Create an info file for all current embeddings'''
        
        try:
            fp = open(fname, 'w')
        except:
            print('Failed to open file: {0}'.format(fp))
            raise IOError
        
        # header
        chim_file = os.path.relpath(self.chimera_file, os.path.dirname(fname))
        fp.write('chimera_file: {0}\n\n'.format(chim_file))

        # embedding files
        for ind in self.embeddings:
            fp.write('{0}: {0}.txt\n'.format(ind))
        
        fp.close()
        
    def save_active_embedding(self):
        '''save the active embedding'''
        
        if self.active_embedding == -1:
            print('Trying to save nothing....should not have happened')
            return
        
        fname = str(QtGui.QFileDialog.getSaveFileName(
            self, 'Save active embedding', self.embed_dir))
        
        if not fname:
            return

        embedding = self.embeddings[self.active_embedding]
        self.save_embedding(embedding, fname)
    
    def save_embedding(self, embedding, fname):
        '''Save a single embedding to file'''
        
        try:
            fp = open(fname, 'w')
        except:
            print('Failed to open file: {0}'.format(fp))
            raise IOError
        
        # chimera file
        chim_file = os.path.relpath(self.chimera_file, os.path.dirname(fname))
        fp.write('chimera_file: {0}\n'.format(chim_file))

        # qca file
        qca_file = os.path.relpath(embedding.qca_file, os.path.dirname(fname))
        fp.write('qca_file: {0}\n\n'.format(qca_file))
        
        # adjacency and embedding type
        fp.write('full_adj: {0}\n'.format(embedding.full_adj))
        fp.write('use_dense: {0}\n\n'.format(embedding.use_dense))
        
        # chimera parameters
        fp.write('M: {0}\n'.format(embedding.M))
        fp.write('N: {0}\n'.format(embedding.N))
        fp.write('L: {0}\n'.format(embedding.L))
        fp.write('M0: {0}\n'.format(embedding.active_range['M'][0]))
        fp.write('N0: {0}\n\n'.format(embedding.active_range['N'][0]))
        
        # cell models
        for cell in embedding.models:
            fp.write('{0}: {1}\n'.format(cell,
                     ';'.join(str(qb) for qb in embedding.models[cell])))
        
        fp.close()
    
    def save_all_embeddings(self):
        '''Save all embeddings to a directory with an embed (summary) file'''
        
        # prompt for directory name
        dir_name = str(QtGui.QFileDialog.getExistingDirectory(
            self, 'Create/Select empty directory...', self.embed_dir))
        
        if not dir_name:
            return

        # convert to standard form
        dir_name = os.path.join(os.path.normpath(dir_name), '')
        
        # update embed home directory
        self.embed_dir = dir_name
        
        # if directory does not exist, create it
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # if files exist in directory, prompt user
        files = [f for f in os.listdir(dir_name)\
            if os.path.isfile(os.path.join(dir_name, f))]

        if len(files) > 0:
            reply = QtGui.QMessageBox.question(self, 'Message',
            'This directory already contain content that will be deleted. Do\
            you want to continue?',
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Cancel)
        
            if reply == QtGui.QMessageBox.Yes:
                for f in files:
                    os.remove(os.path.join(dir_name, f))
            else:
                return
        
        try:
            # create embed file
            self.create_embed_file(os.path.join(dir_name, 'summary.embed'))
            
            # save each embedding
            for ind in self.embeddings:
                fname = os.path.join(dir_name, '{0}.txt'.format(ind))
                self.save_embedding(self.embeddings[ind], fname)
        except IOError:
            print('Failed to save embeddings...')
            return
        
    def load_embedding(self, fname):
        ''' '''
        
        # create embedding
        embedding = Embedding()
        try:
            embedding.from_file(fname, self.chimera_file)
        except:
            print('Failed to load embedding')
            return
        
        self.addEmbedding(embedding)
    
    def load_embed_file(self):
        '''Prompt filename for embed file'''

        fname = str(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Embedding File', self.embed_dir,
                filter='EMBED (*.embed);; All files (*)'))

        if not fname:
            return

        # update embed home directory
        fdir = os.path.dirname(fname)
        self.embed_dir = fdir
        
        try:
            fp = open(fname, 'r')
        except:
            print('Failed to open file: {0}'.format(fname))
            return None
        
        # parse file
        info = {}
        inds = []
        for line in fp:
            if '#' in line or len(line)<3:
                continue
            key, data = [x.strip() for x in line.split(':')]
            info[key] = data
            if key.isdigit():
                inds.append(int(key))
        fp.close()
        
        # delete all embeddings
        self.reset()
        ndir = os.path.dirname(fname)
        chim_file = os.path.normpath(os.path.join(ndir, info['chimera_file']))
        self.chimera_widget.updateChimera(chim_file)
        
        for ind in inds:
            ndir = os.path.dirname(fname)
            fn = os.path.normpath(os.path.join(ndir, info[str(ind)]))
            self.load_embedding(fn)
        
        if not self.qca_active:
            self.qca_active = True
            self.action_embed.setEnabled(True)
            self.action_switch_adj.setEnabled(True)
    
    def load_qca_file(self):
        '''Prompt filename for qca file'''

        fname = str(QtGui.QFileDialog.getOpenFileName(
            self, 'Select QCA File', self.qca_dir))
            
        if not fname:
            return

        # update qca home directory
        fdir = os.path.dirname(fname)
        self.qca_dir = fdir

        self.qca_widget.updateCircuit(fname, self.full_adj)
        
        # disable old embedding
        self.chimera_widget.unclickNodes()
        if self.active_embedding != -1:
            self.embedding_actions[self.active_embedding].setEnabled(True)
        self.active_embedding = -1
        self.action_save_embedding.setEnabled(False)
        
        if not self.qca_active:
            self.qca_active = True
            self.action_embed.setEnabled(True)
            self.action_switch_adj.setEnabled(True)

    def load_chimera_file(self):
        '''Prompt filename for chimera structure'''

        fname = str(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Chimera File', self.chimera_dir))

        if not fname:
            return

        # update chimera home directory
        fdir = os.path.dirname(fname)
        self.chimera_dir = fdir

        self.chimera_widget.updateChimera(fname)
        self.chimera_file = os.path.relpath(fname)

    def export_coefs(self):
        '''Determine the smallest set of files which need to be produced to
        allow for all unique input combinations to all independent embeddings.
        Save each to a file'''
        pass

    # EVENT HANDLING

    def closeEvent(self, e):
        '''Handle main window close event'''

        reply = QtGui.QMessageBox.question(
            self, 'Message', 'Are you sure you want to quit?',
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Cancel)

        if reply == QtGui.QMessageBox.Yes:
            e.accept()
        else:
            e.ignore()
