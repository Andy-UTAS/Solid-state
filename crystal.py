#!/usr/bin/python


"""
Crystal.py: a program to make content for the crystals section of the course
"""

from SSP import *

"""
Basic functions
"""

# Produces the lattice to be fed into plotly
def lattice_generation(a1,a2,N = 10):
    grid = np.arange(-N//2,N//2,1)
    xGrid, yGrid = np.meshgrid(grid,grid)
    return np.reshape(np.kron(xGrid.flatten(),a1),(-1,2))+np.reshape(np.kron(yGrid.flatten(),a2),(-1,2))


# Produces the dotted lines of the unit cell
def dash_contour(a1,a2, vec_zero = np.array([0,0]), color='Red'):
    dotLine_a1 = np.transpose(np.array([a1,a1+a2])+vec_zero)
    dotLine_a2 = np.transpose(np.array([a2,a1+a2])+vec_zero)

    def dash_trace(vec,color):
        trace = go.Scatter(
            x=vec[0],
            y=vec[1],
            mode = 'lines',
            line_width = 2,
            line_color = color,
            line_dash='dot',
            visible=False
        )
        return trace

    return dash_trace(dotLine_a1,color),dash_trace(dotLine_a2,color)

# Makes the lattice vector arrow
def make_arrow(vec,text,color = 'Red',vec_zero = [0,0], text_shift = [-0.2,-0.1]):
    annot = [dict(
            x = vec[0],
            y = vec[1],
            ax = vec_zero[0],
            ay = vec_zero[1],
            xref = 'x',
            yref = 'y',
            axref = 'x',
            ayref = 'y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=3,
            arrowcolor = color
                 ),
         dict(
            x=(vec[0]+vec_zero[0])/2+text_shift[0],
            y=(vec[1]+vec_zero[1])/2+text_shift[1],
            xref='x',
            ayref = 'y',
            text = text,
            font = dict(
                color = color,
                size = 20
            ),
            showarrow=False,
             )
        ]
    return annot


"""
Crystal plots
"""

##################################################
# ################ simple lattice #################
# #################################################

def simple_lattice():
    # Define the lattice vectors
    a1 = np.array([1,0])
    a2 = np.array([0,1])
    a1_alt = -a1-a2
    a2_alt = a1_alt + a1
    a2_c = np.array([0,np.sqrt(3)])

    # Create the pattern
    pattern_points = lattice_generation(a1,a2)

    # Lattice Choice A
    latticeA = go.Scatter(visible = True,x=pattern_points.T[0],y=pattern_points.T[1],mode='markers',marker=dict(
            color = 'Black',
            size = 10,
            )
        )

    bt1_annot = make_arrow(a1,'') + make_arrow(a2,'',text_shift=[-0.3,-0.1], vec_zero = [0,-.1])
    # Button 2
    bt2_annot = make_arrow(a1,'') + make_arrow(a2,'',text_shift=[-0.3,-0.1], vec_zero = [0,-.1]) + make_arrow(a1_alt,'',color='Black',text_shift=[-0.6,-0.1]) + make_arrow(a2_alt,'',color='Black',text_shift=[-0.35,-0.1], vec_zero = [0,.1])


    # (0)  Button 1, (0, 1-5) Button 2, (0, 6-8) Button 3, (0,1,9,10)
    data = [latticeA, *dash_contour(a1,a2), *dash_contour(a1_alt,a2_alt,color='Black'),]


    updatemenus = list([
        dict(
            type="buttons",
            direction = "down",
            active=0,
            buttons=list([
                dict(label="A",
                     method="update",
                     args=[{"visible": [True, False, False, False, False,]},
                           {"title": "A 2D lattice",
                            "annotations": []}]),
                dict(label="B",
                     method="update",
                     args=[{"visible": [True, True, True, False, False,]},
                           {"title": "A 2D lattice with a primitive unit cell",
                            "annotations": bt1_annot}]),
                dict(label="C",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, ]},
                           {"title": "A 2D lattice with two (different) primitive unit cells",
                            "annotations": bt2_annot}]),
            ]),
        )
    ]
    )

    # Setting axis to invisible
    plot_range = 2.1
    axis = dict(
            range=[-plot_range,plot_range],
            visible = False,
            showgrid = False,
            fixedrange = True
        )

    # Figure propeties
    layout = dict(
        showlegend = False,
        updatemenus = updatemenus,
        plot_bgcolor = 'rgb(254, 254, 254)',
        width = 600,
        height = 600,
        xaxis = axis,
        yaxis = axis
    )

    # Displaying the figure
    fig = dict(data = data, layout = layout)
    py.iplot(fig, filename = 'lattice_basics')


    # html file
    py.plot(fig, filename='4-1-simple_lattice.html')

