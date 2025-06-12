from . import *

class ProxyChecker:
    def __init__(self, layout: dymatic_layout.Layout, list_http: list, list_socks4: list, list_socks5: list,
                 threads: int = 500,
                 retries: int = 1,
                 timeout: int= 8, checkPing: bool = False):

        self.list_http = list_http
        self.list_socks4 = list_socks4
        self.list_socks5 = list_socks5

        self.layout: dymatic_layout.Layout = layout
        self.threads: int = threads
        self.retries: int = retries
        self.checkPing: bool = checkPing
        self.timeout = ClientTimeout(total=timeout)
        self.messages = deque(maxlen=os.get_terminal_size()[1]-3)
        self.files: List= open(r"src/proxies.txt").read().strip().split("\n")

        self.reader_country = geoip2.database.Reader("src/GeoLite2-Country.mmdb")
        self.reader_asn = geoip2.database.Reader("src/GeoLite2-ASN.mmdb")

        dymatic_layout.parameter_rgb.update_total_process(len(self.files)*3)

        self.line_live: int = 0

    @staticmethod
    async def ping_ip(ip_address, count=1, timeout=1, interval=0.2):
        try:
            # Gửi ping bất đồng bộ với các tham số tối ưu
            result = await async_ping(
                ip_address,
                count=count,
                timeout=timeout,
                interval=interval,
                privileged=False  # Thử không dùng quyền root
            )
            if result.is_alive:
                return f"{round(result.avg_rtt)}"
            else:
                return "LOSS"
        except (Exception, ):
            return "LOSS"

    async def run_checker(self, proxy_url: str) -> int:

        for attempt in range(self.retries):
            try:
                async with ClientSession(
                        connector=ProxyConnector.from_url(f'{proxy_url}'),
                        timeout=self.timeout,
                        skip_auto_headers=["User-Agent"],

                ) as session:
                    async with session.get("http://httpbin.org/ip") as response:
                        if response.status == 200:
                            return 1

            except (Exception,):
                await asyncio.sleep(0.250)  # Exponential backoff
        return 0


    async def run_checker_anonymity(self, proxy_url: str) -> int:

        for attempt in range(self.retries):
            try:
                async with ClientSession(
                        connector=ProxyConnector.from_url(f'{proxy_url}'),
                        timeout=self.timeout,

                ) as session:
                    async with session.get("http://httpbin.org/anything") as response:
                        if response.status == 200:
                            data = await response.json()
                            proxy_ip = data.get("origin")
                            headers = data.get("headers", {})

                            # Kiểm tra anonymity
                            if proxy_ip == "116.102.162.220":
                                return 1  # Transparent

                            # Danh sách các header proxy phổ biến
                            privacy_headers = [
                                "X-Forwarded-For", "X-Forwarded-Host", "X-Forwarded-Proto",
                                "Via", "Proxy-Connection", "X-Proxy-ID", "MT-Proxy-ID",
                                "X-Tinyproxy", "Proxy-Authenticate", "Proxy-Authorization",
                                "X-Squid-Error"
                            ]

                            # Kiểm tra sự hiện diện của header proxy
                            if any(header in headers for header in privacy_headers):
                                return 2  # Anonymous

                            return 3  # Elite
            except (Exception,):
                await asyncio.sleep(0.250)  # Exponential backoff
        return 0




    async def fetch(self, proxy: str, types):
        start = time.time()

        bool_checker = await self.run_checker_anonymity(f"{types}://{proxy}")

        if bool_checker != 0:
            finish = round(time.time() - start)
            self.messages.append(f"[bold green]{proxy}")
            self.line_live += 1
            dymatic_layout.parameter_rgb.update_count_status(
                live=1
            )
            level_proxy = ("LEVEL 1" if bool_checker == 3 else "LEVEL 2" if bool_checker == 2 else "LEVEL 3")

            dymatic_layout.parameter_rgb.update_count_level(
                **{f'l{3 if bool_checker == 1 else 2 if bool_checker == 2 else 1}': 1}
                )

            # dymatic_layout.parameter_rgb.update_count_level(l3=1) if bool_checker == 1 else
            # dymatic_layout.parameter_rgb.update_count_level(l2=1) if bool_checker == 2 else dymatic_layout.parameter_rgb.update_count_level(l1=1)


            dymatic_layout.parameter_rgb.update_count_protocol(**{f"{types}_s" if types == "http" else types: 1})

            if types == "http":
                self.list_http.append(proxy)
            elif types == "socks4":
                self.list_socks4.append(proxy)
            else:
                self.list_socks5.append(proxy)

            if self.checkPing:
                dymatic_layout.parameter_rgb.update_page_data(
                    self.line_live-1,
                    f"{proxy}|{self.reader_country.country(proxy.split(':')[0]).country.iso_code}|{types.upper()}|{level_proxy}"
                    f"|{self.reader_asn.asn(proxy.split(':')[0]).autonomous_system_number}|{finish}ms|LIVE"
                    f"|{await self.ping_ip(proxy.split(':')[0])}|"
                )
            else:
                dymatic_layout.parameter_rgb.update_page_data(
                    self.line_live - 1,
                    f"{proxy}|{self.reader_country.country(proxy.split(':')[0]).country.iso_code}|{types.upper()}|{level_proxy}"
                    f"|{self.reader_asn.asn(proxy.split(':')[0]).autonomous_system_number}|{finish}ms|LIVE"
                    f"||"
                )

        else:
            await asyncio.sleep(0.0001)
            self.messages.append(f"[bold red]{proxy}")
            dymatic_layout.parameter_rgb.update_count_status(
                die=1
            )


        self.layout["body_screen"].update(dymatic_layout.StyleLayout().generate_table_deque(self.messages))

    async def run(self):
        set_tasks: set = set()
        for proxy in self.files:
            for types in ["http", "socks4", "socks5"]:
                if len(set_tasks) >= self.threads:
                    _done, set_tasks = await asyncio.wait(set_tasks, return_when=asyncio.FIRST_COMPLETED)
                await asyncio.sleep(0.0001)
                set_tasks.add(asyncio.create_task(
                    self.fetch(proxy.strip(), types)
                ))
        if set_tasks:
            await asyncio.gather(*set_tasks)


            # self.messages.append(f"[bold red1]{_}")
            # self.layout["body_screen"].update(StyleLayout().generate_table_deque(self.messages))
            # self.live.update(self.layout)