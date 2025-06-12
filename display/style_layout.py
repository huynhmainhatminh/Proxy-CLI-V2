from display.main_layout import *

class SynchronizedPerformance(ProgressColumn):
    def __init__(self):
        super().__init__()
        self.last_update = 3
        self.frame = 0
        self.color_footer = ""
        self.color_main = ""

        # Initialize overall progress
        self.overall_progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            BarColumn(style=f"bold {self.color_main}"),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            TextColumn("[progress.percentage][bold sky_blue1]{task.percentage:>3.0f}%"),
        )
        self.overall_task = self.overall_progress.add_task(
            "", vertical="top"
        )

        self.max_cpu_freq = psutil.cpu_freq().max / 1000
        self.count_cpu = psutil.cpu_count(logical=True)

        # Initialize individual progress bars
        self.none_progress = Progress("{task.description}", TextColumn(""))
        self.none_progress.add_task(
            "",
        )
        self.memory_progress = Progress(
            "{task.description}",
            BarColumn(style=f"bold {self.color_main}"),
            TextColumn("[progress.percentage][bold violet]{task.percentage:>3.0f}%"),
        )
        self.memory_progress.add_task(
            "[bold yellow1][ [bold sky_blue1]MEMORY [bold yellow1]]", total=100,
            vertical="top"
        )

        self.cpu_progress = Progress(
            "{task.description}",
            BarColumn(style=f"bold {self.color_main}"),
            TextColumn("[progress.percentage][bold violet]{task.percentage:>3.0f}%"),
        )
        self.cpu_progress.add_task(
            "[bold yellow1][ [bold sky_blue1]CPU [bold yellow1]]", total=100,
            vertical="top"
        )

        self.battery_progress = Progress(
            "{task.description}",
            BarColumn(style=f"bold {self.color_main}"),
            TextColumn("[progress.percentage][bold violet]{task.percentage:>3.0f}%"),
        )
        self.battery_progress.add_task(
            "[bold yellow1][ [bold sky_blue1]BATTERY [bold yellow1]]", total=100,
            vertical="top"
        )

        self.ram_free_progress = Progress(
            "{task.description}",
            BarColumn(style=f"bold {self.color_main}"),
            TextColumn("[progress.percentage][bold violet]{task.percentage:>3.0f}%"),
        )
        self.ram_free_progress.add_task(
            "[bold yellow1][ [bold sky_blue1]RAM FREE [bold yellow1]]", total=100,
            vertical="top"
        )

        # Initialize performance table and panel
        self.performance_table = Table.grid(expand=True)

        # Directly create the Panel here and reference it properly
        self.performance_panel = Panel(
            Group(
                self.memory_progress, self.none_progress, self.cpu_progress, self.none_progress,
                self.ram_free_progress, self.none_progress, self.battery_progress
            ),
            padding=(1, 1),
            title=f"[bold yellow1][ [bold sky_blue1]PERFORMANCE [bold yellow1]]",
            border_style=f"bold {self.color_main}",
            style=f"bold {self.color_footer}",  # Initial style with the default color
        )

        # Add the panel to the table in __init__
        self.performance_table.add_row(self.performance_panel)

    def render(self, task):
        elapsed_seconds = int(task.elapsed)
        if elapsed_seconds > self.last_update:
            self.frame += 5
            r_main = int((math.sin(math.radians(self.frame)) + 1) * 127.5)
            g_main = int((math.sin(math.radians(self.frame + 120)) + 1) * 127.5)
            b_main = int((math.sin(math.radians(self.frame + 240)) + 1) * 127.5)

            r_footer = int((math.sin(math.radians(self.frame + 60)) + 1) * 127.5)
            g_footer = int((math.sin(math.radians(self.frame + 180)) + 1) * 127.5)
            b_footer = int((math.sin(math.radians(self.frame + 300)) + 1) * 127.5)

            # Convert RGB to string
            self.color_main = f"rgb({r_main},{g_main},{b_main})"
            self.color_footer = f"rgb({r_footer},{g_footer},{b_footer})"
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            composite_metric = round((memory_percent * self.count_cpu) / 100, 2)
            battery = psutil.sensors_battery()

            battery_percent = battery.percent

            free_percent = (memory.free / memory.total) * 100

            self.memory_progress.update(self.overall_task, completed=memory_percent)
            self.cpu_progress.update(self.overall_task, completed=composite_metric)

            self.battery_progress.update(self.overall_task, completed=battery_percent)
            self.ram_free_progress.update(self.overall_task, completed=free_percent)

            # Update the panel style dynamically
            self.performance_panel.style = f"bold {self.color_footer}"
            self.performance_panel.border_style = f"bold {self.color_main}"

        return self.performance_table