##################################################
# ################ periodic thing  #################
# #################################################

def periodic(save = False):
    # Define the lattice vectors
    vec_0 = np.array([-.5, 0])
    a1 = np.array([1, 0])
    a2 = np.array([.5, np.sqrt(3)/2])
    a1_alt = -a1-a2
    a2_alt = a1_alt + a1
    a2_c = np.array([0,np.sqrt(3)])

    # Create the pattern
    pattern_points = lattice_generation(a1,a2)
    pattern = go.Scatter(x=pattern_points.T[0],y=pattern_points.T[1],mode='markers',marker=dict(
        color='Black',
        size = 20,
        symbol = 'hourglass-open')
        )

    # Lattice Choice A
    latticeA = go.Scatter(visible = False, x = pattern_points.T[0],y = pattern_points.T[1],mode='markers',marker=dict(
            color = 'Red',
            size = 10,
            )
        )

    # Lattice Choice B
    latticeB = go.Scatter(visible = False, x = pattern_points.T[0]+0.5,y = pattern_points.T[1],mode='markers',marker=dict(
            color='Blue',
            size = 10,
            )
        )

    # Annotate the lattice vectors
    # Button 1
    bt1_annot = make_arrow(a1,r'') + make_arrow(a2,r'',text_shift=[-0.3,-0.1], vec_zero = [0,-.1])
    # Button 2
    bt2_annot = make_arrow(a1+vec_0,r'', vec_zero = vec_0, color = 'Blue') + make_arrow(a2+vec_0,r'',text_shift=[-0.3,-0.1], vec_zero = [-.55,-.1], color = 'Blue')
    # Button 3
    bt3_annot = make_arrow([1,0], r'') + make_arrow([0, np.sqrt(3)], r'',text_shift=[-0.3,-0.1])

    # (0)  Button 1, (0, 1-5) Button 2, (0, 6-8) Button 3, (0,1,9,10)
    data = [pattern, latticeA, latticeB, *dash_contour(a1,a2, color = 'Red'),
            *dash_contour(a1, a2, vec_zero = vec_0, color = 'Blue'),
            *dash_contour(np.array([1,0]), a2_c, color = 'Red')]


    updatemenus = list([
        dict(
            type="buttons",
            direction = "down",
            active=0,
            buttons=list([
                dict(label="A",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False, False, False, False,]},
                           {"title": "Periodic structure",
                            "annotations": []}]),
                dict(label="B",
                     method="update",
                     args=[{"visible": [True, True, False, True, True, False, False, False, False,]},
                           {"title": "Periodic structure with lattice and primitive unit cell",
                            "annotations": bt1_annot}]),
                dict(label="C",
                     method="update",
                     args=[{"visible": [True, False, True, False, False, True, True, False, False,]},
                           {"title": "Periodic structure with translated lattice and primitive unit cell",
                            "annotations": bt2_annot}]),
                dict(label="D",
                     method="update",
                     args=[{"visible": [True, True, False, False, False, False, False, True, True,]},
                           {"title": "Periodic structure with lattice and conventional unit cell",
                            "annotations": bt3_annot}]),
            ]),
        )
    ]
    )

    # Setting axis to invisible
    plot_range = 2.1
    axis = dict(
            range=[-plot_range,plot_range],
            visible = False,
            showgrid = False,
            fixedrange = True
        )

    # Figure propeties
    layout = dict(
        showlegend = False,
        updatemenus = updatemenus,
        plot_bgcolor = 'rgb(254, 254, 254)',
        width = 600,
        height = 600,
        xaxis = axis,
        yaxis = axis
    )

    # Displaying the figure
    fig = dict(data = data, layout = layout)
    py.iplot(fig, filename = 'lattice_basics')
    
    if save:
        # html file
        py.plot(fig, filename='4-1-periodic.html')

