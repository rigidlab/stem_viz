import logging
from bokeh.models import Circle, ColumnDataSource
from bokeh.models import Arrow, NormalHead, OpenHead, VeeHead
from bokeh.models import CustomJS, Slider, Label
from bokeh.layouts import column,row
from bokeh.plotting import figure, output_file
from bokeh.plotting import show as bokeh_show
from bokeh.models import SingleIntervalTicker

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.source=ColumnDataSource(dict(x=[self.x],y=[self.y],size=[1])) 
    def plot(self):
        g=Circle(x='x',y='y',size='size')
        return g 

class Vector:
    def __init__(self,start,end,color='black'):
        self.start=start
        self.end=end
        self.x_start=start.x
        self.x_end=end.x
        self.y_start=start.y
        self.y_end=end.y
        self.source=ColumnDataSource(dict(x_start=[self.x_start],
            x_end=[self.x_end],
            y_start=[self.y_start],
            y_end=[self.y_end])) 
        self.color=color

    def plot(self):
        v=Arrow(end=NormalHead(size=8),x_start='x_start',
                x_end='x_end',y_start='y_start',
                y_end='y_end',
                line_color=self.color,
                source=self.source)
        return v

class Plot: 
    def __init__(self,*args,**kwargs):
        self.figure=figure(*args,**kwargs)
        self.figure.circle(x=[0], y=[0], size=1,
            color=['black'], fill_alpha=0.1)
        self.figure.xaxis.ticker = SingleIntervalTicker(interval=1)
        self.figure.yaxis.ticker = SingleIntervalTicker(interval=1)


    def add(self,*args):
        if len(args)>1:
            for i in args:
                self.add(i)
        else:
            if isinstance(args[0],Vector):
                self.figure.add_layout(args[0].plot())
                self.figure.add_glyph(args[0].start.source,
                    args[0].start.plot())
                self.figure.add_glyph(args[0].end.source,
                    args[0].end.plot())
            if isinstance(args[0],Point):
                 self.figure.add_glyph(args[0].source,args[0].plot())

    def show(self):
        bokeh_show(self.figure)

output_file('rotation.html', title='Rotation example')
angle_slider = Slider(start=0.0, end=360, value=0, step=.1, title="Angle (degree)")

p=Plot(sizing_mode='stretch_width',match_aspect=True)
x_axis=Vector(Point(0,0),Point(1,0),color='red')
y_axis=Vector(Point(0,0),Point(0,1),color='green')
p.figure.circle(x=[0],y=[0],radius=[1],fill_color=None,line_color='black')

v1=Vector(Point(0,0),Point(1,0))
v2=Vector(Point(0,0),Point(0,1))
lx=Label(x=1,y=0,text='x')
ly=Label(x=0,y=1,text='y')
p.figure.add_layout(lx)
p.figure.add_layout(ly)

p.add(x_axis,y_axis,v1,v2,Point(-1,0),Point(0,-1))
callback = CustomJS(args=dict(source1=v1.source,
    source2=v2.source,
    angle_slider=angle_slider),
    code="""
    const data1 = source1.data;
    const data2 = source2.data;
    const angle = angle_slider.value;
    const x_start_1 = data1['x_start'];
    const x_end_1 = data1['x_end'];
    const y_start_1 = data1['y_start'];
    const y_end_1 = data1['y_end'];
    
    const x_end_2 = data2['x_end'];
    const y_end_2 = data2['y_end'];

    x_end_1[0] = Math.cos(angle*Math.PI/180);
    y_end_1[0] = Math.sin(angle*Math.PI/180);
    x_end_2[0] = -Math.sin(angle*Math.PI/180);
    y_end_2[0] = Math.cos(angle*Math.PI/180);

    source1.change.emit();
    source2.change.emit();
    """
)

angle_slider.js_on_change('value', callback)

layout=row(p.figure,angle_slider,sizing_mode='stretch_width')
bokeh_show(layout)