# class ProcessNoneRGB:
#     def __init__(
#             self,
#             speed: float = 40.0,  # Tốc độ thay đổi màu (độ mỗi giây)
#             bar_length: int = 53,  # Chiều dài tối đa của thanh tiến trình
#             process_speed: float = 2.0  # Tốc độ hoàn thành tiến trình (chu kỳ mỗi giây)
#     ) -> None:
#         self.speed = speed
#         self.bar_length = bar_length
#         self.process_speed = process_speed
#         self.frame = 0
#
#     @staticmethod
#     def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
#         """Chuyển đổi từ HSL sang RGB."""
#         h = h % 360
#         s = max(0, min(1, s))
#         l = max(0, min(1, l))
#
#         c = (1 - abs(2 * l - 1)) * s
#         x = c * (1 - abs((h / 60) % 2 - 1))
#         m = l - c / 2
#
#         if 0 <= h < 60:
#             r, g, b = c, x, 0
#         elif 60 <= h < 120:
#             r, g, b = x, c, 0
#         elif 120 <= h < 180:
#             r, g, b = 0, c, x
#         elif 180 <= h < 240:
#             r, g, b = 0, x, c
#         elif 240 <= h < 300:
#             r, g, b = x, 0, c
#         else:
#             r, g, b = c, 0, x
#
#         return (
#             int((r + m) * 255),
#             int((g + m) * 255),
#             int((b + m) * 255)
#         )
#
#     def __rich__(self) -> Panel:
#         t = time.time()
#
#         # Tính độ dài thanh tiến trình (dao động từ 0 đến bar_length)
#         progress = (math.sin(t * self.process_speed) + 1) / 2
#         current_length = int(progress * self.bar_length)
#
#         # Tạo thanh tiến trình
#         bar_text = Text(justify="center")
#         for i in range(self.bar_length):
#             # Tính hue cho mỗi khối
#             hue = (t * self.speed + i * 360 / self.bar_length) % 360
#             if i < current_length:
#                 r, g, b = self.hsl_to_rgb(hue, 1.0, 0.5)
#                 color = f"rgb({r},{g},{b})"
#                 bar_text.append("█", style=color)
#             else:
#                 r, g, b = self.hsl_to_rgb(hue, 1.0, 0.5)
#                 color = f"rgb({r},{g},{b})"
#                 bar_text.append("█", style=color)
#
#         # Tính màu cho viền Panel
#         hue_border = (t * self.speed) % 360
#         r_border, g_border, b_border = self.hsl_to_rgb(hue_border, 1.0, 0.5)
#         f"rgb({r_border},{g_border},{b_border})"
#
#         self.frame += 5
#         r_main = int((math.sin(math.radians(self.frame)) + 1) * 127.5)
#         g_main = int((math.sin(math.radians(self.frame + 120)) + 1) * 127.5)
#         b_main = int((math.sin(math.radians(self.frame + 240)) + 1) * 127.5)
#
#         r_footer = int((math.sin(math.radians(self.frame + 60)) + 1) * 127.5)
#         g_footer = int((math.sin(math.radians(self.frame + 180)) + 1) * 127.5)
#         b_footer = int((math.sin(math.radians(self.frame + 300)) + 1) * 127.5)
#
#         # Trả về Panel với thanh tiến trình
#         return Panel(
#             bar_text,
#             border_style=f"bold rgb({r_footer},{g_footer},{b_footer})",
#             style=f"bold rgb({r_main},{g_main},{b_main})",
#             expand=True
#         )