##################################################
# ##############  graphene single  ################
# #################################################

def graphene_single(save = False):
    # Define the lattice vectors
    a1 = np.array([np.sqrt(3),0])
    a2 = np.array([np.sqrt(3)/2,3/2])
    a2_c = np.array([0,3])
    N_points = 10

    # Wigner-Seitz lines
    x_dotted = [np.sqrt(3)/2, -np.sqrt(3)/2, None, np.sqrt(3)/2,0, None, np.sqrt(3)/2, np.sqrt(3), None,
                np.sqrt(3)/2, 3*np.sqrt(3)/2, None, np.sqrt(3)/2, np.sqrt(3), None, np.sqrt(3)/2,0]
    y_dotted = [3/2, 3/2, None, 3/2, 3, None, 3/2, 3, None,
                3/2, 3/2, None, 3/2, 0, None, 3/2, 0]
    WS_x = [0, 0, np.sqrt(3)/2, np.sqrt(3), np.sqrt(3), np.sqrt(3)/2, 0]
    WS_y = [1, 2, 2.5, 2, 1, 0.5, 1]

    # New lattice generation
    def graphene_generation(a1,a2,N = 10):
        grid = np.arange(-N//2,N//2,1)
        xGrid, yGrid = np.meshgrid(grid, grid[np.mod(grid+1,3) != 0])
        return np.reshape(np.kron(xGrid*np.sqrt(3).flatten(),a1),(-1,2))+np.reshape(np.kron(yGrid.flatten(),a2),(-1,2))

    # Creating interatomic lines
    def create_lines(x, y):
        x_edges = []
        y_edges = []
        for i in range(len(x)-1):
            for j in range(i+1, len(x)-1):
                vec_len = np.sqrt((x[j]-x[i])**2+(y[j]-y[i])**2)
                if vec_len < 1.1:
                    x_edges.extend([x[i], x[j], None])
                    y_edges.extend([y[i], y[j], None])

        return x_edges, y_edges

    # Create the pattern
    lat_vec1 = np.array([1,0])
    lat_vec2 = np.array([0,1])
    pattern_points = graphene_generation(lat_vec1, lat_vec2)

    # Extracting data
    xx = np.append(pattern_points.T[0], pattern_points.T[0] + np.sqrt(3)/2)
    yy = np.append(pattern_points.T[1], pattern_points.T[1] + 3/2)

    # Creating graphene structure
    graph_struc = go.Scatter(visible = True, x = xx, y = yy, mode = 'markers', marker=dict(
            color = 'Black',
            size = 10,
            )
        )

    # Creating lines      
    x_edges, y_edges = create_lines(xx, yy)
    line_trace = go.Scatter(name='edge',
                            x=x_edges,
                            y=y_edges,
                            mode='lines',
                            line_width=2,
                            line_color='black')

    # (0)  Button 1, (0, 1-5) Button 2, (0, 6-8) Button 3, (0,1,9,10)
    data = [graph_struc, line_trace]

    # Setting axis to invisible
    plot_range = N_points//3+0.3
    shift = 1
    axis = dict(
            range=[-plot_range+shift, plot_range+shift],
            visible = False,
            showgrid = False,
            fixedrange = True
        )

    # Figure propeties
    layout = dict(
        showlegend = False,
        plot_bgcolor = 'rgb(254, 254, 254)',
        width = 600,
        height = 600,
        xaxis = axis,
        yaxis = axis
    )

    # Displaying the figure
    fig = dict(data = data, layout = layout)
    py.iplot(fig, filename = 'lattice_basics')
    
    if save:
        py.plot(fig,  filename='4-1-graphene-single')

##################################################
# ################    graphene    #################
# #################################################

def graphene(save = False):
    # Define the lattice vectors
    a1 = np.array([np.sqrt(3),0])
    a2 = np.array([np.sqrt(3)/2,3/2])
    a2_c = np.array([0,3])
    N_points = 10

    # Wigner-Seitz lines
    x_dotted = [np.sqrt(3)/2, -np.sqrt(3)/2, None, np.sqrt(3)/2,0, None, np.sqrt(3)/2, np.sqrt(3), None,
                np.sqrt(3)/2, 3*np.sqrt(3)/2, None, np.sqrt(3)/2, np.sqrt(3), None, np.sqrt(3)/2,0]
    y_dotted = [3/2, 3/2, None, 3/2, 3, None, 3/2, 3, None,
                3/2, 3/2, None, 3/2, 0, None, 3/2, 0]
    WS_x = [0, 0, np.sqrt(3)/2, np.sqrt(3), np.sqrt(3), np.sqrt(3)/2, 0]
    WS_y = [1, 2, 2.5, 2, 1, 0.5, 1]

    # New lattice generation
    def graphene_generation(a1,a2,N = 10):
        grid = np.arange(-N//2,N//2,1)
        xGrid, yGrid = np.meshgrid(grid, grid[np.mod(grid+1,3) != 0])
        return np.reshape(np.kron(xGrid*np.sqrt(3).flatten(),a1),(-1,2))+np.reshape(np.kron(yGrid.flatten(),a2),(-1,2))

    # Creating interatomic lines
    def create_lines(x, y):
        x_edges = []
        y_edges = []
        for i in range(len(x)-1):
            for j in range(i+1, len(x)-1):
                vec_len = np.sqrt((x[j]-x[i])**2+(y[j]-y[i])**2)
                if vec_len < 1.1:
                    x_edges.extend([x[i], x[j], None])
                    y_edges.extend([y[i], y[j], None])

        return x_edges, y_edges

    # Create the pattern
    lat_vec1 = np.array([1,0])
    lat_vec2 = np.array([0,1])
    pattern_points = graphene_generation(lat_vec1, lat_vec2)

    # Extracting data
    xx = np.append(pattern_points.T[0], pattern_points.T[0] + np.sqrt(3)/2)
    yy = np.append(pattern_points.T[1], pattern_points.T[1] + 3/2)

    # Creating graphene structure
    graph_struc = go.Scatter(visible = True, x = xx, y = yy, mode = 'markers', marker=dict(
            color = 'Black',
            size = 10,
            )
        )

    # Creating lines      
    x_edges, y_edges = create_lines(xx, yy)
    line_trace = go.Scatter(name='edge',
                            x=x_edges,
                            y=y_edges,
                            mode='lines',
                            line_width=2,
                            line_color='black')

    # Creating lattice
    lat_points = lattice_generation(a1, a2)
    x_lat = lat_points.T[0]
    y_lat = lat_points.T[1]
    lattice = go.Scatter(visible = False, x = x_lat, y = y_lat, mode = 'markers', marker=dict(
            color = 'Red',
            size = 10,
            )
        )

    # Constructing the Wigner-Seitz cell
    WS_dotted = go.Scatter(visible = False,
                            x = x_dotted,
                            y = y_dotted,
                            mode = 'lines',
                            line = dict(color = 'red', width = 2, dash = 'dash')
                            )

    WS_cell = go.Scatter(visible = False,
                            x = WS_x,
                            y = WS_y,
                            mode = 'lines',
                            line = dict(color = 'red', width = 2),
                            fill = 'toself',
                            fillcolor = 'rgba(255, 0, 0, 0.15)'
                            )

    # Button 1
    bt1_annot = make_arrow(a1, '') + make_arrow(a2,'', text_shift=[0,-0.3], vec_zero = [-.05, -.05])
    # Button 2
    bt2_annot = make_arrow(a1,'') + make_arrow(a2_c,'', vec_zero = [0, -.05])


    # (0)  Button 1, (0, 1-5) Button 2, (0, 6-8) Button 3, (0,1,9,10)
    data = [graph_struc, line_trace, lattice, *dash_contour(a1,a2, color = 'Red'), *dash_contour(a1,a2_c, color='Red'), WS_dotted, WS_cell]


    updatemenus = list([
        dict(
            type="buttons",
            direction = "down",
            active=0,
            buttons=list([
                dict(label="A",
                     method="update",
                     args=[{"visible": [True, True, False, False, False, False, False, False, False]},
                           {"title": "Graphene structure",
                            "annotations": []}]),
                dict(label="B",
                     method="update",
                     args=[{"visible": [True, True, True, False, False, False, False, False, False]},
                           {"title": "Lattice",
                            "annotations": []}]),
                dict(label="C",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, False, False, False, False]},
                           {"title": "Lattice with primitive unit cell",
                            "annotations": bt1_annot}]),
                dict(label="D",
                     method="update",
                     args=[{"visible": [True, True, True, False, False, True, True, False, False]},
                           {"title": "Lattice with conventional unit cell",
                            "annotations": bt2_annot}]),
                dict(label="E",
                     method="update",
                     args=[{"visible": [True, True, True, False, False, False, False, True, True]},
                           {"title": "Lattice with the Wigner-Seitz cell",
                            "annotations": []}]),
            ]),
        )
    ]
    )

    # Setting axis to invisible
    plot_range = N_points//3+0.3
    shift = 1
    axis = dict(
            range=[-plot_range+shift, plot_range+shift],
            visible = False,
            showgrid = False,
            fixedrange = True
        )

    # Figure propeties
    layout = dict(
        showlegend = False,
        updatemenus = updatemenus,
        plot_bgcolor = 'rgb(254, 254, 254)',
        width = 600,
        height = 600,
        xaxis = axis,
        yaxis = axis
    )

    # Displaying the figure
    fig = dict(data = data, layout = layout)
    py.iplot(fig, filename = 'lattice_basics')

    if save:
        # html file
        py.plot(fig, filename='4-1-graphene.html')

