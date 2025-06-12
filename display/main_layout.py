from . import *

class MainLayout:

    @staticmethod
    def layout_main() -> Layout:
        root_layout = Layout(name="root")

        root_layout.split_column(
            Layout(name="head", size=3),
            Layout(name="body", ratio=1),
            # Layout(name="footer", size=5),
        )
        root_layout["head"].split_row(
            Layout(name="head_author", size=47),
            Layout(name="head_title", size=71),
            Layout(name="head_github", size=33),
            Layout(name="head_telegram", size=30),
            Layout(name="head_icon"),
        )

        root_layout["body"].split_row(
            Layout(name="body_screen", size=25),
            Layout(name="body_main", ratio=1),
            Layout(name="body_menu_setting_option", size=57),

        )
        root_layout["body_main"].split_column(
            Layout(name="body_main_display", ratio=1),
            Layout(name="body_main_footer", size=5),
        )
        root_layout["body_menu_setting_option"].split_column(
            Layout(name="body_start", size=9),  # 1
            Layout(name="body_pages", size=3),  # 1
            Layout(name="body_process_none", size=3),  # 4
            Layout(name="body_protocol_level", size=9),  # 2
            Layout(name="body_status_hazard", size=9),  # 3
            Layout(name="body_performance"),  # 5
            Layout(name="body_security", size=5),  # 6
            Layout(name="body_notification", size=5),  # 6
        )
        #
        root_layout["body_start"].split_row(
            Layout(name="body_start_option"),
            Layout(name="body_start_run"),
        )

        root_layout["body_pages"].split_row(
            Layout(name="body_setting_tools", size=28),
            Layout(name="body_pages_left", size=5),
            Layout(name="body_pages_default"),
            Layout(name="body_pages_right", size=5),
        )

        root_layout["body_start_option"].split_column(
            Layout(name="body_proxy_scraper"),
            Layout(name="body_proxy_checker"),
            Layout(name="body_clean_refresh"), # body_clean_refresh
        )
        #
        root_layout["body_start_run"].split_column(
            Layout(name="body_run_tools"),
            Layout(name="body_import_file"),
            Layout(name="body_export_file"),
        )
        #
        root_layout["body_protocol_level"].split_row(
            Layout(name="body_protocol"),
            Layout(name="body_level"),
        )

        root_layout["body_status_hazard"].split_row(
            Layout(name="body_status"),
            Layout(name="body_hazard"),
        )

        root_layout["body_security"].split_row(
            Layout(name="body_screen_f12"),
            Layout(name="body_time_process"),
        )

        return root_layout