class ProcessNoneRGB:
    def __init__(
            self,
            speed: float = 80.0,
            bar_length: int = 53,
            total_time: float = 10.0
    ) -> None:
        self.speed = speed
        self.bar_length = bar_length
        self.total_time = total_time
        self.start_time = time.time()
        self.frame = 0
        self.completed = False
        self._last_update = 0.0
        self._color_cache = {}  # Cache để lưu trữ màu sắc đã tính toán

    @staticmethod
    def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
        h = h % 360
        s = max(0, min(1, s))
        l = max(0, min(1, l))

        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        return (
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )

    def __rich__(self) -> Panel:
        current_time = time.time()
        # Giới hạn tần suất cập nhật để cải thiện hiệu suất (60 FPS)
        if current_time - self._last_update < 1/120:
            return self._last_panel if hasattr(self, '_last_panel') else Panel(Text(""))

        self._last_update = current_time
        elapsed = current_time - self.start_time
        progress = min(elapsed / self.total_time, 1.0)
        if progress >= 1.0:
            self.completed = True

        current_length = int(progress * self.bar_length)
        bar_text = Text(justify="center")

        # Tối ưu hóa tính toán màu sắc bằng cách sử dụng cache
        for i in range(self.bar_length):
            hue = (current_time * self.speed + i * 360 / self.bar_length) % 360
            lightness = 0.5 + 0.15 * math.sin(math.radians(hue + current_time * self.speed * 10))
            hue_key = (round(hue, 1), round(lightness, 2))
            if hue_key not in self._color_cache:
                self._color_cache[hue_key] = self.hsl_to_rgb(hue, 1, 0.5)
            r, g, b = self._color_cache[hue_key]
            color = f"rgb({r},{g},{b})"
            bar_text.append("█" if i < current_length else " ", style=color)

        # Tính toán màu viền
        hue_border = (current_time * self.speed) % 360
        hue_border_key = round(hue_border, 2)
        if hue_border_key not in self._color_cache:
            self._color_cache[hue_border_key] = self.hsl_to_rgb(hue_border, 1, 0.5)
        r_border, g_border, b_border = self._color_cache[hue_border_key]
        border_color = f"rgb({r_border},{g_border},{b_border})"

        # Tính toán màu chính với tốc độ cập nhật mượt mà hơn
        self.frame += 2  # Giảm tốc độ tăng frame để mượt mà hơn
        r_main = int((math.sin(math.radians(self.frame)) + 1) * 127.5)
        g_main = int((math.sin(math.radians(self.frame + 120)) + 1) * 127.5)
        b_main = int((math.sin(math.radians(self.frame + 240)) + 1) * 127.5)
        main_color = f"rgb({r_main},{g_main},{b_main})"

        title_text = f"[ {int(progress * 100)} % ]"

        # Tạo Panel và lưu trữ để sử dụng lại nếu cần
        panel = Panel(
            bar_text,
            border_style=f"bold {border_color}",
            style=f"bold {main_color}",
            expand=True,
            title=title_text if not self.completed else None,
            title_align="center"
        )
        self._last_panel = panel
        return panel

