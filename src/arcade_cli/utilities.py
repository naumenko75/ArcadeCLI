from datetime import datetime, date
from colorama import Fore, init
import threading
import time

init(autoreset=True)

# Global variable for tracking the active timer
active_timer = None
time_running = False


def format_time(seconds):
    """Format seconds into HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def countdown_timer(duration, callback):
    """Background timer thread"""
    global timer_running
    timer_running = True

    for remaining in range(duration, 0, -1):
        if not timer_running:
            return
        time.sleep(1)

    if timer_running:
        callback()


def timer_finished():
    """Callback when timer finishes"""
    print(f"\n{Fore.RED}Timer finished!{Fore.RESET}")
    global active_timer, timer_running
    active_timer = None
    timer_running = False


def start_timer(duration):
    """Start a new timer"""
    global active_timer, timer_running

    # Остановить предыдущий таймер, если он запущен
    if active_timer and timer_running:
        stop_timer()

    print(f"{Fore.GREEN}Starting timer for {format_time(duration)}")
    print(f"{Fore.YELLOW}Timer will finish at {(time.time() + duration):.0f} (Unix timestamp).")

    # Запуск таймера в отдельном потоке
    active_timer = threading.Thread(
        target=countdown_timer, args=(duration, timer_finished))
    active_timer.daemon = True
    active_timer.start()

    print(f"{Fore.CYAN}Timer started! Type 'timer stop' to cancel.{Fore.RESET}")


def stop_timer():
    """Stop the active timer (simplified version)"""
    global active_timer, timer_running

    if timer_running:
        timer_running = False
        active_timer = None
        print(f"{Fore.GREEN}Timer stopped.{Fore.RESET}")
    else:
        print(f"{Fore.YELLOW}No active timer to stop.{Fore.RESET}")


def show_timer_status():
    """Show current timer status"""
    global active_timer, timer_running

    if active_timer and timer_running:
        print(f"{Fore.GREEN}Timer is running in background{Fore.RESET}")
        print(f"{Fore.CYAN}Type 'timer stop' to cancel{Fore.RESET}")
    else:
        print(f"{Fore.YELLOW}No active timer{Fore.RESET}")


def print_timer_help():
    """
    Display help for timer commands
    """
    print(f"{Fore.CYAN}Timer commands usage:{Fore.RESET}")
    print("-" * 35)
    print(
        f"{Fore.YELLOW}timer [seconds]{Fore.RESET}     - Start timer for X seconds")
    print(
        f"{Fore.YELLOW}timer [MM:SS]{Fore.RESET}       - Start timer for minutes:seconds")
    print(
        f"{Fore.YELLOW}timer [HH:MM:SS]{Fore.RESET}    - Start timer for hours:minutes:seconds")
    print(f"{Fore.YELLOW}timer stop{Fore.RESET}          - Stop active timer")
    print(f"{Fore.YELLOW}timer status{Fore.RESET}        - Show timer status")
    print(f"{Fore.YELLOW}timer help{Fore.RESET}          - Show this help")


def show_time():
    """
    Display current time
    """
    now = datetime.now()

    print(now.strftime(f'{Fore.LIGHTYELLOW_EX}%H:%M:%S{Fore.RESET}'))


def show_date():
    """
    Display current date in various formats
    """
    today = date.today()
    print(today.strftime(f'{Fore.LIGHTYELLOW_EX}%d %B %Y{Fore.RESET}'))


def show_datetime():
    """
    Display both date and time
    """
    now = datetime.now()
    print(now.strftime(f'{Fore.LIGHTYELLOW_EX}%d %B %Y, %H:%M:%S{Fore.RESET}'))


def show_time_info():
    """
    Display time info: timezone and unix timestamp
    """
    now = datetime.now()
    print(f"Timezone: {now.astimezone().tzinfo}")
    print(f"Unix timestamp: {int(now.timestamp())}")


def show_date_info():
    """
    Display date info
    """
    today = date.today()
    now = datetime.now()

    print(f"Day of year:    {today.strftime('%j')}")
    print(f"Day of week:    {now.strftime('%A')}")
    print(f"Month:          {now.strftime('%B')}")
    print(f"Year:           {today.year}")


def show_datetime_info():
    """
    Display date and time info:
    """
    today = date.today()
    now = datetime.now()

    print(f"Timezone:       {now.astimezone().tzinfo}")
    print(f"Day of year:    {today.strftime('%j')}")
    print(f"Day of week:    {now.strftime('%A')}")
    print(f"Month:          {now.strftime('%B')}")
    print(f"Year:           {today.year}")


def datetime_mode(cmd, args):
    """
    Handle time and date commands
    """
    if len(args) == 0:
        if cmd in ('time', 't'):
            show_time()
        elif cmd in ('date', 'd'):
            show_date()
        elif cmd in ('datetime', 'dt'):
            show_datetime()

    elif len(args) == 1:
        if args[0] == 'info':
            if cmd in ('time', 't'):
                show_time_info()
            elif cmd in ('date', 'd'):
                show_date_info()
            elif cmd in ('datetime', 'dt'):
                show_datetime_info()
        else:
            print(
                f"Invalid argument, type '{cmd} info' to see additional information.")

    else:
        print(f"Too many arguments. Use 'help {cmd}' to see mistake.")


def timer_mode(args):
    """
    Handle timer commands
    """
    if not args:
        show_timer_status()
        return

    command = args[0].lower()

    if command == 'stop':
        stop_timer()

    elif command == 'status':
        show_timer_status()

    elif command in ('help', '?'):
        print_timer_help()

    else:
        # Trying to interpret it as time
        try:
            # Support for different time formats
            if ':' in command:
                # HH:MM:SS or MM:SS format
                parts = command.split(':')
                if len(parts) == 2:
                    # MM:SS
                    minutes = int(parts[0])
                    seconds = int(parts[1])
                    duration = minutes * 60 + seconds
                elif len(parts) == 3:
                    # HH:MM:SS
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    seconds = int(parts[2])
                    duration = hours * 3600 + minutes * 60 + seconds
                else:
                    raise ValueError("Invalid time format")
            else:
                # just a seconds
                duration = int(command)

            if duration <= 0:
                print(f"{Fore.RED}Duration must be positive{Fore.RESET}")
                return

            if duration > 24 * 3600:  # 24 hours
                print(
                    f"{Fore.RED}Timer duration too long (max 24 hours){Fore.RESET}")
                return

            start_timer(duration)

        except ValueError as e:
            print(f"{Fore.RED}Invalid duration: {command}{Fore.RESET}")
            print(
                f"{Fore.YELLOW}Use seconds (60) or time format (01:30 or 01:30:00){Fore.RESET}")
            print_timer_help()
