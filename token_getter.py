import logging
import sys
import getopt
import requests

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def get_access_token_str(api_key, secret_key):
    token_request_url = 'https://aip.baidubce.com/oauth/2.0/token'
    token_request_params = dict(grant_type='client_credentials', client_id=api_key, client_secret=secret_key)
    return requests.get(url=token_request_url, params=token_request_params).text


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "ha:s:", ["api_key=", "secret_key="])
    except getopt.GetoptError:
        print('Error: token_getter.py -a <API Key> -s <Secret Key> [token_file_name]')
        print('   or: token_getter.py --api_key=<API Key> --secret_key=<Secret Key> [token_file_name]')
        sys.exit(2)

    filename, api_key, secret_key = '', '', ''

    if len(args) == 0:
        filename = 'env/access_token.json'
    elif len(args) == 1:
        filename = args[0]
    else:
        print('Error: token_getter.py -a <API Key> -s <Secret Key> [token_file_name]')
        print('   or: token_getter.py --api_key=<API Key> --secret_key=<Secret Key> [token_file_name]')
        sys.exit(2)

    op_keys = list(map(lambda o: o[0], opts))
    if '-a' in op_keys and '-s' not in op_keys:
        print('请输入正确的Secret Key')
        sys.exit(1)
    elif '-a' not in op_keys and '-s' in op_keys:
        print('请输入正确的API Key')
        sys.exit(1)

    for opt in opts:
        if opt[0] == '-h':
            print('token_getter.py -a <API Key> -s <Secret Key> [token_file_name]')
            print('token_getter.py --api_key=<API Key> --secret_key=<Secret Key> [token_file_name]')
            sys.exit()
        if opt[0] in ('-a', '--api_key'):
            api_key = opt[1]
        elif opt[0] in ('-s', '--secret_key'):
            secret_key = opt[1]

    json_line = get_access_token_str(api_key=api_key, secret_key=secret_key)
    with open(filename, 'w', encoding='utf-8') as w:
        w.write(json_line)
    print('access_token文件已写入{0}'.format(filename))


if __name__ == "__main__":
    main(sys.argv[1:])