##################################################
# ################      FCC       #################
# #################################################       

def FCC(save = False):
    # Coordinates of the corner atoms
    x = np.tile(np.arange(0,2,1),4)
    y = np.repeat(np.arange(0,2,1),4)
    z = np.tile(np.repeat(np.arange(0,2,1),2),2)

    # Coordinates for the bcc lattice
    x_bcc = [.5,0,.5,1,.5,.5]
    y_bcc = [.5,.5,0,.5,1,.5]
    z_bcc = [0,.5,.5,.5,.5,1]

    # creating edge lines
    x_edges, y_edges, z_edges = [], [], []
    for i in range(len(x)):
        for j in range(i+1, len(x)):
            vec_len = np.sqrt((x[j]-x[i])**2+(y[j]-y[i])**2+(z[j]-z[i])**2)
            if vec_len < 1.1:
                x_edges.extend([x[i], x[j], None])
                y_edges.extend([y[i], y[j], None])
                z_edges.extend([z[i], z[j], None])

    # Creating fcc lines
    x_fcc, y_fcc, z_fcc = [], [], []
    for j in range(len(x)):
        vec_len = np.sqrt((x[j]-0.5)**2+(y[j]-0.5)**2+(z[j]-0.5)**2)
        if vec_len < 1:
            x_fcc.extend([x[j], 0.5, None])
            y_fcc.extend([y[j], 0.5, None])
            z_fcc.extend([z[j], 0.5, None])

    # Creating bcc lines
    x_bcc_l, y_bcc_l, z_bcc_l = [], [], []
    for j in range(len(x)):
        for i in range(len(x_bcc)):
            vec_len = np.sqrt((x[j]-x_bcc[i])**2+(y[j]-y_bcc[i])**2+(z[j]-z_bcc[i])**2)
            if vec_len < 1:
                x_bcc_l.extend([x_bcc[i], x[j], None])
                y_bcc_l.extend([y_bcc[i], y[j], None])
                z_bcc_l.extend([z_bcc[i], z[j], None])

    # Initialize figure
    c_size = 32
    l_width = 2
    fig = go.Figure()

    # Adding simple qubic traces
    fig.add_trace(
        go.Scatter3d(
            x = x,
            y = y,
            z = z,
            mode = 'markers',
            marker = dict(
                sizemode = 'diameter',
                sizeref = c_size,
                size = c_size,
                color = 'rgb(211,211,211)',
                line = dict(
                  color = 'rgb(0,0,0)',
                  width = 5
                )
                )
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x = x_edges,
            y = y_edges,
            z = z_edges,
            mode = 'lines',
            line_width=l_width,
            line_color='black',
        )
    )


    # fcc traces
    fig.add_trace(
        go.Scatter3d(visible = False,
            x = [0.5],
            y = [0.5],
            z = [0.5],
            mode = 'markers',
            marker = dict(
                sizemode = 'diameter',
                sizeref = c_size,
                size = c_size,
                color = 'rgb(211,211,211)',
                line = dict(
                  color = 'rgb(0,0,0)',
                  width = 5
                )
                )
        )
    )

    fig.add_trace(
        go.Scatter3d(visible = False,
            x = x_fcc,
            y = y_fcc,
            z = z_fcc,
            mode = 'lines',
            line_width=l_width,
            line_color='black'
        )
    )


    # bcc traces
    fig.add_trace(
        go.Scatter3d(visible = False,
            x = x_bcc,
            y = y_bcc,
            z = z_bcc,
            mode = 'markers',
            marker = dict(
                sizemode = 'diameter',
                sizeref = c_size,
                size = c_size,
                color = 'rgb(211,211,211)',
                line = dict(
                  color = 'rgb(0,0,0)',
                  width = 5
                )
                )
        )
    )

    fig.add_trace(
        go.Scatter3d(visible = False,
            x = x_bcc_l,
            y = y_bcc_l,
            z = z_bcc_l,
            mode = 'lines',
            line_width=l_width,
            line_color='black',
        )
    )    

    # Defining button
    button_data = [
        dict(
            type = "buttons",
            direction = "down",
            active = 0,
            buttons = list([
                dict(label="A",
                     method="update",
                     args=[{"visible": [True, True, False, False, False, False]},
                           {"title": "Simple cubic lattice",
                            }]),
                dict(label="B",
                     method="update",
                     args=[{"visible": [True, True, True, True, False, False]},
                           {"title": "Body-centred cubic lattice",
                            }]),
                dict(label="C",
                     method='update',
                     args=[{"visible": [True, True, False, False, True, True]},
                           {"title": "Face-centred cubic lattice",
                            }]),
            ]),
        )
    ]


    # Creating buttons
    fig.update_layout(
        scene = dict(
                    xaxis = dict(
                    title= 'x[a]',
                    ticks='',
                    ),
                    yaxis=dict(
                    title= 'y[a]',
                    ticks='',
                    showgrid = False,
                    zeroline = False,
                    showline = False,
                    ),
                    zaxis=dict(
                    title= 'z[a]',
                    ticks='',
                    )
        ),
        showlegend = False,
        width = 600,
        height = 600,
        updatemenus = button_data,
    )

    # Setting background to white
    fig.update_scenes(xaxis_visible = False, yaxis_visible = False,zaxis_visible = False )
    fig.show();       
    
    if save:
        # html file
        py.plot(fig, filename='4-1-fcc.html')
        

