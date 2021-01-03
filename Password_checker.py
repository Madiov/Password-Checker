import requests
import hashlib


# Requesting Api And checking  the response

def request_api_data(hash_char):
    url = 'https://api.pwnedpasswords.com/range/' + hash_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching :{res.status_code} , check the API and try again.')
    return res


# Examine The Response text and check if any tail in response is identical to our tail and return How many times it leaked

def get_leak_count(response, hash_to_check):
    hash_count = (line.split(':') for line in response.text.splitlines())
    for h, c in hash_count:
        if h == hash_to_check:
            return c
    return 0


# Hashing the password  and seprating it to two part : frist 5 charachters and the rest of hash

def pwned_api_checker(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5)
    return get_leak_count(response, tail)


# For every password in input checks how many time it leaked

def main():
    print('enter the passwords you want to check :')
    args = []
    while True:
        password = input()
        if password == '':
            break
        args.append(password)
        print('you can enter another password but if you are done press enter ')

    for arg in args:
        count = pwned_api_checker(arg)
        if count != 0:
            print(f'{arg} was found {count} times ... you should probably change it!.')
        else:
            print(f'{arg} was NOT found.Nice One !!')


main()
