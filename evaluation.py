import copy
import statistics
import timeit
from sudokutools import generate_board, print_board, solve, solve_A
from tqdm import tqdm

def measure_solving_time(solving_function, board, num_runs=3):
   
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
    
    # Define the code to time as a string
    timer_stmt = f"""
board = _setup_timer()
{solving_function.__name__}(board)
"""
    
    # Use timeit for accurate measurement
    try:
        # Create a timer with globals that include our setup function and solving function
        timer = timeit.Timer(
            stmt=timer_stmt, 
            globals={
                '_setup_timer': setup_timer, 
                solving_function.__name__: solving_function
            }
        )
        
        # Run the timer multiple times and take the best result
        times = timer.repeat(repeat=num_runs, number=1)
        best_time = min(times)
        
        return board_copy, best_time, True
    except Exception as e:
        print(f"Error during timing: {e}")
        return board_copy, 0, False

def compare_algorithms(num_puzzles, removed_cells, progress_callback=None):
    
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

def evaluate_difficulty_impact(difficulty_levels, puzzles_per_level):

    results = {}
    
    # Calculate total iterations for progress bar
    total_puzzles = len(difficulty_levels) * puzzles_per_level
    print(f"\nEvaluating {len(difficulty_levels)} difficulty levels with {puzzles_per_level} puzzles each")
    
    # Create progress bar
    with tqdm(total=total_puzzles, desc="Testing difficulties", unit="puzzle") as pbar:
        for difficulty in difficulty_levels:
            stats = compare_algorithms(num_puzzles=puzzles_per_level, removed_cells=difficulty)
            results[str(difficulty)] = stats
            
            # Update progress bar after each difficulty level
            pbar.update(puzzles_per_level)
            pbar.set_description(f"Testing difficulty {difficulty}")
    
    return results

if __name__ == "__main__":
    # Testing Parameters
    # Difficulty levels (number of cells to remove)
    # Puzzles per level (number of iterations)
    difficulty_levels = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    puzzles_per_level = 10
    
    difficulty_results = evaluate_difficulty_impact(
        difficulty_levels=difficulty_levels, 
        puzzles_per_level=puzzles_per_level
    )
    
    # Print summary of difficulty impact
    print(f"\nDifficulty Impact Summary with {puzzles_per_level} iterations:")
    print("-" * 50)
    
    # Create a formatted table header
    print(f"{'Difficulty':<10} | {'Backtracking':<20} | {'A*':<20} | {'Comparison'}")
    print("-" * 75)
    
    # Make sure all difficulty levels are shown in order
    for difficulty in difficulty_levels:
        diff_str = str(difficulty)
        stats = difficulty_results[diff_str]
        
        # Format backtracking results
        bt_time = stats['backtracking']['avg_time']
        bt_str = f"{bt_time:.5f}s" if bt_time is not None else "No successful solves"
        
        # Format A* results
        astar_time = stats['astar']['avg_time']
        astar_str = f"{astar_time:.5f}s" if astar_time is not None else "No successful solves"
        
        # Prepare comparison string
        comparison = ""
    
        if bt_time is not None and astar_time is not None:
            # Add a small epsilon to prevent division by zero with very small values
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
            
        # Print the row
        print(f"{difficulty:<10} | {bt_str:<20} | {astar_str:<20} | {comparison}")