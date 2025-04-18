import copy
import statistics
import timeit
from sudokutools import generate_board, solve, solve_A
import typing

## Evaluation Parameters ##
# Number of pieces removed from the board to create a puzzle, list of ints
DIFFICULTY_RANGE = range(1, 65)  
# Number of puzzles to solve for each difficulty level
NUM_PUZZLES = 10 
# Number for the best of n runs for each algorithm
NUM_BEST_OF = 3  

def measure_solving_time(solving_function: typing.Callable, board: list[list], num_runs: int=NUM_BEST_OF):
    # Create a copy of the board for verification
    board_copy = copy.deepcopy(board)
    
    # First, check if the solver can solve the board
    board_test = copy.deepcopy(board)
    solved = solving_function(board_test)
    
    if not solved:
        return board_copy, 0, False
    
    # Setup for timeit - need to create a copy each time since the board is modified
    # during solving
    def setup_timer():
        return copy.deepcopy(board)
    
    # String used by timeit to run the solving function
    timer_stmt = f"""
board = _setup_timer()
{solving_function.__name__}(board)
"""
    
    try:
        # Create a timer with globals that include our setup function and solving function
        timer = timeit.Timer(
            stmt=timer_stmt, 
            globals={
                '_setup_timer': setup_timer, 
                solving_function.__name__: solving_function
            }
        )
        
        # Run the timer multiple times and take the best result, to prevent outliers
        times: list[float] = timer.repeat(repeat=num_runs, number=1)
        best_time: float = min(times)
        
        # Return solved board, the best time in seconds, and whether the board was solved
        return board_copy, best_time, True
    
    except Exception as e:
        print(f"Error during timing: {e}")
        return board_copy, 0, False

def compare_algorithms(num_puzzles: int, removed_cells: int):
    backtracking_times = []
    astar_times = []
    backtracking_success = 0
    astar_success = 0
    
    for i in range(num_puzzles):
        board = generate_board(removed_cells)
        
        # Test backtracking algorithm
        bt_board, bt_time, bt_solved = measure_solving_time(solve, copy.deepcopy(board))
        if bt_solved:
            backtracking_success += 1
            backtracking_times.append(bt_time)
            
        # Test A* algorithm
        astar_board, astar_time, astar_solved = measure_solving_time(solve_A, copy.deepcopy(board))
        if astar_solved:
            astar_success += 1
            astar_times.append(astar_time)
    
    # Calculate statistics
    # Most of these are unused for our analysis, but could be helpful if we come back to this project
    stats = {
        "backtracking": {
            "success_rate": backtracking_success / num_puzzles,
            "avg_time": statistics.mean(backtracking_times) if backtracking_times else None,
            "min_time": min(backtracking_times) if backtracking_times else None,
            "max_time": max(backtracking_times) if backtracking_times else None,
            "median_time": statistics.median(backtracking_times) if backtracking_times else None
        },
        "astar": {
            "success_rate": astar_success / num_puzzles,
            "avg_time": statistics.mean(astar_times) if astar_times else None,
            "min_time": min(astar_times) if astar_times else None,
            "max_time": max(astar_times) if astar_times else None,
            "median_time": statistics.median(astar_times) if astar_times else None
        }
    }
    
    return stats

if __name__ == "__main__":
    # Testing Parameters
    difficulty_levels = DIFFICULTY_RANGE
    puzzles_per_level = NUM_PUZZLES
    
    difficulty_results = {}
    
    # Print total number of iterations
    total_puzzles = len(difficulty_levels) * puzzles_per_level
    print(f"\nEvaluating {len(difficulty_levels)} difficulty levels with {puzzles_per_level} puzzles each")

    # Keep track of the current puzzle for progress tracking
    current_puzzle = 0
    
    for difficulty in difficulty_levels:
        print(f"Testing difficulty {difficulty} [{current_puzzle}/{total_puzzles}]")
        stats = compare_algorithms(num_puzzles=puzzles_per_level, removed_cells=difficulty)
        difficulty_results[str(difficulty)] = stats
        
        # Update progress counter
        current_puzzle += puzzles_per_level
        
        # Show completion percentage
        completion = (current_puzzle / total_puzzles) * 100
        print(f"Progress: {completion:.1f}% complete")
    
    # Print summary of difficulty impact
    print(f"\nDifficulty Impact Summary with {puzzles_per_level} iterations:")
    print("-" * 97)
    
    # Create a formatted table header
    print(f"{'Difficulty':<10} | {'Backtracking':<30} | {'A*':<30} | {'Comparison'}")
    print(f"{'':10} | {'Time':<15}{'Success':<15} | {'Time':<15}{'Success':<15} | ")
    print("-" * 97)
    
    # Make sure all difficulty levels are shown in order
    for difficulty in difficulty_levels:
        diff_str = str(difficulty)
        stats = difficulty_results[diff_str]
        
        # Format Backtracking results
        bt_time = stats['backtracking']['avg_time']
        bt_success = stats['backtracking']['success_rate'] * 100  # Convert to percentage
        bt_time_str = f"{bt_time:.5f}s" if bt_time is not None else "N/A"
        bt_success_str = f"{bt_success:.1f}%" if bt_success > 0 else "0.0%"
        
        # Format A* results
        astar_time = stats['astar']['avg_time']
        astar_success = stats['astar']['success_rate'] * 100  # Convert to percentage
        astar_time_str = f"{astar_time:.5f}s" if astar_time is not None else "N/A"
        astar_success_str = f"{astar_success:.1f}%" if astar_success > 0 else "0.0%"
    
        # Calculate the difference in time for comparing both algorithms
        if bt_time is not None and astar_time is not None:

            # Use a small epsilon to avoid division by zero errors
            # Calculate the speedup factor for comparison column
            epsilon = 1e-10
            if abs(astar_time) < epsilon:
                comparison = f"BT is much slower (A* took ~0s)"
            elif abs(bt_time) < epsilon:
                comparison = f"A* is much slower (BT took ~0s)"
            else:
                speedup = bt_time / astar_time
                if speedup > 1:
                    comparison = f"A* is {speedup:.2f}x faster"
                else:
                    comparison = f"BT is {1/speedup:.2f}x faster"
        else:
            comparison = "N/A"
            
        # Print each row of the table
        print(f"{difficulty:<10} | {bt_time_str:<15}{bt_success_str:<15} | {astar_time_str:<15}{astar_success_str:<15} | {comparison}")