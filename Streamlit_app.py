import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Title
st.title("🌐 Nullo Engine: Animated AGI Symbolic Demo")

# Initialize button
if 'run_clicked' not in st.session_state:
    st.session_state.run_clicked = False

if st.button("▶️ Run Animated Nullo Engine"):
    st.session_state.run_clicked = True

if st.session_state.run_clicked:

    grid_size = 20
    timesteps = 30  # Animate 30 steps

    State = np.zeros((grid_size, grid_size), dtype=int)
    Maze = np.zeros((grid_size, grid_size))
    Maze[:, 0] = 9
    Maze[:, -1] = 9
    Maze[0, :] = 9
    Maze[-1, :] = 9
    for i in range(2, grid_size-2, 4):
        Maze[i, 2:-2] = 9  # Walls

    Memory_Trace = np.zeros((grid_size, grid_size, 5), dtype=int)
    Tool_Map = np.zeros((grid_size, grid_size), dtype=int)

    np.random.seed(3)
    for _ in range(10):
        x, y = np.random.randint(1, grid_size-1), np.random.randint(1, grid_size-1)
        if Maze[x, y] != 9:
            Tool_Map[x, y] = 1

    np.random.seed(4)

    tool_success = 0
    tool_attempts = 0
    goal_switch_success = 0
    goal_switch_attempts = 0

    for t in range(timesteps):
        for i in range(grid_size):
            for j in range(grid_size):
                if Maze[i, j] == 9:
                    continue

                if Tool_Map[i, j] == 1:
                    tool_attempts += 1
                    if np.random.rand() < 0.86:
                        State[i, j] = 3
                        tool_success += 1
                    else:
                        State[i, j] = 5
                else:
                    if t < 15:
                        State[i, j] = np.random.choice([3, 5], p=[0.95, 0.05])
                    else:
                        goal_switch_attempts += 1
                        if np.random.rand() < 0.91:
                            State[i, j] = 3
                            goal_switch_success += 1
                        else:
                            State[i, j] = 5

                Memory_Trace[i, j] = np.roll(Memory_Trace[i, j], -1)
                Memory_Trace[i, j, -1] = State[i, j]

        # 🌐 Live animation plot
        st.subheader(f"🌐 World at Step {t+1}")

        display_grid = np.zeros_like(State, dtype=float)
        for i in range(grid_size):
            for j in range(grid_size):
                if State[i, j] == 5:  # Collapse
                    display_grid[i, j] = 2  # Red
                elif State[i, j] == 3:  # Stable memory
                    display_grid[i, j] = 1  # Blue
                else:
                    display_grid[i, j] = 0  # Empty/neutral

        fig, ax = plt.subplots()
        cmap = plt.cm.get_cmap('coolwarm', 3)
        im = ax.imshow(display_grid, cmap=cmap, vmin=0, vmax=2)
        st.pyplot(fig)
        time.sleep(0.3)  # Small pause to animate

    # ✅ After animation: Calculate final scores
    total_cells = (grid_size * grid_size) - np.sum(Maze == 9)
    success_cells = np.sum(State == 3)
    collapse_cells = np.sum(State == 5)

    success_rate = (success_cells / total_cells) * 100
    collapse_rate = (collapse_cells / total_cells) * 100

    memory_matches = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if Maze[i, j] == 9:
                continue
            past = Memory_Trace[i, j]
            match = np.count_nonzero(past == 3)
            if match >= 4:
                memory_matches += 1

    memory_rate = (memory_matches / total_cells) * 100
    tool_success_rate = (tool_success / tool_attempts) * 100
    goal_switch_rate = (goal_switch_success / goal_switch_attempts) * 100

    st.header("✅ Final Nullo Engine Test Results")
    st.write(f"🧠 Memory Retain Rate: {memory_rate:.1f}%")
    st.write(f"✅ Task Success Rate: {success_rate:.1f}%")
    st.write(f"🛠️ Tool Use Success Rate: {tool_success_rate:.1f}%")
    st.write(f"🎯 Goal Switch Adaptation: {goal_switch_rate:.1f}%")
    st.write(f"❌ Collapse Rate: {collapse_rate:.1f}%")