class StyleRGB:

    def __init__(
            self, content: str | None, title: str | None,
            justify: Literal["default", "left", "center", "right", "full"] = "center"
    ) -> None:
        self.frame = 0
        self.content: str | None = content
        self.title: str | None = title
        self.justify: Literal["default", "left", "center", "right", "full"] = justify

    def __rich__(self) -> Panel:
        # Calculate dynamic colors based on time (frame)
        self.frame += 3
        r_main = int((math.sin(math.radians(self.frame)) + 1) * 127.5)
        g_main = int((math.sin(math.radians(self.frame + 120)) + 1) * 127.5)
        b_main = int((math.sin(math.radians(self.frame + 240)) + 1) * 127.5)

        r_footer = int((math.sin(math.radians(self.frame + 60)) + 1) * 127.5)
        g_footer = int((math.sin(math.radians(self.frame + 180)) + 1) * 127.5)
        b_footer = int((math.sin(math.radians(self.frame + 300)) + 1) * 127.5)

        # Convert RGB to string
        self.color_main = f"rgb({r_main},{g_main},{b_main})"
        self.color_footer = f"rgb({r_footer},{g_footer},{b_footer})"

        grid = Table.grid(expand=True)
        grid.add_column(justify=self.justify)

        if self.content == "PROXY CHECKER & PROXY SCRAPER ( PREMIUM )":

            grid.add_row(
                f"[bold cyan]PROXY CHECKER [bold red]& [bold yellow]PROXY SCRAPER [bold orchid1]( [bold "
                f"sky_blue1]PREMIUM [bold orchid1])   [bold white]|   [bold pale_violet_red1]{datetime.now().ctime()}"
            )
        else:
            grid.add_row(
                self.content
            )
        return Panel(
            grid, border_style=f"bold {self.color_footer}", style=f"bold {self.color_main}"
        )

