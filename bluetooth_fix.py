#!/usr/bin/env python3
import configparser
import argparse

def _parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--reg_path', help='Path to reg file.', default='keys.reg', type=str)

    return parser.parse_args()


def _open_reg_file(file_path):
    """ Open file at given path and return as config option."""
    config = configparser.ConfigParser()
    config.read_file(open(file_path))

    return config


def _insert_mac_colons(mac):
    """ Bluetooth Mac directory file name."""
    mac = mac.upper()
    mac_parts = [mac[i:i + 2] for i in range(0, len(mac), 2)]
    # import pdb; pdb.set_trace()
    return ':'.join(mac_parts)


def _bluetooth_dir_name(section_name):
    """ Return the bluetooth directory name."""
    full_path = section_name.split('\\')
    last_two_macs = full_path[-2:]
    path_parts = []
    for mac in last_two_macs:
        path_parts.append(_insert_mac_colons(mac))

    return '/'.join(path_parts)


def _format_erand(erand):
    """ Reverse erang and return uppercase."""
    erand = erand.replace('hex(b):', '')
    erand_parts = erand.split(',')
    erand_parts.reverse()
    hex_str = ''.join(erand_parts)
    dec = int(hex_str, 16)

    return dec


def _format_ediv(ediv):
    """ Convert ediv to decimal and return."""
    ediv = ediv.replace('dword:', '')
    return int(ediv, 16)



def _format_ltk(ltk):
    """ Convert LTK to uppercase and remove commas."""
    return ltk.lstrip('hex:').upper().replace(',', '')


def _format_irk(irk):
    """ Convert irk to uppercase and remove commas."""
    return irk.replace('hex:', '').replace(',', '').upper()

def _output_section(config, section, irk):
    # print('\n')
    print(f'Replace in /var/lib/bluetooth/{_bluetooth_dir_name(section)}/info:\n')

    print('[IdentityResolvingKey]') # was LocalSignatureKey?
    print('Key={}'.format(_format_irk(irk))) 

    print('\n[LongTermKey]') # was LinkKey?
    print('Key={}'.format(_format_ltk(config[section]['LTK'])))
    print('EncSize=16')
    print('EDiv={}'.format(_format_ediv(config[section]['EDIV'])))
    print('Rand={}'.format(_format_erand(config[section]['ERand'])))


def _process_reg_file(config):
    """ Process the reg file."""
    sections = config.sections()
    for section in sections:
        if 'CentralIRK' in config[section]:
            subsection = [sub for sub in sections if sub.startswith(section + '\\')][0]
            sections.remove(subsection);
            _output_section(config, subsection, config[section]['CentralIRK'])
        else:
            if len(section) < 98:
                continue;
            _output_section(config, section, config[section]['IRK'])

def main():
    """ Main entrypoint to script. """    
    
    args = _parse_args()    
    config = _open_reg_file(args.reg_path)
    _process_reg_file(config)


if __name__ == '__main__':
    main()

