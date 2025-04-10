# Script to sort an Arcaea chart file (.aff) for comparison
# Usage: python sort_chart.py <path_to_aff_file>

from ArcaeaLib import Aff, Timing, Tap, Hold, Arc, Flick, Camera, SceneControl, TiminggroupProperties
import sys
import os

# Define the desired sort order for event types explicitly
# This ensures consistency if the class definition order changes slightly
EVENT_SORT_ORDER = {
    Timing: 0,
    Tap: 1,
    Hold: 2,
    Arc: 3,
    Flick: 4,
    Camera: 5,
    SceneControl: 6,
    TiminggroupProperties: -1 # Keep timing groups definitions conceptually early
}

def sort_key(event):
    """Provides a stable sorting key for an event based on time, type, and specific attributes."""
    event_type = type(event)
    type_order = EVENT_SORT_ORDER.get(event_type, 999)

    if isinstance(event, TiminggroupProperties):
        # Sort TiminggroupProperties primarily by their ID
        return (-1, type_order, event.TiminggroupId) # Use -1 time to ensure they come before actual events if needed conceptually

    start_time = getattr(event, 'StartTime', 0) # Default to 0 if no StartTime

    # Base key: Time, Type Order
    key = [start_time, type_order]

    # Add type-specific attributes for tie-breaking
    if event_type is Timing:
        key.extend([getattr(event, 'BPM', 0), getattr(event, 'Beats', 0)])
    elif event_type is Tap:
        key.append(getattr(event, 'Lane', 0))
    elif event_type is Hold:
        key.extend([getattr(event, 'Lane', 0), getattr(event, 'EndTime', 0)])
    elif event_type is Arc:
        # Add multiple attributes for stable sorting of Arcs
        key.extend([
            getattr(event, 'Color', -1),
            getattr(event, 'XStart', 0.0),
            getattr(event, 'YStart', 0.0),
            getattr(event, 'XEnd', 0.0),
            getattr(event, 'YEnd', 0.0),
            getattr(event, 'EasingType', ''),
            getattr(event, 'Effect', ''),
            getattr(event, 'IsSkyLine', False),
            getattr(event, 'EndTime', 0) # EndTime as final tie-breaker for arcs
        ])
    elif event_type is Flick:
         key.extend([
            getattr(event, 'PosX', 0.0),
            getattr(event, 'PosY', 0.0),
            getattr(event, 'VecX', 0.0),
            getattr(event, 'VecY', 0.0)
        ])
    elif event_type is Camera:
         key.extend([
            getattr(event, 'PosX', 0.0),
            getattr(event, 'PosY', 0.0),
            getattr(event, 'PosZ', 0.0),
            getattr(event, 'RotX', 0.0),
            getattr(event, 'RotY', 0.0),
            getattr(event, 'RotZ', 0.0),
            getattr(event, 'EasingType', ''),
            getattr(event, 'LastingTime', 0)
        ])
    elif event_type is SceneControl:
        # SceneControl args list: [StartTime, Type, Param1(optional), Param2(optional)]
        sc_args = getattr(event, 'args', [])
        key.append(sc_args[1] if len(sc_args) > 1 else '') # Type
        key.append(sc_args[2] if len(sc_args) > 2 else None) # Param1 or None
        key.append(sc_args[3] if len(sc_args) > 3 else None) # Param2 or None

    # Return as tuple for sorting
    return tuple(key)


def get_sorted_chart_string(chart: Aff) -> str:
    """Generates the sorted chart string, respecting timing groups."""
    output_string = ''
    output_string += f'AudioOffset:{chart.AudioOffset}\n'
    if chart.TimingPointDensityFactor != 1.0:
        output_string += f'TimingPointDensityFactor:{chart.TimingPointDensityFactor}\n'
    output_string += '-\n'

    grouped_events = {}
    timing_groups_props = {}

    # Separate events by timing group ID and store TiminggroupProperties
    for event in chart.Events:
        if isinstance(event, TiminggroupProperties):
            timing_groups_props[event.TiminggroupId] = event
            if event.TiminggroupId not in grouped_events:
                grouped_events[event.TiminggroupId] = []
        else:
            group_id = getattr(event, 'TiminggroupId', 0) # Default to group 0
            if group_id not in grouped_events:
                grouped_events[group_id] = []
            grouped_events[group_id].append(event)

    # --- Output Main Group (Group 0) ---
    if 0 in grouped_events:
        grouped_events[0].sort(key=sort_key)
        for event in grouped_events[0]:
            # Skip outputting the implicit TiminggroupProperties for group 0
            if not isinstance(event, TiminggroupProperties):
                 output_string += f"{event.__str__()}\n"

    # --- Output Other Timing Groups ---
    # Sort group IDs to ensure consistent output order of groups themselves
    other_group_ids = sorted([gid for gid in grouped_events if gid != 0])

    for group_id in other_group_ids:
        # Output the timing group definition line
        if group_id in timing_groups_props:
            output_string += f"{timing_groups_props[group_id].__str__()}{{\n"
        else:
            # Fallback if definition is missing but events exist (indicates chart error)
             output_string += f"# Warning: Timing Group {group_id} definition missing.\n"
             output_string += f"timinggroup(){{\n" # Generic empty group start

        # Output the sorted events within this group
        if group_id in grouped_events:
            grouped_events[group_id].sort(key=sort_key)
            for event in grouped_events[group_id]:
                 # Skip outputting TiminggroupProperties within the block content
                 if not isinstance(event, TiminggroupProperties):
                     output_string += f"  {event.__str__()}\n"

        output_string += '};\n' # Close the timing group block

    return output_string.strip() # Remove trailing newline if any


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sort_chart.py <path_to_aff_file>")
        print("Example: python sort_chart.py testfiles/2.aff")
        sys.exit(1)

    input_file_path = sys.argv[1]

    if not os.path.exists(input_file_path):
        print(f"Error: Input file not found at '{input_file_path}'")
        sys.exit(1)

    if not input_file_path.lower().endswith('.aff'):
        print(f"Warning: Input file '{input_file_path}' does not have an .aff extension.")
        # Continue anyway, but warn the user

    try:
        # Create an Aff object
        chart = Aff()

        # Load the chart file
        print(f"Loading chart: {input_file_path}...")
        chart.Load(input_file_path)
        print("Load complete.")

        # Get the sorted chart string using the refined logic
        print("Sorting chart...")
        sorted_chart_string = get_sorted_chart_string(chart)
        print("Sorting complete.")

        # Print to console (optional, can be commented out if only file output is needed)
        # print(f"\n--- Sorted Chart Output for {os.path.basename(input_file_path)} ---")
        # print(sorted_chart_string)
        # print("--- End of Sorted Chart ---")

        # Save the sorted chart to a new file
        output_file_path = input_file_path.replace('.aff', '_sorted.aff')
        # Ensure the output path is different if the input didn't end with .aff
        if output_file_path == input_file_path:
             output_file_path += '_sorted'

        try:
            print(f"\nSaving sorted chart to: {output_file_path}...")
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(sorted_chart_string)
            print("Save complete.")
        except Exception as e:
            print(f"\nError saving sorted chart to file '{output_file_path}': {e}")


    except ImportError:
        print("Error: Could not import Aff class from ArcaeaLib.py.")
        print("Ensure ArcaeaLib.py is in the same directory or accessible in your Python path.")
        sys.exit(1)
    except FileNotFoundError:
        # This case should be caught by the os.path.exists check earlier,
        # but kept here as a fallback during chart.Load()
        print(f"Error: Input file not found at '{input_file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred:")
        import traceback
        traceback.print_exc()
        sys.exit(1)