class StyleLayout:
    def __init__(self) -> None:
        self.layout: Layout = MainLayout().layout_main()

        self.option_setting_body = {

            "head_author": "[bold bright_green]Copyright By [bold bright_white]: [bold cyan]Huỳnh Mai Nhật Minh [bold yellow1]([bold bright_red] 2005 [bold yellow1])[/]",
            "head_title": f"PROXY CHECKER & PROXY SCRAPER ( PREMIUM )",
            "head_github": f"[ Github ] : huynhmainhatminh",
            "head_telegram": f"[ Telegram ] : @MarkJethro",
            "head_icon": f"[ X ] : @HunhMaiNhtMinh1",
            ########## body_start ##########
            "body_proxy_scraper": "[bold yellow1][[bold sky_blue1] PROXY [bold cyan1]SCRAPER [bold yellow1]]",
            "body_proxy_checker": "[bold yellow1][[bold sky_blue1] PROXY [light_goldenrod1]CHECKER [bold yellow1]]",
            "body_clean_refresh": "[bold yellow1][[bold orange1] REFRESH TOOLS [bold yellow1]]",
            "body_run_tools": "[bold yellow1][[bold sky_blue1] START TOOLS [bold yellow1]]",
            "body_import_file": "[bold yellow1][[bold green1] IMPORT [bold sky_blue1]FILE [bold yellow1]]",
            "body_export_file": "[bold yellow1][[bold orange1] EXPORT [bold sky_blue1]FILE [bold yellow1]]",
            "body_setting_tools": "[bold yellow1][[bold sky_blue1] SETTING TOOLS [bold yellow1]]",
            "body_pages_left": "<",
            "body_pages_right": ">",
        }

    @staticmethod
    def generate_table_deque(rows) -> Panel:
        return Panel(
            "\n".join([str(row) for row in rows]),
            padding=1,
            border_style="bold medium_spring_green",
            title=f"[bold yellow1][[bold sky_blue1] PROXY [light_goldenrod1]CHECKER [bold yellow1]]"
        )

    @staticmethod
    def update_frame_layout(content: str, style: str="bold medium_spring_green") -> Panel:
        sponsor_message = Table.grid(expand=True)
        sponsor_message.add_column(justify="center")
        sponsor_message.add_row(content)

        message_panel = Panel(
            sponsor_message,
            box=ROUNDED,
            style=style
        )
        return message_panel

    @staticmethod
    def update_table_pages(page_min=0, page_max=0) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center")
        grid.add_row(
            f"[bold cyan1]{page_min}[bold yellow1] / [bold red1]{page_max}"
        )
        return Panel(grid, border_style="bold dark_slate_gray2")

    @staticmethod
    def update_table_screen(screen=False):
        grid = Table.grid(expand=True, padding=1)
        grid.add_column(justify="center", ratio=1)

        if screen:
            grid.add_row(
                f"[bold dark_olive_green2][[bold light_slate_blue] lock screen [bold dark_olive_green2]]"
            )
        else:
            grid.add_row(
                f"[bold dark_olive_green2]([bold light_slate_blue] opened screen [bold dark_olive_green2])"
            )
        return Panel(
            grid,
            border_style="bold medium_spring_green", padding=(1, 2),
            title=f"[bold yellow1][ [bold sky_blue1]SCREEN F12 [bold yellow1]]"
        )

    @staticmethod
    def update_table_noti(content: str = "Chúc bạn một ngày mới tốt lành"):
        sponsor_message = Table.grid(expand=True)
        sponsor_message.add_column(justify="center")
        sponsor_message.add_row(content)

        message_panel = Panel(
            sponsor_message,
            padding=(1, 1),
            box=ROUNDED,
            title="[bold yellow1][[bold sky_blue1] NOTIFICATION [bold yellow1]]",
            style="bold medium_spring_green"
        )
        return message_panel

    def update_style_layout(self) -> Layout:

        ######## head #########
        self.layout["head_author"].update(StyleRGB(content=self.option_setting_body["head_author"], title=None))
        self.layout["head_title"].update(StyleRGB(content=self.option_setting_body["head_title"], title=None))
        self.layout["head_github"].update(StyleRGB(content=self.option_setting_body["head_github"], title=None))
        self.layout["head_telegram"].update(StyleRGB(content=self.option_setting_body["head_telegram"], title=None))
        self.layout["head_icon"].update(StyleRGB(content=self.option_setting_body["head_icon"], title=None))

        ############# body #########
        # self.layout["body_proxy_scraper"].update(
        #     self.update_frame_layout(self.option_setting_body["body_proxy_scraper"])
        # )
        # self.layout["body_proxy_checker"].update(
        #     self.update_frame_layout(self.option_setting_body["body_proxy_checker"])
        # )
        # self.layout["body_setting_tools"].update(
        #     self.update_frame_layout(self.option_setting_body["body_setting_tools"])
        # )
        #
        # self.layout["body_run_tools"].update(
        #     self.update_frame_layout(self.option_setting_body["body_run_tools"])
        # )
        #
        # self.layout["body_import_file"].update(
        #     self.update_frame_layout(self.option_setting_body["body_import_file"])
        # )
        #
        # self.layout["body_export_file"].update(
        #     self.update_frame_layout(self.option_setting_body["body_export_file"])
        # )
        # self.layout["body_clean_refresh"].update(
        #     self.update_frame_layout(self.option_setting_body["body_clean_refresh"])
        # )
        # self.layout["body_pages_default"].update(
        #     self.update_table_pages()
        # )
        self.layout["body_pages_left"].update(
            self.update_frame_layout(self.option_setting_body["body_pages_left"])
        )
        self.layout["body_pages_right"].update(
            self.update_frame_layout(self.option_setting_body["body_pages_right"])
        )

        self.layout["body_process_none"].update(ProcessNoneRGB())

        self.layout["body_notification"].update(
            self.update_table_noti()
        )

        self.layout["body_screen_f12"].update(
            self.update_table_screen()
        )

        self.layout["body_screen"].update(
            self.generate_table_deque([""])
        )

        progress_performance = Progress("{task.description}", SynchronizedPerformance())
        progress_performance.add_task("", vertical="top")
        self.layout["body_performance"].update(progress_performance)

        self.time_progress = Progress("{task.description}", TimeElapsedColumn())
        self.time_progress.add_task(" [bold yellow1][ [bold light_slate_blue]TIME [bold yellow1]]", vertical="top")
        self.panel_time = Panel(
            self.time_progress,
            border_style="bold medium_spring_green",
            padding=(1, 1),
            title=f"[bold yellow1][ [bold sky_blue1]TIME PROGRESS [bold yellow1]]"
        )
        self.layout["body_time_process"].update(self.panel_time)


        return self.layout
