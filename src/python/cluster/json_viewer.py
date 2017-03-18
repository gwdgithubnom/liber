class ClusterViwer:
    """
    用于配置ClusterViewer的Json视图
    """
    def __init__(self,name='undefine',type='cluster',large='true',symbol='circle',symbolSize=12,label='',data='',itemStyle=''):
        self.name = name
        self.type = type
        self.large = large
        self.symbol = symbol
        self.symbolSize = symbolSize
        self.lablel = label
        self.data = data
        self.itemStyle=itemStyle