##################################################
# ################     filling    #################
# #################################################   

def filling(save = False):
    # Coordinates of the corner atoms
    x = np.append(np.tile(np.arange(0,2,1),2), 0.5)
    y = np.append(np.repeat(np.arange(0,2,1),2), 0.5)

    # lines
    x_line = [0, 0, 1, 1, 0]
    y_line = [0, 1, 1, 0, 0]

    # Initialize figure
    c_size = 40
    l_width = 2
    fig = go.Figure()

    # Adding x and y axis text
    def add_xy(vec,text,color = 'Black', text_shift = [-0.2,-0.1]):
        annot = [
             dict(
                x=vec[0]+text_shift[0],
                y=vec[1]+text_shift[1],
                xref = 'x',
                ayref = 'y',
                text = text,
                font = dict(
                    color = color,
                    size = 20
                ),
                showarrow=False,
                 )
            ]
        return annot

    # Adding simple fcc face
    fig.add_trace(
        go.Scatter(
            x = x,
            y = y,
            mode = 'markers',
            marker = dict(
                sizemode = 'diameter',
                sizeref = c_size,
                size = c_size,
                color = 'rgb(211,211,211)',
                line = dict(
                  color = 'rgb(0,0,0)',
                  width = 2
                )
                )
        )
    )

    # Trace with blown up atoms
    fig.add_trace(
        go.Scatter(visible = False,
            x = x,
            y = y,
            mode = 'markers',
            marker = dict(
                sizemode = 'diameter',
                sizeref = c_size,
                size = 151,
                color = 'rgb(211,211,211)',
                line = dict(
                  color = 'rgb(0,0,0)',
                  width = 2
                )
                )
        )
    )

    # Adding lines
    fig.add_trace(
        go.Scatter(visible = True,
            x = x_line,
            y = y_line,
            mode = 'lines',
            line_width=l_width,
            line_color='black',
        )
    )  

    # Axis
    axis_annot = add_xy(np.array([.5, 0]), r'x[a]', text_shift = [0,-.1]) + add_xy(np.array([0, .5]), r'y[a]', text_shift = [-.15,0])
    axis_annot2 = axis_annot+make_arrow(np.array([1,1]), r'4R', color = 'Black',vec_zero = np.array([0,0]), text_shift = [.12,-.05])

    # Defining button
    button_data = [
        dict(
            type = "buttons",
            direction = "down",
            active = 0,
            buttons = list([
                dict(label="A",
                     method="update",
                     args=[{"visible": [True, False, True]},
                           {"title": "Face of FCC lattice",
                            "annotations": axis_annot}]),
                dict(label="B",
                     method="update",
                     args=[{"visible": [False, True, True]},
                           {"title": "Face of FCC lattice with 'blown up' atoms",
                            "annotations": axis_annot2}]),
            ]),
        )
    ]

    # Defining axis
    axis = dict(
            range=[-0.5, 1.5],
            visible = False,
            showgrid = False,
            fixedrange = True
        )

    # Creating buttons
    fig.update_layout(
        showlegend = False,
        width = 600,
        height = 600,
        xaxis = axis,
        yaxis = axis,
        updatemenus = button_data,
        plot_bgcolor = 'rgba(0,0,0,0)'
    )
    
    if save:
        # html file
        py.plot(fig, filename='4-1-filling.html')
    
    fig.show();

