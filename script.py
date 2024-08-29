from read_write import *

def main():
    os.system('clear')
    split = '=' * 90
    check = [
        'Перевірка usb девайсів',
        'Перевірка з\'єднання по хосту',
        'Перевірка підключений ELRS'
    ]
    func = [
        usb_devices_check,
        connection_to_the_host,
        usb_over_ip_check
    ]
    # print('\n' + split + '\n')
    for check, func in zip(check, func):
        print(check + ':\n')
        func()
        print(split)


main()