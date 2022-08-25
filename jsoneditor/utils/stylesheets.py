APPLICATION_STYLESHEET = """
    QHeaderView::section {
        /* background-color: #678DB2; */
        color: black;
        height: 28px;
        font-size: 16px;
        font-family: courier;
    }

    QScrollBar:vertical {
        width:12px;
        background:#E7EFFC;
        margin:0px,0px,0px,0px;
        padding-top:12px;
        padding-bottom:12px;
    }
    QScrollBar::handle:vertical {
        width:16px;
        background:#678DB2;
        border-radius:32px;
        min-height:20;
    }
    QScrollBar::handle:vertical:hover {
        width:12px;
        background:#778FF3;
        border-radius:4px;
        min-height:20;
    }
"""

QTREEVIEW_STYLESHEET = """
    QTreeView {
        border: 3px solid;
        border-color: #678DB2;
        /*alternate-background-color: yellow;
        show-decoration-selected: 100; */
        background: #FFFFFF;
    }

    /* QTreeView::item {
        border: 1px solid #D9D9D9;
        border-top-color: transparent;
        border-bottom-color: transparent;
        border-left-color: transparent;
    } */  
    
    QTreeView::item:children {
        height: 28px;
    }

    QTreeView::item:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E5F3FF, stop: 1 #E5F3FF);
        border: 1px solid #bfcde4;
    }

    QTreeView::item:selected {
        border: 1px solid #678DB2;
        color: #000000;
    }

    QTreeView::item:selected:active{
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #CCE8FF, stop: 1 #CCE8FF);
    }

    /*
    QTreeView::branch {
        background-color: white;
    } */
    
    /*
    QTreeView::branch:closed:has-children {
        image: url("utils/images/treeview/branch-closed.png");
    }

    QTreeView::branch:has-siblings:!adjoins-item {
        border-image: url("utils/images/treeview/vline.png") 0;
    }

    QTreeView::branch:has-siblings:adjoins-item {
        border-image: url("utils/images/treeview/branch-more.png") 0;
    }

    QTreeView::branch:!has-children:!has-siblings:adjoins-item {
        border-image: url("utils/images/treeview/branch-end.png") 0;
    }

    QTreeView::branch:has-children:!has-siblings:closed,
    QTreeView::branch:closed:has-children:has-siblings {
        border-image: none;
        image: url("utils/images/treeview/branch-closed.png)";
    }

    QTreeView::branch:open:has-children:!has-siblings,
    QTreeView::branch:open:has-children:has-siblings  {
        border-image: none;
        image: url("utils/images/treeview/branch-open.png");
    } 
    */
"""
