import copy
import curses
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np


class Grid:
    def __init__(self, width: int, height: int, default_char: str = "#"):
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("width and height must be integers.")
        if not isinstance(default_char, str) or len(default_char) != 1:
            raise ValueError("default_char must be a single character.")
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive integers.")

        self._default_char = default_char
        self._grid = np.full((height, width), default_char, dtype=str)

    @property
    def width(self):
        return self._grid.shape[1]

    @property
    def height(self):
        return self._grid.shape[0]

    @property
    def grid(self):
        """Access the full grid as a NumPy array."""
        return self._grid

    @grid.setter
    def grid(self, new_grid: np.ndarray):
        """Replace the grid with a new NumPy array."""
        if not isinstance(new_grid, np.ndarray):
            raise TypeError("The new grid must be a NumPy array.")
        if new_grid.shape != (self.height, self.width):
            raise ValueError(
                f"The new grid must have shape {(self.height, self.width)}."
            )
        self._grid = new_grid

    def clear(self):
        """Reset grid to default character."""
        self._grid.fill(self._default_char)

    def __str__(self):
        rows = ["".join(row) for row in self._grid]
        return "\n".join(rows)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        return self._grid[key]

    def __setitem__(self, key, value):
        if any(k < 0 for k in key):
            raise ValueError(f"Cannot set grid at negative index {key}.")
        self._grid[key] = value

    def __deepcopy__(self, memo):
        new_grid = Grid(self.width, self.height, self._default_char)
        new_grid._grid = copy.deepcopy(self._grid)
        return new_grid


class Animation:
    def __init__(self, frames: Iterable[Grid]):
        """Animation for ASCII grid consisting of a sequence of Grids.

        Parameters
        ----------
        frames : Iterable[Grid]
            Sequence of Grids for animation

        Methods
        -------
        animate()
            Animate the grid.
        """
        if not isinstance(frames, List):
            raise TypeError("frames must be a list.")

        self.frames = frames
        self.width = frames[0].width
        self.height = frames[0].height

    def animate(self, frame_time: int = 500) -> None:
        """Animate the grid with a time delay between frames."""
        curses_visualizer = CursesVisualizer(self, frame_time)
        curses_visualizer.run()

    def export_xpm(self, file_prefix: str, color_dict: Dict) -> None:
        """Export the animation to an XPM file."""
        exporter = XPMExporter(self, color_dict)
        exporter.export(file_prefix)

    def export_mp4(
        self,
        file_prefix: str,
        color_dict: Dict,
        frame_time: int,
        resolution: Tuple[int, int] = (640, 480),
    ) -> None:
        """Export the animation to an MP4 file."""
        exporter = MP4Exporter(self, color_dict)
        exporter.export(file_prefix, frame_time, resolution)


class CursesVisualizer:
    def __init__(self, animation: Animation, frame_time: int = 500):
        """Create a text-based terminal visualization of an Animation with curses.

        Parameters
        ----------
        animation : Animation
            Animation to visualize.
        frame_time : int, optional
            Time in milliseconds to display each frame, by default 500.

        Methods
        -------
        run()
            Run the visualization.
        """
        self.animation = animation
        self.frame_time = frame_time

        # Set up curses
        stdscr = curses.initscr()  # Initialize the screen
        curses.noecho()  # Turn off echo of keys
        curses.cbreak()  # Immediate reaction to key presses
        stdscr.keypad(True)  # Enable keypad mode
        curses.start_color()  # Allow default colors
        curses.use_default_colors()
        curses.curs_set(0)  # Turn off curser visibility

        self.stdscr = stdscr

    def run(self) -> None:
        """Run the visualization."""
        for frame in self.animation.frames:
            self.stdscr.clear()

            # Add string in middle of screen
            y, x = self.stdscr.getmaxyx()
            y = y // 2 - frame.height // 2
            x = x // 2 - frame.width // 2
            for row in range(frame.height):
                self.stdscr.addstr(y + row, x, "".join(frame.grid[row]))

            self.stdscr.refresh()
            curses.napms(self.frame_time)  # Wait for frame_time milliseconds

        self.stdscr.getkey()
        curses.endwin()


class Exporter:
    def __init__(self, animation: Animation, color_dict: Dict):
        """Export an Animation to a file. Intended to be subclassed."""
        if not isinstance(animation, Animation):
            raise TypeError("animation must be an Animation.")
        if not isinstance(color_dict, Dict):
            raise TypeError("color_dict must be a dictionary.")

        # Check color_dict has all the unique values in frames
        unique_chars = set()
        for frame in animation.frames:
            unique_chars.update(set(np.unique(frame.grid)))

        for char in unique_chars:
            if char not in color_dict:
                raise ValueError(f"color_dict must have a value for {char}.")

        self.animation = animation
        self.color_dict = color_dict


