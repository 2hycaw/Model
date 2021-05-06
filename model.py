import random
import tkinter
import matplotlib
matplotlib.use('TkAgg')
# import matplotlib.pyplot
import agentframework
import csv
import requests
import bs4

#Web scraping
page = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = page.text
soup = bs4.BeautifulSoup(content, 'html.parser')

# Convert scraped data to lists of integers
td_ys = [int(y.text) for y in soup.find_all(attrs={"class" : "y"})]
td_xs = [int(x.text) for x in soup.find_all(attrs={"class" : "x"})]

# Coordinate data as pairs (y, x)
td = list(zip(td_ys, td_xs))

# Create the global environment
environment = []

with open('in.txt', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        environment = [[value for value in row] for row in reader]

num_of_agents = 10
num_of_iterations = 100
neighbourhood = 20

# Make the agents from the first num_of_agents coordinates
agents = []
for (y, x) in td[:num_of_agents]:
    agents.append(agentframework.Agent(environment, agents, y, x))

# Setup the basic figure and axes for matplotlib. We se the axes limits here
# and below for aesthetics.
fig = matplotlib.figure.Figure(figsize=(7, 7))
ax = fig.add_axes([0.1, 0.1, 0.85, 0.85])
ax.set_xlim(0, 99)
ax.set_ylim(0, 99)

# Global boolean variable. Is potentially modified in the update() function.
carry_on = True

def update(frame_number):
    """Function shuffles the list of agents and then lets them interact with
    the environment. Points are plotted on the axes."""
    
    # Need to declare this variable global as we potentially change it.
    global carry_on
    
    # Clear the plot to start again.
    ax.clear()

    # First randomly shuffle the agents, then let the agents interact with
    # the environment.
    for j in range(num_of_iterations):
        random.shuffle(agents)
        for agent in agents:
            agent.move()
            agent.eat()
            agent.share_with_neighbours(neighbourhood)
    
    # If all the agents have enough stores then we end the model early.
    if all(agent.store > 5 for agent in agents):
        carry_on = False
        print("All agents are full!")

    # Set the scope of the axes and display the environment. We need to do
    # this on each iteration because we clear the axes in each loop.
    ax.set_xlim(0, 99)
    ax.set_ylim(0, 99)
    ax.imshow(environment)
    
    # Add each data point to the plot. In this approach each point is
    # automatically given a new colour.
    for agent in agents:
        ax.scatter(agent.x, agent.y)

    return ax

def gen_function():
    """Simple generator function. Maximum iterations 20."""
    a = 0
    # Declared global for clarity.
    global carry_on
    
    # Can be ended early by the carry_on flag.
    while (a < 20) & (carry_on):
        yield a
        a += 1
        
def run():
    # Need to assign the animation to a variable so it does not get garbage
    # collected.
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()

# Setup TkInter environment
root = tkinter.Tk()
root.wm_title("Model")

# Add a menu bar to tkinter
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

# Main canvas environment obtained from the matplotlib figure.
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# Initialise TkInter
tkinter.mainloop()





