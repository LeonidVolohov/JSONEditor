from PyQt5.QtCore import QSortFilterProxyModel


class QSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(QSortFilterProxyModel, self).__init__(parent)
        self.__showAllChildren = False

    def showAllChildren(self):
        return self.__showAllChildren

    def setShowAllChildren(self, showAllChildren):
        if showAllChildren == self.__showAllChildren:
            return
        self.__showAllChildren = showAllChildren
        self.invalidateFilter()

    def filterAcceptsRow (self, source_row, source_parent ):
        if self.filterRegExp() == "":
            return True

        if  super(QSortFilterProxyModel, self).filterAcceptsRow( source_row, source_parent) :
            return True

        source_index = self.sourceModel().index(source_row, 0, source_parent)
        for i in range( self.sourceModel().rowCount(source_index)):
            if self.filterAcceptsRow(i, source_index):
                return True

        return False