class XPMExporter(Exporter):
    def __init__(self, animation: Animation, color_dict: Dict):
        """Export an Animation to an XPM file.

        Parameters
        ----------
        animation : Animation
            Animation to export.
        color_dict : Dict
            Dictionary mapping characters to color names (either #RRGGBB or a web color name)

        Methods
        -------
        export()
            Export the animation frames to XPM files.

        Notes
        -----
        XPM is a simple text-based image format. The images are readable as text, or
        you can view them with magick display *.xpm.
        """
        super().__init__(animation, color_dict)

    def export(self, file_prefix: str) -> None:
        num_colors = len(self.color_dict)
        width = self.animation.width
        height = self.animation.height
        num_frames = len(self.animation.frames)
        num_digits = len(str(num_frames))

        for i, frame in enumerate(self.animation.frames):
            filename = f"{file_prefix}{i:0{num_digits}d}.xpm"
            filename = Path(filename).resolve()
            with open(filename, "w") as f:
                # Write header
                f.write("/* XPM */\n")
                f.write("static char *xpm[] = {\n")
                f.write(f'"{width} {height} {num_colors} 1",\n')
                for char, color in self.color_dict.items():
                    f.write(f'"{char} c {color}",\n')

                # Write frames
                for row in frame.grid:
                    f.write('"')
                    f.write("".join(row))
                    f.write('",\n')

                f.write("};")


class MP4Exporter(XPMExporter):
    def __init__(self, animation: Animation, color_dict: Dict):
        """Export an Animation to an MP4 file. Requires ffmpeg to be installed.

        Parameters
        ----------
        animation : Animation
            Animation to export.
        color_dict : Dict
            Dictionary mapping characters to color names (either #RRGGBB or a web color name)

        Methods
        -------
        export()
            Export the animation frames to XPM and then stitch them together into an MP4.
        """
        super().__init__(animation, color_dict)

    def export(
        self,
        output_mp4: str,
        frame_time: int,
        resolution: Tuple[int, int] = (640, 480),
        remove_xpm=True,
    ) -> None:
        # Check resolution
        if (
            not isinstance(resolution, tuple)
            or not isinstance(resolution[0], int)
            or not isinstance(resolution[1], int)
        ):
            raise TypeError("resolution must be a tuple of two integers.")

        # Check output_mp4 ends with .mp4
        if not output_mp4.endswith(".mp4"):
            raise ValueError("output_mp4 must end with '.mp4'.")
        output_mp4 = Path(output_mp4).resolve()

        # Check if ffmpeg is installed
        try:
            subprocess.run(["ffmpeg", "-version"], check=True)
        except FileNotFoundError:
            raise FileNotFoundError("ffmpeg not found. Please install ffmpeg.")

        file_prefix = output_mp4.with_suffix("")
        file_prefix = Path(file_prefix).resolve()
        super().export(file_prefix)

        # Use ffmpeg to stitch together the XPM files into an MP4
        ffmpeg_command = [
            "ffmpeg",
            "-framerate",
            f"{1000 / frame_time}",
            "-i",
            f"{file_prefix}%d.xpm",
            "-c:v",
            "libx264",
            "-vf",
            f"scale={resolution[0]}:{resolution[1]}:flags=neighbor,format=yuv420p",
            "-movflags",
            "+faststart",
            f"{file_prefix}.mp4",
            "-y",
        ]
        subprocess.run(ffmpeg_command, check=True)

        if remove_xpm:
            for i in range(len(self.animation.frames)):
                xpm_file = (
                    f"{file_prefix}{i:0{len(str(len(self.animation.frames)))}d}.xpm"
                )
                xpm_file = Path(xpm_file).resolve()
                xpm_file.unlink()


# Add test
if __name__ == "__main__":
    # Make an animation
    grid1 = Grid(4, 4)
    grid1[2, 0] = "X"
    grid2 = copy.deepcopy(grid1)
    grid2[2, 1] = "X"
    grid3 = copy.deepcopy(grid2)
    grid3[2, 2] = "X"
    grid4 = copy.deepcopy(grid3)
    grid4[2, 3] = "X"

    animation = Animation([grid1, grid2, grid3, grid4])
    animation.animate()
    color_dict = {"#": "black", "X": "red"}

    # Export to MP4
    animation.export_mp4(
        "../../practice/output.mp4", color_dict, resolution=(320, 240), frame_time=500
    )
