from matplotlib.patches import Circle, Ellipse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

role_colors = {
    'Passer': 'darkred',
    'Other Route Runner': 'red',
    'Defensive Coverage' : 'blue',
    'Potential Lurker' : 'lightblue'
}

# Function to draw the football field
def draw_football_field(ax):
    # Draw field boundaries
    ax.plot([0, 120], [0, 0], color='white', linewidth=2)
    ax.plot([0, 120], [53.3, 53.3], color='white', linewidth=2)
    ax.plot([10, 10], [0, 53.3], color='white', linewidth=2)
    ax.plot([110, 110], [0, 53.3], color='white', linewidth=2)
    ax.plot([60, 60], [0, 53.3], color='white', linewidth=2)

    # Shade end zones
    ax.axvspan(0, 10, facecolor='blue', alpha=0.2)
    ax.axvspan(110, 120, facecolor='red', alpha=0.2)

    # Draw yard lines
    for x in range(20, 110, 10):
        ax.plot([x, x], [0, 53.3], color='white', linestyle='--', linewidth=1)

# Function to draw player
def draw_player(ax, x, y, name, role, o):
    if role == 'Targeted Receiver':
        ax.scatter(x, y,
                   c='lime', s=300, edgecolor='white',
                   alpha=1.0, label=str(role), marker='*', linewidth=3)
        ax.text(x, y, name,
                ha='center', va='bottom', fontsize=8, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='red', alpha=0.8, edgecolor='white'))
    else:
         ax.scatter(x, y,
                    c=role_colors[role], s=120, edgecolor='black',
                    alpha=0.8, label=str(role), linewidth=1.5)
    ax.plot([x, x + np.cos(np.deg2rad(o))], [y, y + np.sin(np.deg2rad(o))], linewidth = 1)

# Function to draw circle for radius of player
def draw_circle(ax, x, y, radius):
    circle = Circle((x, y), radius, edgecolor='red', facecolor='none', linewidth=2)
    ax.add_patch(circle)

# Function to draw ball
def draw_ball(ax, x, y):
    football = Ellipse((x, y), 3, 1.5, edgecolor='black', facecolor='brown', linewidth = 2, label = 'Football')
    ax.add_patch(football)

def draw_position_of_last_frame(frame_data, radius):
    
    game_id = frame_data['game_id'].values[0]
    play_id = frame_data['play_id'].values[0]
    ball_x = frame_data['ball_land_x'].values[0]
    ball_y = frame_data['ball_land_y'].values[0]
    target_x = frame_data.loc[frame_data['player_role'] == 'Targeted Receiver', 'x'].values[0]
    target_y = frame_data.loc[frame_data['player_role'] == 'Targeted Receiver', 'y'].values[0]
    frame_data.loc[(frame_data['x'] < target_x) & (frame_data['player_role'] == 'Defensive Coverage'), 'player_role'] = 'Potential Lurker'

    fig, ax = plt.subplots(figsize=(16, 8)) # Slightly wider plot for the legend
    ax.set_facecolor('green')
    ax.axis("equal")
    draw_football_field(ax)

    for x, y, name, role, o in zip(frame_data.x, frame_data.y, frame_data.player_name, frame_data.player_role, frame_data.o):
        draw_player(ax, x, y, name, role, o)
    
    draw_ball(ax, ball_x, ball_y)
    draw_circle(ax, ball_x, ball_y, radius)
    draw_circle(ax, target_x, target_y, radius)

    #ax.set_xlim(0, 120)
    #ax.set_ylim(0, 53.3)

    title_text = f'Game: {game_id}, Play: {play_id}'
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.,
                  fontsize=10, framealpha=0.9)
    ax.set_title(title_text, fontsize=12, pad=20, fontweight='bold')
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.subplots_adjust(right=0.85)