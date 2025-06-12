# from tkinter import filedialog
from display.style_layout import *
from src.proxy_checker import ProxyChecker
from src.proxy_scraper import ProxyScraper

class ParameterRGB():
    def __init__(self) -> None:

        self.completed: int = 0
        self.viewing_old_page = False


        self.array_protocol = {
            "http_s": 0,
            "socks4": 0,
            "socks5": 0,
        }

        self.array_level = {
            "l1": 0,
            "l2": 0,
            "l3": 0,
        }

        self.array_status = {
            "all" : 0,
            "live": 0,
            "die" : 0,
        }

        self.array_hazard = {
            "vpn": 0,
            "proxy": 0,
            "tor": 0,
        }

        self.border_color = ""
        self.style_color = ""


        self.frame = 0

        self.last_count = 22
        self.pages = {}  # Store pages as a dictionary
        self.current_page = 1  # Start at page 1
        self.total_pages = 1

        # Initialize overall progress
        self.overall_progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            BarColumn(style=f"bold {self.border_color}"),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            TextColumn("[progress.percentage][bold sky_blue1]{task.percentage:>3.0f}%"),
        )
        self.overall_task = self.overall_progress.add_task(
            "", vertical="top", total=None
        )

        self.progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            BarColumn(style=f"bold {self.style_color}", bar_width=85),
            TimeRemainingColumn(),
            MofNCompleteColumn(),
            TextColumn("[progress.percentage][bold violet]{task.percentage:>3.0f}%"),
        )
        self.progress.add_task("[bold yellow1][ [bold spring_green1]ALL JOBS [bold yellow1]]")


        self.lock = threading.Lock()  # Lock for thread-safe operations
        threading.Thread(target=self.update_colors_loop, daemon=True).start()

    def update_colors(self) -> None:
        """Generate dynamic colors for the panel border."""
        self.frame += 3
        time_factor = self.frame * 0.1  # Tốc độ nhanh hơn một chút để thấy rõ chuyển động

        r = int((math.sin(math.radians(time_factor)) + 1) * 127.5)
        g = int((math.sin(math.radians(time_factor + 120)) + 1) * 127.5)
        b = int((math.sin(math.radians(time_factor + 240)) + 1) * 127.5)

        r_footer = int((math.sin(math.radians(self.frame + 60)) + 1) * 127.5)
        g_footer = int((math.sin(math.radians(self.frame + 180)) + 1) * 127.5)
        b_footer = int((math.sin(math.radians(self.frame + 300)) + 1) * 127.5)

        self.border_color = f"rgb({r},{g},{b})"
        self.style_color = f"rgb({r_footer},{g_footer},{b_footer})"

    def update_colors_loop(self) -> None:
        """Continuously update the colors in a separate thread."""
        while True:
            self.update_colors()
            time.sleep(0.1)  # Smooth color transition

    def update_page_data(self, index, list_account) -> None:
        """Update data in the current page."""
        page_number = (index // self.last_count) + 1
        row_index = index % self.last_count

        with self.lock:
            if page_number not in self.pages:
                self.pages[page_number] = [[""] * 10 for _ in range(self.last_count)]
                self.total_pages = max(self.total_pages, page_number)  # Update total pages
            value = list_account.split("|")
            if len(value) < 10:
                value.extend([""] * (10 - len(value)))
            self.pages[page_number][row_index] = value

            # Automatically switch to the next page only if not viewing older pages
            if not self.viewing_old_page and page_number > self.current_page:
                self.current_page = page_number


    def shift_page(self, direction):
        """Shift to the next or previous page."""
        with self.lock:
            if direction == "next":
                if self.current_page + 1 in self.pages:
                    self.current_page += 1
            elif direction == "previous":
                if self.current_page > 1:
                    self.current_page -= 1

    def update_completed_process(self, completed: int) -> None:

        self.progress.update(self.overall_task, completed=completed)

    def update_count_protocol(self, http_s: int = 0, socks4: int = 0, socks5: int = 0) -> None:
        self.array_protocol['http_s'] += http_s
        self.array_protocol['socks4'] += socks4
        self.array_protocol['socks5'] += socks5

    def update_count_level(self, l1: int = 0, l2: int = 0, l3 : int = 0) -> None:
        self.array_level['l1'] += l1
        self.array_level['l2'] += l2
        self.array_level['l3'] += l3

    def update_count_status(self, live=0, die=0):
        with self.lock:
            self.array_status['live'] += live
            self.array_status['die'] += die
            self.array_status['all'] = self.array_status['live'] + self.array_status['die']
            self.update_completed_process(self.array_status['all'])

    def update_count_hazard(self, vpn: int = 0, proxy: int = 0, tor: int = 0) -> None:
        self.array_hazard['vpn'] += vpn
        self.array_hazard['proxy'] += proxy
        self.array_hazard['tor'] += tor

    def update_total_process(self, total: int) -> None:
        self.progress.update(self.overall_task, total=total)

    def _create_grid_panel(self, title, items, title_color="sky_blue1"):
        grid = Table.grid(padding=1)
        for label, value in items:
            grid.add_row(f"[bold yellow1][[{label} [bold yellow1]][bold turquoise2] :", f"[bold violet]{value}")
        return Panel(
            grid,
            border_style=f"bold {self.border_color}",
            style=f"bold {self.style_color}",
            padding=(1, 1),
            title=f"[bold yellow1][ [bold {title_color}]{title} [bold yellow1]]"
        )

    def update_table_protocol(self) -> Panel:
        items = [
            ("bold spring_green2] HTTP/S", self.array_protocol['http_s']),
            ("bold orange1] SOCKS4", self.array_protocol['socks4']),
            ("bold medium_orchid1] SOCKS5", self.array_protocol['socks5']),
        ]
        return self._create_grid_panel("PROTOCOL", items)

    def update_table_level(self) -> Panel:
        items = [
            ("bold spring_green2] LEVEL 1", self.array_level['l1']),
            ("bold orange1] LEVEL 2", self.array_level['l2']),
            ("bold red1] LEVEL 3", self.array_level['l3']),
        ]
        return self._create_grid_panel("ANONYMITY", items)

    def update_table_status(self) -> Panel:
        items = [
            ("bold cyan1] ALL", self.array_status['all']),
            ("bold spring_green2] LIVE", self.array_status['live']),
            ("bold red1] DIE", self.array_status['die']),
        ]
        return self._create_grid_panel("STATUS", items)


    def update_table_hazard(self):
        items = [
            ("bold spring_green2] VPN", self.array_hazard['vpn']),
            ("bold orange1] PROXY", self.array_hazard['proxy']),
            ("bold medium_orchid1] TOR", self.array_hazard['tor']),
        ]
        return self._create_grid_panel("HAZARD", items)


    def update_table_pages(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="center")
        grid.add_row(
            f"[bold cyan1]{self.current_page}[bold yellow1] / [bold red1]{self.total_pages}"
        )
        return Panel(grid,
                     border_style=f"bold {self.border_color}",
                     style=f"bold {self.style_color}",
                     )


    def reset_table(self) -> None:

        self.completed: int = 0

        self.array_protocol['http_s'] = 0
        self.array_protocol['socks4'] = 0
        self.array_protocol['socks5'] = 0

        self.array_status['live'] = 0
        self.array_status['die'] = 0
        self.array_status['all'] = 0

        self.array_level['l1'] = 0
        self.array_level['l2'] = 0
        self.array_level['l3'] = 0

        self.last_count = 22
        self.pages = {}  # Store pages as a dictionary
        self.current_page = 1  # Start at page 1
        self.total_pages = 1


        self.progress.reset(self.overall_task)
        self.overall_progress.reset(self.overall_task)

        self.update_total_process(total=100)



    def update_table_process(self) -> Table:
        self.performance_table = Table.grid(expand=True)
        self.performance_panel = Panel(
           self.progress,
            padding=(1, 1),
            title=f"[bold yellow1][ [bold sky_blue1]PROCESS [bold yellow1]]",
            border_style=f"bold {self.border_color}",
            style=f"bold {self.style_color}",  # Initial style with the default color
        )

        # Add the panel to the table in __init__
        self.performance_table.add_row(self.performance_panel)

        return self.performance_table


    def update_table_layout(self) -> Panel:
        table = Table(show_lines=True, box=ROUNDED)
        columns = [
            ("", "bold bright_white"),
            ("IP:PORT", "bold cyan1"),
            ("CODE", "bold grey89"),
            ("PROTOCOLS", "green"),
            ("ANONYMITY", "green"),
            ("ORG & ASN", "green"),
            ("TIMEOUT", "green"),
            ("STATUS", "green"),
            ("PING", "green"),
            ("BLACKLIST", "green"),
        ]
        for data_columns in columns:
            table.add_column(data_columns[0], style=data_columns[1], justify="center", no_wrap=True)

        with self.lock:
            page_data = self.pages.get(self.current_page, [[""] * 10 for _ in range(self.last_count)])

        for idx, value in enumerate(page_data, start=(self.current_page - 1) * self.last_count + 1):
            protocol_color = (
                "bold spring_green2" if value[2] == "HTTP"
                else "orange1" if value[2] == "SOCKS4"
                else "bold medium_orchid1"
            )

            ping_color = (
                "bold red1" if value[7] == "LOSS" else "bold cyan1"
            )

            anonymity_color = (
                "bold spring_green2" if value[3] == "LEVEL 1" else "bold orange1" if value[3] == "LEVEL 2" else "bold red1"
            )


            table.add_row(
                f'[bold cyan1]{idx}',
                f'[bold yellow1]{value[0]}',
                f'[bold yellow1]{value[1]}',
                f'[{protocol_color}]{value[2]}',
                f'[{anonymity_color}]{value[3]}',
                f'[bold yellow1]{value[4]}',
                f'[bold yellow1]{value[5]}',
                f'[bold spring_green1]{value[6]}',
                f'[{ping_color}]{value[7]}',
                f'[bold yellow1]{value[8]}',
            )
        return Panel(
            Align.left(table, vertical="top"),
            box=ROUNDED,
            padding=0,
            border_style=f"bold {self.border_color}",
            style=f"bold {self.style_color}"
        )

    def render(self, task=None):
        return (
            self.update_table_protocol(),
            self.update_table_level(),
            self.update_table_status(),
            self.update_table_hazard(),
            self.update_table_process(),
            self.update_table_layout(),
            self.update_table_pages()
        )

parameter_rgb = ParameterRGB()



class CleanMachine:
    def __init__(self, layout):
        self.layout = layout
        self.temp_dirs = [
            os.path.expandvars(r"%TEMP%"),  # Thư mục Temp chính của người dùng
            os.path.expandvars(r"%APPDATA%\LocalLow\Temp"),  # Thư mục Temp phụ
            os.path.expandvars(r"%LOCALAPPDATA%\Temp"),  # Thư mục Temp cục bộ
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\INetCache"),  # Cache IE/Edge
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache"),  # Cache Chrome
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Code Cache"),  # Cache mã Chrome
            os.path.expandvars(r"%LOCALAPPDATA%\Mozilla\Firefox\Profiles\*\cache2"),  # Cache Firefox
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache"),  # Cache Edge
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Recent"),  # Thư mục Recent
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Explorer\ThumbCache"),  # Cache thumbnail
            os.path.expandvars(r"%APPDATA%\Adobe\Flash Player\NativeCache"),  # Cache Flash Player
        ]

        expanded_dirs = []
        for dir_pattern in self.temp_dirs:
            if '*' in dir_pattern:
                expanded_dirs.extend(glob.glob(dir_pattern))
            else:
                expanded_dirs.append(dir_pattern)

        expanded_dirs = list(set(d for d in expanded_dirs if Path(d).exists()))

        initial_free_space = self.get_disk_space()

        total_deleted_size = 0

        with ThreadPoolExecutor(max_workers=8) as executor:  # Tăng số luồng
            futures = {executor.submit(self.clean_directory_threaded, directory): directory for directory in
                       expanded_dirs}
            for future in as_completed(futures):
                try:
                    deleted_size, elapsed_time = future.result()
                    total_deleted_size += deleted_size
                    pass
                except Exception as e:
                    pass
        final_free_space = self.get_disk_space()

        self.layout["body_notification"].update(
                            StyleLayout().update_table_noti(f"[bold sky_blue1]Dung Lượng Giải Phóng[bold white] : [bold yellow1]{(final_free_space - initial_free_space) / 1024 / 1024:.2f} [bold red1]MB")
                        )

    @staticmethod
    def get_size(path):
        total_size = 0
        try:
            path_obj = Path(path)
            if path_obj.is_file():
                return path_obj.stat().st_size
            for item in path_obj.rglob('*'):
                if item.is_file():
                    total_size += item.stat().st_size
        except Exception:
            return 0
        return total_size

    def clean_directory(self, directory):
        deleted_size = 0
        try:
            path = Path(directory)
            if not path.exists():
                return 0, 0
            for item in path.rglob('*'):  # Sử dụng rglob để dọn dẹp sâu hơn
                try:
                    if item.is_file():
                        size = item.stat().st_size
                        item.unlink()
                        deleted_size += size
                    elif item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                        size = self.get_size(item)
                        deleted_size += size
                except (PermissionError, FileNotFoundError, OSError):
                    pass
        except Exception as e:
            pass
        return deleted_size

    def clean_directory_threaded(self, directory):
        """Wrapper để chạy clean_directory trong luồng."""
        return self.clean_directory(directory)

    @staticmethod
    def get_disk_space():
        """Lấy dung lượng đĩa trống (byte)."""
        total, used, free = shutil.disk_usage(os.path.expandvars(r"%SystemDrive%"))
        return free


# class DymaticLayout:
#     def __init__(self, layout: Layout, live: Live | None) -> None:
#         self.layout: Layout = layout
#         self.live: Live | None = live
#         self.selected_index: int = 0
#
#         self.option_setting_body = {
#             "body_proxy_scraper": "[bold yellow1][[bold sky_blue1] PROXY [bold cyan1]SCRAPER [bold yellow1]]",
#             "body_proxy_checker": "[bold yellow1][[bold sky_blue1] PROXY [light_goldenrod1]CHECKER [bold yellow1]]",
#             "body_setting_tools": "[bold yellow1][[bold sky_blue1] SETTING TOOLS [bold yellow1]]",
#             "body_clean_refresh": "[bold yellow1][[bold orange1] REFRESH TOOLS [bold yellow1]]",
#             "body_run_tools": "[bold yellow1][[bold sky_blue1] START TOOLS [bold yellow1]]",
#             "body_import_file": "[bold yellow1][[bold green1] IMPORT [bold sky_blue1]FILE [bold yellow1]]",
#             "body_export_file": "[bold yellow1][[bold orange1] EXPORT [bold sky_blue1]FILE [bold yellow1]]",
#             "body_pages_left": "<",
#             "body_pages_right": ">",
#         }
#
#         self.bool_screen: bool = False
#         self.bool_proxy_checker = False
#         self.bool_proxy_scraper = False
#
#         self.keys_option: list[str] = list(self.option_setting_body.keys())
#
#         self.array_setting = {
#             "threads": 1000,
#             "timeout": 5,
#         }
#
#         # self.loop = asyncio.SelectorEventLoop() # Linux
#         self.loop = asyncio.ProactorEventLoop() # Windows
#
#
#         threading.Thread(target=self._update_body_protocol, daemon=True).start()
#
#
#     def run_tools(self):
#         self.loop.run_until_complete(ProxyChecker(layout=self.layout).run())
#
#     def _update_body_protocol(self) -> None:
#         while True:
#             for i, panel in enumerate(parameter_rgb.render(None)):
#                 self.layout[["body_protocol", "body_level", "body_status", "body_hazard", "body_main_footer",
#                              "body_main_display"][i]].update(panel)
#             if self.live:
#                 self.live.update(self.layout)
#             time.sleep(0.1)  # Reduced frequency
#     def dymatic_select(self) -> None:
#         for i, option in enumerate(self.option_setting_body):
#             if i == self.selected_index:
#                 highlight_table = Table.grid(expand=True)
#                 highlight_table.add_column(justify="center")
#                 highlight_table.add_row(self.option_setting_body[option])
#                 self.layout[option].update(
#                     Panel(
#                         highlight_table,
#                         style="bold medium_orchid1"
#                     )
#                 )
#             else:
#                 self.layout[option].update(StyleLayout().update_frame_layout(self.option_setting_body[option]))
#
#
#     def handle_key_press(self, event) -> None:
#         if event.name == "down" and self.bool_screen is False:
#             self.selected_index = (self.selected_index + 1) % len(self.keys_option)
#         elif event.name == "up" and self.bool_screen is False:
#             self.selected_index = (self.selected_index - 1) % len(self.keys_option)
#         elif event.name == "right" and self.bool_screen is False:
#             self.selected_index = (self.selected_index + 4) % len(self.keys_option)
#         elif event.name == "left" and self.bool_screen is False:
#             self.selected_index = (self.selected_index - 4) % len(self.keys_option)
#         elif event.name == "space" and self.bool_screen is False:
#
#             if self.keys_option[self.selected_index] == "body_run_tools":
#                 self.option_setting_body["body_run_tools"] = "[bold yellow1][[bold red1] START TOOLS [bold yellow1]]"
#
#                 self.dymatic_select()
#                 self.live.update(self.layout)
#                 threading.Thread(target=self.run_tools, daemon=True).start()
#                 self.bool_proxy_scraper = True
#                 # self.loop.run_until_complete(ProxyChecker(layout=self.layout).run())
#
#             elif self.keys_option[self.selected_index] == "body_proxy_checker":
#                 if self.bool_proxy_checker is False:
#                     self.option_setting_body["body_proxy_checker"] = "[bold red1][[bold sky_blue1] PROXY [light_goldenrod1]CHECKER [bold red1]]"
#                     self.bool_proxy_checker = True
#                 else:
#                     self.option_setting_body["body_proxy_checker"] = "[bold yellow1][[bold sky_blue1] PROXY [light_goldenrod1]CHECKER [bold yellow1]]"
#                     self.bool_proxy_checker = False
#
#
#             elif self.keys_option[self.selected_index] == "body_proxy_scraper":
#                 if self.bool_proxy_scraper is False:
#                     self.option_setting_body["body_proxy_scraper"] = "[bold red1][[bold sky_blue1] PROXY [bold cyan1]SCRAPER [bold red1]]"
#                     self.bool_proxy_scraper = True
#
#                 else:
#                     self.option_setting_body["body_proxy_scraper"] = "[bold yellow1][[bold sky_blue1] PROXY [bold cyan1]SCRAPER [bold yellow1]]"
#                     self.bool_proxy_scraper = False
#
#             elif self.keys_option[self.selected_index] == "body_import_file":
#                 pass
#                 # file_path = filedialog.askopenfilename(
#                 #     title="Chọn tệp .txt",
#                 #     filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
#                 # )
#                 #
#                 # self.layout["body_notification"].update(
#                 #     StyleLayout().update_table_noti(f"Đã tìm thấy {len(open(file_path).readlines())} proxies")
#                 # )
#         elif event.name == "f12":
#             self.block_display = False
#
#
#
#         self.dymatic_select()
#         if self.live:
#             self.live.update(self.layout)
#
#
#
#
#         # while True:
#         #     self.array_protocol["http_s"] += 1
#         #     protocol_rgb.update_count_protocol(h=self.array_protocol["http_s"], s4=2, s5=2)
#         #     time.sleep(1)
#         #     self.dymatic_select()
#         #     self.live.update(self.layout)
#
#         # parameter_rgb.update_total_process(1000)
#         # for _ in range(100):
#         #     time.sleep(1)
#         #     parameter_rgb.update_completed_process(_)
#         #     self.dymatic_select()
#         #     self.live.update(self.layout)
#
#         # while True:
#         #     self.messages.append(f"[bold bright_white]{random_ipv4()}")
#         #     self.layout["body_screen"].update(StyleLayout().generate_table_deque(self.messages))
#         #     self.dymatic_select()
#         #     self.live.update(self.layout)



class DymaticLayout:
    def __init__(self, layout: Layout, live: Live | None) -> None:
        self.layout = layout
        self.live = live
        self.selected_index = 0

        self.list_http: list = []
        self.list_socks4: list = []
        self.list_socks5: list = []

        with open("src/settings.json", 'r', encoding='utf-8') as file:
            self.settings_file = json.load(file)
            self.settings = self.settings_file['data']

        self.option_setting_body = {
            "body_proxy_scraper": f"{'[bold red1][[bold cyan1] PROXY [light_goldenrod1]SCRAPER [bold red1]]' if self.settings['proxyScraper'] else '[bold yellow1][[bold sky_blue1] PROXY [cyan1]SCRAPER [bold yellow1]]'}",
            "body_proxy_checker": f"{'[bold red1][[bold sky_blue1] PROXY [light_goldenrod1]CHECKER [bold red1]]' if self.settings['proxyChecker'] else '[bold yellow1][[bold sky_blue1] PROXY [light_goldenrod1]CHECKER [bold yellow1]]'}",
            "body_clean_refresh": "[bold yellow1][[bold orange1] REFRESH TOOLS [bold yellow1]]",
            "body_setting_tools": "[bold yellow1][[bold sky_blue1] SETTING TOOLS [bold yellow1]]",
            "body_run_tools": "[bold yellow1][[bold sky_blue1] START TOOLS [bold yellow1]]",
            "body_import_file": "[bold yellow1][[bold green1] IMPORT [bold sky_blue1]FILE [bold yellow1]]",
            "body_export_file": "[bold yellow1][[bold orange1] EXPORT [bold sky_blue1]FILE [bold yellow1]]",
            "body_pages_left": "<",
            "body_pages_right": ">",
        }

        self.option_setting_body_backups = self.option_setting_body


        self.option_setting_tools = {
            "body_threads": f"[bold sky_blue1] THREADS : {self.settings['threads']}",
            "body_timeout": f"[bold sky_blue1] TIMEOUT : {self.settings['timeout']}",
            "body_retries": f"[bold sky_blue1] RETRIES : {self.settings['retries']}",
            "body_setting_tools": "[bold yellow1][[bold sky_blue1] COME BACK TOOLS [bold yellow1]]",
            "body_up" : "[bold sky_blue1]▲",
            "body_default": "[bold sky_blue1]‖",
            "body_down" : "[bold sky_blue1]▼",
            "body_run_tools": "[bold yellow1][[bold sky_blue1] CHECK BLACKLIST [bold yellow1]]",
            "body_import_file": f"{'[bold red1][[bold sky_blue1] CHECK PING IP [bold red1]]' if self.settings['checkPing'] else '[bold yellow1][[bold sky_blue1] CHECK PING IP [bold yellow1]]'}",
            "body_export_file": "[bold yellow1][[bold sky_blue1] MODE AUTO TOOLS [bold yellow1]]",
            "body_pages_left": "<",
            "body_pages_right": ">",
        }


        self.bool_screen = False

        self.bool_setting_tools = False


        ########## bool edit setting ##############

        self.bool_edit_threads = False
        self.bool_edit_retries = False
        self.bool_edit_timeout = False
        self.bool_proxy_checker = False
        self.bool_proxy_scraper = False
        self.bool_check_ping = False




        self.keys_option = list(self.option_setting_body.keys())

        self._running = True
        self.proxy_checker_future: Future | None = None

        self.loop = asyncio.ProactorEventLoop()
        threading.Thread(target=self._run_event_loop, daemon=True).start()

        asyncio.run_coroutine_threadsafe(self._update_body_protocol_async(), self.loop)

        self._setup_keyboard_handlers()

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def _update_body_protocol_async(self):
        try:
            while self._running:
                for i, panel in enumerate(parameter_rgb.render(None)):
                    self.layout[["body_protocol", "body_level", "body_status", "body_hazard", "body_main_footer",
                                 "body_main_display", "body_pages_default"][i]].update(panel)
                if self.live:
                    self.live.update(self.layout)
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            raise

    def _setup_keyboard_handlers(self):
        keyboard.on_press_key("down", lambda e: self.handle_key_press("down"))
        keyboard.on_press_key("up", lambda e: self.handle_key_press("up"))
        keyboard.on_press_key("right", lambda e: self.handle_key_press("right"))
        keyboard.on_press_key("left", lambda e: self.handle_key_press("left"))
        keyboard.on_press_key("space", lambda e: self.handle_key_press("space"))
        keyboard.on_press_key("f12", lambda e: self.handle_key_press("f12"))

    def handle_key_press(self, event_name: str) -> None:
        if event_name == "down" and not self.bool_screen:
            self.selected_index = (self.selected_index + 1) % len(self.keys_option)
        elif event_name == "up" and not self.bool_screen:
            self.selected_index = (self.selected_index - 1) % len(self.keys_option)
        elif event_name == "right" and not self.bool_screen:
            self.selected_index = (self.selected_index + 4) % len(self.keys_option)
        elif event_name == "left" and not self.bool_screen:
            self.selected_index = (self.selected_index - 4) % len(self.keys_option)
        elif event_name == "space" and not self.bool_screen:
            # print(self.keys_option[self.selected_index])
            if self.keys_option[self.selected_index] == "body_run_tools" and self.bool_setting_tools is False:

                if self.settings['proxyScraper']:
                    self.option_setting_body[
                        "body_run_tools"] = "[bold yellow1][[bold red1] STOPS TOOLS [bold yellow1]]"
                    self.dymatic_select()
                    asyncio.run_coroutine_threadsafe(
                                ProxyScraper(layout=self.layout,).run_scraper(), self.loop
                            )
                    time.sleep(10)

                if self.settings['proxyChecker']:
                    self.list_http.clear()
                    self.list_socks4.clear()
                    self.list_socks5.clear()

                    self.layout["body_screen"].update(
                        StyleLayout().generate_table_deque([""])
                    )
                    if self.proxy_checker_future is None or self.proxy_checker_future.done():
                        if len(open('src/proxies.txt').readlines()) > 100:
                            self.option_setting_body["body_run_tools"] = "[bold yellow1][[bold red1] STOPS TOOLS [bold yellow1]]"
                            self.bool_screen = True
                            self.dymatic_select()
                            parameter_rgb.reset_table()
                            self.proxy_checker_future = asyncio.run_coroutine_threadsafe(
                                self._run_proxy_checker(), self.loop
                            )
                        else:
                            self.layout["body_notification"].update(
                                StyleLayout().update_table_noti(
                                    f"[bold red1]Số Lượng Proxy Không Đủ[bold white]. [bold yellow1]Tối Thiểu 100 Proxy"
                                )
                            )
                else:
                    self.layout["body_notification"].update(
                        StyleLayout().update_table_noti(
                            f"[bold red1]Hãy Chọn Chức Năng [bold sky_blue1]PROXY [light_goldenrod1]CHECKER"
                        )
                    )

            elif self.keys_option[self.selected_index] == "body_proxy_checker" and self.bool_setting_tools is False:

                if self.bool_proxy_checker:
                    self.bool_proxy_checker = False
                else:
                    self.bool_proxy_checker = True

                if self.bool_proxy_checker:
                    self.settings['proxyChecker'] = True
                    self.option_setting_body["body_proxy_checker"] = "[bold red1][[bold sky_blue1] PROXY [light_goldenrod1]CHECKER [bold red1]]"
                    self.layout["body_notification"].update(
                        StyleLayout().update_table_noti(
                            f"[bold green1]Đã Chọn Chức Năng [bold sky_blue1]PROXY [light_goldenrod1]CHECKER"
                        )
                    )
                else:
                    self.settings['proxyChecker'] = False
                    self.option_setting_body["body_proxy_checker"] = "[bold yellow1][[bold sky_blue1] PROXY [light_goldenrod1]CHECKER [bold yellow1]]"

                    self.layout["body_notification"].update(
                        StyleLayout().update_table_noti(
                            f"[bold red1]Đã Hủy Chức Năng [bold sky_blue1]PROXY [light_goldenrod1]CHECKER"
                        )
                    )

                with open("src/settings.json", 'w', encoding='utf-8') as file:
                    json.dump(self.settings_file, file, indent=4)

            elif self.keys_option[self.selected_index] == "body_proxy_scraper" and self.bool_setting_tools is False:

                if self.bool_proxy_scraper:
                    self.bool_proxy_scraper = False
                else:
                    self.bool_proxy_scraper = True

                if self.bool_proxy_scraper:
                    self.settings['proxyScraper'] = True
                    self.option_setting_body["body_proxy_scraper"] = "[bold red1][[bold sky_blue1] PROXY [bold cyan1]SCRAPER [bold red1]]"
                    self.layout["body_notification"].update(
                        StyleLayout().update_table_noti(
                            f"[bold green1]Đã Chọn Chức Năng [bold sky_blue1]PROXY [cyan1]SCRAPER"
                        )
                    )
                else:
                    self.settings['proxyScraper'] = False
                    self.option_setting_body["body_proxy_scraper"] = "[bold yellow1][[bold sky_blue1] PROXY [bold cyan1]SCRAPER [bold yellow1]]"

                    self.layout["body_notification"].update(
                        StyleLayout().update_table_noti(
                            f"[bold red1]Đã Hủy Chức Năng [bold sky_blue1]PROXY [cyan1]SCRAPER"
                        )
                    )
                with open("src/settings.json", 'w', encoding='utf-8') as file:
                    json.dump(self.settings_file, file, indent=4)

            elif self.keys_option[self.selected_index] == "body_setting_tools":

                if self.bool_setting_tools:
                    self.layout["body_proxy_scraper"].unsplit()
                    self.layout["body_proxy_checker"].unsplit()
                    self.layout["body_clean_refresh"].unsplit()
                    self.bool_setting_tools = False
                    self.option_setting_body = self.option_setting_body_backups
                    self.keys_option = list(self.option_setting_body.keys())  # Khôi phục keys_option
                    self.selected_index = 0
                    with open("src/settings.json", 'w', encoding='utf-8') as file:
                        json.dump(self.settings_file, file, indent=4)

                else:
                    self.layout["body_proxy_scraper"].split_row(
                        Layout(name="body_threads"),
                        Layout(name="body_up", size=5),
                    )
                    self.layout["body_proxy_checker"].split_row(
                        Layout(name="body_timeout"),
                        Layout(name="body_default", size=5),
                    )
                    self.layout["body_clean_refresh"].split_row(
                        Layout(name="body_retries"),
                        Layout(name="body_down", size=5),
                    )
                    self.bool_setting_tools = True
                    self.option_setting_body = self.option_setting_tools
                    self.keys_option = list(self.option_setting_tools.keys())  # Cập nhật keys_option
                    self.selected_index = 0

            elif self.keys_option[self.selected_index] == "body_clean_refresh" and self.bool_setting_tools is False:

                self.option_setting_body["body_clean_refresh"] = "[bold red1][[bold orange1] REFRESH TOOLS [bold red1]]"
                self.layout["body_notification"].update(
                    StyleLayout().update_table_noti(
                        f"[bold green1]Đang Tiến Hành [bold orange1]Dọn Dép Rác [bold red1]..."
                    )
                )
                parameter_rgb.reset_table()
                self.layout["body_screen"].update(
                    StyleLayout().generate_table_deque([""])
                )
                self.dymatic_select()
                CleanMachine(self.layout)
                self.layout["body_process_none"].update(ProcessNoneRGB())
                self.option_setting_body["body_clean_refresh"] = "[bold yellow1][[bold orange1] REFRESH TOOLS [bold yellow1]]"


            elif self.keys_option[self.selected_index] == "body_pages_left":
                parameter_rgb.shift_page("previous")

            elif self.keys_option[self.selected_index] == "body_pages_right":
                parameter_rgb.shift_page("next")


            elif self.keys_option[self.selected_index] == "body_import_file" and self.bool_setting_tools is False:
                pass

            elif self.keys_option[self.selected_index] == "body_export_file" and self.bool_setting_tools is False:

                self.list_http.clear()
                self.list_socks4.clear()
                self.list_socks5.clear()

                for proxy_type, proxies in [("http", self.list_http), ("socks4", self.list_socks4),
                                            ("socks5", self.list_socks5)]:

                    self.option_setting_body['body_export_file'] = "[bold red1][[bold orange1] EXPORT [bold sky_blue1]FILE [bold red1]]"

                    with open(f"result/raw/{proxy_type}.txt", "a") as f:
                        for proxy in proxies:
                            f.write(proxy + "\n")

                all_proxies = list(set(self.list_http + self.list_socks4 + self.list_socks5))

                with open("result/raw/all.txt", "a") as f:
                    for proxy in all_proxies:
                        f.write(proxy + "\n")

                time.sleep(3)

                self.option_setting_body['body_export_file'] = "[bold yellow1][[bold orange1] EXPORT [bold sky_blue1]FILE [bold yellow1]]"

                self.layout["body_notification"].update(
                    StyleLayout().update_table_noti(
                        f"[bold green1]Đã Lưu File Thành Công Thư Mục : [bold red1]RAW [bold cyan]/ [bold yellow1]FULL"
                    )
                )

            elif self.keys_option[self.selected_index] == "body_threads" and self.bool_setting_tools is True:
                self.bool_edit_threads = True
                self.bool_edit_timeout = False
                self.bool_edit_retries = False

                if self.bool_edit_threads:
                    self.option_setting_body["body_threads"] = f"[bold medium_orchid1] THREADS : {self.settings['threads']}"
                    self.option_setting_body["body_timeout"] = f"[bold sky_blue1] TIMEOUT : {self.settings['timeout']}"
                    self.option_setting_body["body_retries"] = f"[bold sky_blue1] RETRIES : {self.settings['retries']}"


            elif self.keys_option[self.selected_index] == "body_timeout" and self.bool_setting_tools is True:
                self.bool_edit_threads = False
                self.bool_edit_timeout = True
                self.bool_edit_retries = False


                if self.bool_edit_timeout:
                    self.option_setting_body["body_threads"] = f"[bold sky_blue1] THREADS : {self.settings['threads']}"
                    self.option_setting_body["body_timeout"] = f"[bold medium_orchid1] TIMEOUT : {self.settings['timeout']}"
                    self.option_setting_body["body_retries"] = f"[bold sky_blue1] RETRIES : {self.settings['retries']}"

            elif self.keys_option[self.selected_index] == "body_retries" and self.bool_setting_tools is True:
                self.bool_edit_threads = False
                self.bool_edit_timeout = False
                self.bool_edit_retries = True


                if self.bool_edit_retries:
                    self.option_setting_body["body_threads"] = f"[bold sky_blue1] THREADS : {self.settings['threads']}"
                    self.option_setting_body["body_timeout"] = f"[bold sky_blue1] TIMEOUT : {self.settings['timeout']}"
                    self.option_setting_body["body_retries"] = f"[bold medium_orchid1] RETRIES : {self.settings['retries']}"

            elif self.keys_option[self.selected_index] == "body_up" and self.bool_setting_tools is True:

                if self.bool_edit_threads:
                    if self.settings['threads'] != 2000:
                        self.settings['threads'] += 100
                    else:
                        self.layout["body_notification"].update(
                            StyleLayout().update_table_noti(
                                f"[bold red1]Đã Đạt Giới Hạn Tối Đa [bold yellow1]( [bold sky_blue1]THREADS[bold yellow1] )"
                                )
                        )
                    self.option_setting_body["body_threads"] = f"[bold medium_orchid1] THREADS : {self.settings['threads']}"
                elif self.bool_edit_timeout:
                    if self.settings['timeout'] < 15:
                        self.settings['timeout'] += 1
                    else:
                        self.layout["body_notification"].update(
                            StyleLayout().update_table_noti(
                                f"[bold red1]Đã Đạt Giới Hạn Tối Đa [bold yellow1]( [bold sky_blue1]TIMEOUT[bold yellow1] )"
                            )
                        )
                    self.option_setting_body["body_timeout"] = f"[bold medium_orchid1] TIMEOUT : {self.settings['timeout']}"
                elif self.bool_edit_retries:
                    if self.settings['retries'] < 5:
                        self.settings['retries'] += 1
                    else:
                        self.layout["body_notification"].update(
                            StyleLayout().update_table_noti(
                                f"[bold red1]Đã Đạt Giới Hạn Tối Đa [bold yellow1]( [bold sky_blue1]RETRIES[bold yellow1] )"
                            )
                        )
                    self.option_setting_body["body_retries"] = f"[bold medium_orchid1] RETRIES : {self.settings['retries']}"
                else:
                    pass


            elif self.keys_option[self.selected_index] == "body_down" and self.bool_setting_tools is True:

                if self.bool_edit_threads:
                    if self.settings['threads'] > 500:
                        self.settings['threads'] -= 100
                    else:
                        self.layout["body_notification"].update(
                            StyleLayout().update_table_noti(
                                f"[bold red1]Đã Đạt Giới Hạn Nhỏ Nhất [bold yellow1]( [bold sky_blue1]THREADS[bold yellow1] )"
                            )
                        )
                    self.option_setting_body["body_threads"] = f"[bold medium_orchid1] THREADS : {self.settings['threads']}"
                elif self.bool_edit_timeout:
                    if self.settings['timeout'] > 5:
                        self.settings['timeout'] -= 1
                    else:
                        self.layout["body_notification"].update(
                            StyleLayout().update_table_noti(
                                f"[bold red1]Đã Đạt Giới Hạn Nhỏ Nhất [bold yellow1]( [bold sky_blue1]TIMEOUT[bold yellow1] )"
                            )
                        )
                    self.option_setting_body["body_timeout"] = f"[bold medium_orchid1] TIMEOUT : {self.settings['timeout']}"
                elif self.bool_edit_retries:
                    if self.settings['retries'] > 1:
                        self.settings['retries'] -= 1
                    else:
                        self.layout["body_notification"].update(
                            StyleLayout().update_table_noti(
                                f"[bold red1]Đã Đạt Giới Hạn Nhỏ Nhất [bold yellow1]( [bold sky_blue1]RETRIES[bold yellow1] )"
                            )
                        )
                    self.option_setting_body["body_retries"] = f"[bold medium_orchid1] RETRIES : {self.settings['retries']}"
                else:
                    pass


            elif self.keys_option[self.selected_index] == "body_run_tools" and self.bool_setting_tools is True:
                self.option_setting_body["body_run_tools"] = "[bold red1][[bold sky_blue1] CHECK BLACKLIST [bold red1]]"


            elif self.keys_option[self.selected_index] == "body_import_file" and self.bool_setting_tools is True:
                if self.bool_check_ping:
                    self.bool_check_ping = False

                else:
                    self.bool_check_ping = True

                if self.bool_check_ping:
                    self.settings['checkPing'] = True
                    self.option_setting_body["body_import_file"] = "[bold red1][[bold sky_blue1] CHECK PING IP [bold red1]]"
                    self.layout["body_notification"].update(
                        StyleLayout().update_table_noti(
                            f"[bold green1]Đã Chọn Chức Năng [bold yellow1]( [bold sky_blue1]CHECK PING IP[bold yellow1] )"
                        )
                    )
                else:
                    self.settings['checkPing'] = False
                    self.option_setting_body["body_import_file"] = "[bold yellow1][[bold sky_blue1] CHECK PING IP [bold yellow1]]"
                    self.layout["body_notification"].update(
                        StyleLayout().update_table_noti(
                            f"[bold red1]Đã Hủy Chức Năng [bold yellow1]( [bold sky_blue1]CHECK PING IP[bold yellow1] )"
                        )
                    )


        elif event_name == "f12":
            self.bool_screen = False
            if self.proxy_checker_future is not None and not self.proxy_checker_future.done():
                asyncio.run_coroutine_threadsafe(self._cancel_proxy_checker(), self.loop)
                self.option_setting_body["body_run_tools"] = "[bold yellow1][[bold sky_blue1] START TOOLS [bold yellow1]]"

        self.dymatic_select()
        if self.live:
            asyncio.run_coroutine_threadsafe(self._update_layout_once(), self.loop)

    async def _run_proxy_checker(self):
        try:
            await ProxyChecker(layout=self.layout,
                               threads=self.settings['threads'],
                               retries=self.settings['retries'],
                               timeout=self.settings['timeout'],
                               checkPing=self.settings['checkPing'],
                               list_http=self.list_http, list_socks4=self.list_socks4, list_socks5=self.list_socks5).run()
        except asyncio.CancelledError:
            raise
        finally:
            self.bool_screen = False
            self._stop_proxy_checker = False
            self.option_setting_body["body_run_tools"] = "[bold yellow1][[bold sky_blue1] START TOOLS [bold yellow1]]"
            self.dymatic_select()
            # await self._update_layout_once()

    async def _cancel_proxy_checker(self):
        if self.proxy_checker_future and not self.proxy_checker_future.done():
            self.proxy_checker_future.cancel()

    async def _update_layout_once(self):
        if self.live:
            self.live.update(self.layout)
            await asyncio.sleep(0)

    def dymatic_select(self):
        for i, option in enumerate(self.option_setting_body):
            if i == self.selected_index:
                highlight_table = Table.grid(expand=True)
                highlight_table.add_column(justify="center")
                highlight_table.add_row(self.option_setting_body[option])
                self.layout[option].update(Panel(highlight_table, style="bold medium_orchid1"))
            else:
                self.layout[option].update(StyleLayout().update_frame_layout(self.option_setting_body[option]))