##################################################
# ################    diatomic    #################
# #################################################        

def diatomic(save = False):
        
    x = np.tile(np.arange(0,2,1),4)
    y = np.repeat(np.arange(0,2,1),4)
    z = np.tile(np.repeat(np.arange(0,2,1),2),2)

    trace1 = go.Scatter3d(
        x = x,
        y = y,
        z = z,
        mode = 'markers',
        marker = dict(
            sizemode = 'diameter',
            sizeref = 20,
            size = 20,
            color = 'rgb(255, 255, 255)',
            line = dict(
              color = 'rgb(0,0,0)',
              width = 5
            )
            )
    )

    trace2 = go.Scatter3d(
        x = [0.5],
        y = [0.5],
        z = [0.5],
        mode = 'markers',
        marker = dict(
            sizemode = 'diameter',
            sizeref = 20,
            size = 20,
            color = 'rgb(0,0,0)',
            line = dict(
              color = 'rgb(0,0,0)',
              width = 5
            )
            )
    )

    data=[trace1, trace2]

    layout=go.Layout(showlegend = False,
                    scene = dict(
                            xaxis=dict(
                            title= 'x[a]',
                            ticks='',
                            showticklabels=False
                            ),
                            yaxis=dict(
                            title= 'y[a]',
                            ticks='',
                            showticklabels=False
                            ),
                            zaxis=dict(
                            title= 'z[a]',
                            ticks='',
                            showticklabels=False
                            )
                        ))


    fig=go.Figure(data=data, layout=layout)
    py.iplot(fig, show_link=False)

    if save:
            # html file
            py.plot(fig, filename='4-1-diatomic.html')

