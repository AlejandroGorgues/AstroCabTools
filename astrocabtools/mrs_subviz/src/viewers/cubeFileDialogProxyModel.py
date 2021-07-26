from PyQt5.QtCore import Qt,QIdentityProxyModel

__all__ = ['ProxyModel']

class ProxyModel(QIdentityProxyModel):
    """ Proxy class that alter the way the list widget will apear to not
    allow to select files
    """
    def flags(self, index):
        flags = super(ProxyModel, self).flags(index)
        if not self.sourceModel().isDir(index):
            flags &= ~Qt.ItemIsEnabled

        return flags
