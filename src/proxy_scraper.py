from . import *
from display.style_layout import *

class ProxyScraper:
    def __init__(self, layout: dymatic_layout.Layout) -> None:
        self.layout: dymatic_layout.Layout = layout
        self.messages = deque(maxlen=os.get_terminal_size()[1] - 3)
        self.list_urls: List[str] = []
        self.all_proxy: List[str] = []

    @staticmethod
    def filter_ip(proxy: str) -> bool:
        regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        try:
            ip = proxy.split(':')[0]
            port = proxy.split(':')[1]
            if re.search(regex, ip):
                if len(port) > 5 or len(port) == 1:
                    return False
                return True
            return False
        except IndexError:
            return False

    @staticmethod
    def filter_text(text: str) -> str | None:
        pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+'
        match = re.search(pattern, text)
        return match.group() if match else None



    async def run_get_proxy(self, url: str) -> None:
        async with ClientSession() as session:
            try:
                async with session.get(url) as response:
                    proxy = await response.text()
                    response_lines = proxy.strip().split('\n')
                    for proxies in response_lines:
                        text_filter = self.filter_text(proxies.strip())
                        if text_filter and self.filter_ip(text_filter.strip()):
                            self.all_proxy.append(text_filter.strip())
            except Exception as e:
                pass

    async def fetch_all(self) -> None:
        tasks = [asyncio.create_task(self.run_get_proxy(link)) for link in self.list_urls]
        await asyncio.gather(*tasks)


    async def get_urls_scraper(self) -> None:
        async with ClientSession() as session:
            try:
                async with session.get("https://raw.githubusercontent.com/huynhmainhatminh/Proxy-CLI-V2/refs/heads/main/urls_scraper/urls.txt") as response:
                    resp = await response.text()
                    self.list_urls.extend(line.strip() for line in resp.splitlines() if line.strip())
            except Exception as e:
                pass
        await self.fetch_all()

    async def run_scraper(self) -> None:
        await self.get_urls_scraper()
        unique_proxies = list(set(self.all_proxy))
        for i, proxy in enumerate(unique_proxies, 1):
            self.messages.append(f"[bold sky_blue2]{proxy}")
        self.layout["body_screen"].update(dymatic_layout.StyleLayout().generate_table_deque(self.messages))
        self.layout["body_notification"].update(
            StyleLayout().update_table_noti(
                f"[bold cyan1] PROXY [light_goldenrod1]SCRAPER : [bold green1]{len(unique_proxies)} [bold yellow1]PROXIES"
            )
        )
        with open("src/proxies.txt", "w") as f:
            f.write("\n".join(unique_proxies))

