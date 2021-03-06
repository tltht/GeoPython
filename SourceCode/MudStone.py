
from CustomClass import *




class MudStone(AppForm, Tool):
    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    Tags = []

    Label = [u'Clay', u'Sand', u'Silt']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
                     (-13, -2),
                     (104, -1)]

    Labels = [u'Y',
              u'SY',
              u'TY',
              u'YS',
              u'STY',
              u'YT',
              u'S',
              u'TS',
              u'ST',
              u'T',
              '20',
              '40',
              '60',
              '80',

              '80',
              '60',
              '40',
              '20',

              '80',
              '60',
              '40',
              '20', ]

    Locations = [(10, 10, 80),
                 (40, 10, 50),
                 (10, 40, 50),
                 (50, 10, 40),
                 (30, 30, 30),
                 (10, 50, 40),
                 (80, 10, 10),
                 (60, 30, 10),
                 (40, 50, 10),
                 (10, 80, 10),

                 (20, 0, 80),
                 (40, 0, 60),
                 (60, 0, 40),
                 (80, 0, 20),

                 (20, 80, 0),
                 (40, 60, 0),
                 (60, 40, 0),
                 (80, 20, 0),

                 (0, 20, 80),
                 (0, 40, 60),
                 (0, 60, 40),
                 (0, 80, 20),
                 ]
    Offset = [(0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),

              (-18, 0),
              (-18, 0),
              (-18, 0),
              (-18, 0),

              (0, -18),
              (0, -18),
              (0, -18),
              (0, -18),

              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0), ]

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Sand-Silt-Clay')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Tri')

        self.create_main_frame()
        self.create_status_bar()

        self.raw = self._df
        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i],
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1],
                                                        self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1]))

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((15.0, 9.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Tri)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Tri)  # int

        self.Tag_cb = QCheckBox('&Tag')
        self.Tag_cb.setChecked(True)
        self.Tag_cb.stateChanged.connect(self.Tri)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.legend_cb, self.Tag_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Tri(self):

        self.axes.clear()
        self.axes.axis('off')
        self.axes.set_xlim(-15, 140)
        self.axes.set_ylim(-10, 100)

        s = [TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black',
                     Style='-',
                     Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        for i in range(len(self.LabelPosition)):
            self.axes.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                               textcoords='offset points',
                               fontsize=16, )
        # 20间隔点坐标：
        Gap20 = [(20, 0, 80),
                 (40, 0, 60),
                 (60, 0, 40),
                 (80, 0, 20),

                 (20, 80, 0),
                 (40, 60, 0),
                 (60, 40, 0),
                 (80, 20, 0),

                 (0, 80, 20),
                 (0, 60, 40),
                 (0, 40, 60),
                 (0, 20, 80)]

        # 二等分点坐标：
        Gap50 = [(50, 0, 50),
                 (40, 20, 40),

                 (0, 50, 50),
                 (20, 40, 40),

                 (50, 50, 0),
                 (40, 40, 20), ]

        # 四等分点坐标：
        Gap25 = [(25, 0, 75),
                 (0, 25, 75),

                 (75, 0, 25),
                 (75, 25, 0),

                 (25, 75, 0),
                 (0, 75, 25), ]

        # 中心三角坐标：
        Middle = [(20, 20, 60),
                  (60, 20, 20),
                  (20, 60, 20), ]

        # 中心三角垂直链接四等分线坐标：
        Other = [(12.5, 12.5, 75),
                 (75, 12.5, 12.5),
                 (12.5, 75, 12.5), ]

        tmp = []
        # 中心三角绘制
        tmp.append(
            TriLine(Points=[Middle[0], Middle[1], Middle[2], Middle[0]], Sort='', Width=1, Color='black', Style='-',
                    Alpha=0.7,
                    Label=''))

        # 二等分和四等分线条绘制
        for i in range(len(Gap50)):

            if i % 2 == 0:
                tmp.append(
                    TriLine(Points=[Gap50[i], Gap50[i + 1]], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                            Label=''))
                tmp.append(
                    TriLine(Points=[Gap25[i], Gap25[i + 1]], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                            Label=''))

        # 中心外延线条绘制
        for i in range(len(Middle)):
            tmp.append(TriLine(Points=[Middle[i], Other[i]], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                               Label=''))

        # 20网格线条绘制
        for i in range(len(Gap20)):
            if i <= len(Gap20) - 5:
                tmp.append(
                    TriLine(Points=[Gap20[i], Gap20[i + 4]], Sort='', Width=0.5, Color='grey', Style='-', Alpha=0.5,
                            Label=''))
            else:
                tmp.append(
                    TriLine(Points=[Gap20[i], Gap20[-1 - i]], Sort='', Width=0.5, Color='grey', Style='-', Alpha=0.5,
                            Label=''))

        for i in tmp:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        raw = self._df
        PointLabels = []
        TPoints = []
        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            TPoints.append(TriPoint((raw.at[i, 'sand'], raw.at[i, 'silt'], raw.at[i, 'clay']), Size=raw.at[i, 'Size'],
                                    Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                    Label=TmpLabel))


            # TPoints.append(TriPoint((raw.at[i, 'X'], raw.at[i, 'Y'], raw.at[i, 'Z']), Size=raw.at[i, 'Size'],
            #         Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
            #         Label=TmpLabel))

        for i in TPoints:
            self.axes.scatter(i.X, i.Y, marker=i.Marker, s=i.Size, color=i.Color, alpha=i.Alpha,
                              label=i.Label, edgecolors='black')

        if (self.Tag_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=i.FontSize, color='grey', alpha=0.8)

        if (self.legend_cb.isChecked()):
            # a = int(self.slider.value())
            # self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=4, prop=fontprop, bbox_to_anchor=(1.1, 0.5))

        self.canvas.draw()

        self.canvas.draw()