##################################################
# ################    diamond     #################
# #################################################        

def diamond(save = False):
    Xn = np.tile(np.arange(0,2,1),4)
    Yn = np.repeat(np.arange(0,2,1),4)
    Zn = np.tile(np.repeat(np.arange(0,2,1),2),2)

    Xn = np.hstack((Xn, Xn, Xn+0.5, Xn+0.5))
    Yn = np.hstack((Yn, Yn+0.5, Yn+0.5, Yn))
    Zn = np.hstack((Zn, Zn+0.5, Zn, Zn+0.5))

    Xn = np.hstack((Xn, Xn+1/4))
    Yn = np.hstack((Yn, Yn+1/4))
    Zn = np.hstack((Zn, Zn+1/4))

    Xe=[]
    Ye=[]
    Ze=[]

    num_atoms = len(Xn)
    for i in range(num_atoms):
        for j in np.arange(i+1, num_atoms, 1):
            pos1 = np.array([Xn[i], Yn[i], Zn[i]])
            pos2 = np.array([Xn[j], Yn[j], Zn[j]])
            if np.linalg.norm(pos1-pos2) == np.sqrt(3)/4:
                Xe+=[Xn[i], Xn[j], None]
                Ye+=[Yn[i], Yn[j], None]  
                Ze+=[Zn[i], Zn[j], None]  

    trace1=go.Scatter3d(x=Xe,
                   y=Ye,
                   z=Ze,
                   mode='lines',
                   line=dict(color='rgb(0,0,0)', width=3),
                   hoverinfo='none'
                    )

    trace2=go.Scatter3d(x=Xn,
                   y=Yn,
                   z=Zn,
                   mode = 'markers',
                   marker = dict(
                            sizemode = 'diameter',
                            sizeref = 20,
                            size = 20,
                            color = 'rgb(255,255,255)',
                            line = dict(
                                   color = 'rgb(0,0,0)',
                                   width = 5
                                   )
                           )
                         )

    layout=go.Layout(showlegend = False,
                    scene = dict(
                            xaxis=dict(
                            title= 'x[a]',
                            range= [0,1],
                            ticks='',
                            showticklabels=False
                            ),
                            yaxis=dict(
                            title= 'y[a]',
                            range= [0,1],
                            ticks='',
                            showticklabels=False
                            ),
                            zaxis=dict(
                            title= 'z[a]',
                            range= [0,1],
                            ticks='',
                            showticklabels=False
                            )
                        ))

    data=[trace1, trace2]

    fig=go.Figure(data=data, layout=layout)

    py.iplot(fig, filename='Diamond')

    if save:
            # html file
            py.plot(fig, filename='4-1-diamond.html')
