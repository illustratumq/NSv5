import subprocess
import re
import os


def write_console(string: str):
    write = subprocess.Popen(string.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = write.communicate(timeout=3)
        return out.decode('ascii'), err.decode('ascii')
    except:
        out = 'Час очікування відповіді минув, хост 192.168.9.1 не доступний'
        return out, 1


def usb_over_ip_check(pr: bool = True):
    out, err = write_console('usbip list -r 192.168.9.1')
    pattern = '\d+-\d+: Silicon Labs : CP210x UART Bridge'
    devices = re.findall(pattern, out)
    devices_count = len(devices)
    if devices_count > 0:
        devices_to_string = "\n".join(devices)
        if pr:
            print(f'Знайдено {devices_count} підключених ELRS:\n{devices_to_string}')
        else:
            return devices_count == 3
    else:
        if pr:
            print(f'ELRS не знайдено перевірте підключення:\n{out}')


def usb_devices_check(pr: bool = True):
    out, err = write_console('lsusb')
    devices = [
        'Microdia HDANALOG',
        'Realtek Semiconductor Corp\. RTL[0-9]{4} Gigabit Ethernet Adapter',
        'Realtek Semiconductor Corp\. RTS[0-9]{4} Hub'
    ]
    devices_count = len(devices)
    successful_count = 0
    for d, n in zip(devices, range(1, devices_count + 1)):
        device_string = re.findall(d, out)
        if device_string:
            if pr:
                print(f'[{n}/{devices_count}] ✓ пристрій знайдено: {device_string[0]}')
            successful_count += 1
        else:
            if pr:
                print(f'[{n}/{devices_count}] ✗ пристрій не знайдено: {d}')
    return successful_count == devices_count


def connection_to_the_host(pr: bool = True):
    out, err = write_console('ping -c 3 192.168.9.1')
    packets_pattern = r"(\d+) packets transmitted, (\d+) received, (\d+)% packet loss, time (\d+ms)"
    packets_string = re.findall(packets_pattern, out)
    if packets_string:
        packets_string = packets_string[0]
        if pr:
            print(
                f'Надіслано пакетів: {packets_string[0]}, '
                f'отримано пакетів: {packets_string[1]}, '
                f'втрати: {packets_string[2]}%, '
                f'час затримки: {packets_string[3]}'
            )
        else:
            return True
    else:
        print(out)


