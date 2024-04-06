import regex, argparse, time


# Microsoft's "Password must meet complexity requirements" categories check
# https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements#reference
def check_password_complexity(password):

    # Categories defined by character type
    uppercase_regex = r'[A-ZΑ-ΩА-Я]'  # Uppercase including Greek, Cyrillic
    lowercase_regex = r'[a-zα-ωа-я]'  # Lowercase including Greek, Cyrillic
    digits_regex = r'\d'  # Digits
    special_chars_regex = r'[-!"#$%&()*,./:;?@\[\]^_`{|}~+<>]'  # Special characters
    other_alphabetic_regex = r'\p{L}&&[^\p{Latin}]'  # Any letter not in the ASCII or Latin-1 Supplement ranges (May require refining as it is quite broad)

    # If categories are met within the password string, award a single point
    categories_met = 0
    if regex.search(uppercase_regex, password):
        categories_met += 1
    if regex.search(lowercase_regex, password):
        categories_met += 1
    if regex.search(digits_regex, password):
        categories_met += 1
    if regex.search(special_chars_regex, password):
        categories_met += 1
    if regex.search(other_alphabetic_regex, password):
        categories_met += 1

    # At least 3 of the categories are required to pass
    return categories_met >= 3

def check_for_displayname(password, display_name):
    # Split the displayName using the defined delimiters and check tokens against the password
    tokens = regex.split(r"[,.\\-_ #\t]", display_name)
    for token in tokens:
        if len(token) >= 3 and token.lower() in password.lower():
            return True
    return False

def check_for_samaccountname(password, sam_account_name):
    # Check the samAccountName in its entirety if it's 3 characters or longer
    if len(sam_account_name) >= 3 and sam_account_name.lower() in password.lower():
        return True
    return False

# Self explanatory
def check_password_min_length(password, min_length):
    return len(password) >= min_length

# Self explanatory
def check_password_max_length(password, max_length):
    return len(password) <= max_length

# Get total lines within original wordlist for statistics
def count_lines(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        return sum(1 for _ in file)

def main():

    parser = argparse.ArgumentParser(description="""
                                     
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓████████▓▒░
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓██████▓▒░   
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░        
 ░▒▓█████████████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓████████▓▒░ 

    A tool to refine big wordlists - because sometimes less is more.""",
    # This was necessary so that the ASCII art doesn't get mangled
    formatter_class=argparse.RawTextHelpFormatter)

    # Main argument definitions
    parser.add_argument('-m', '--minimum-length', default=7, type=int, help='Minimum password length (default: 7)')
    parser.add_argument('-M', '--maximum-length', type=int, help='Maximum password length')
    parser.add_argument('-c', '--complexity-check', action='store_true', help='Enforce Microsoft\'s password complexity requirements')
    parser.add_argument('--sam-account', nargs='+', help='User samAccountName(s) if known')
    parser.add_argument('--display-name', nargs='+', help='Windows display name(s) if known')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='Path to wordlist')
    parser.add_argument('-o', '--output', type=str, help='Path for processed wordlist - prints to stdout by default')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')

    args = parser.parse_args()

    # Make sure max and min length are not clashing
    if args.maximum_length is not None and args.maximum_length < args.minimum_length:
        print('Error: Maximum length >  Minimum length.')
        return

    total_count = count_lines(args.wordlist)  # Total items in original wordlist
    valid_passwords = []  # Valid password candidates array
    processed_count = 0  # Processed passwords counter
    rejected_count = 0  # Rejected passwords counter

    # Stopwatch - start
    start_time = time.time()

    try:
        # Open wordlist and ignore errors when reading, some wordlists don't play nice with UTF-8
        with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as wordlist_file:
            for password in wordlist_file:
                try:
                    password = password.strip()
                    processed_count += 1

                    # Check min / max length first, as it's the simplest computation and most frequent rejecting factor
                    if not check_password_min_length(password, args.minimum_length) or (args.maximum_length is not None and not check_password_max_length(password, args.maximum_length)):
                        rejected_count += 1
                        continue

                    # Check for both samAccountName / displayName in password if any supplied
                    personal_info_flag = False
                    # Check samAccountName if provided
                    if args.sam_account and any(check_for_samaccountname(password, sam_account) for sam_account in args.sam_account):
                        personal_info_flag = True

                    # Check displayName if provided
                    if not personal_info_flag and args.display_name and \
                    any(check_for_displayname(password, display_name) for display_name in args.display_name):
                        personal_info_flag = True

                    # Reject if personal info in password or complexity requirements not met
                    if personal_info_flag or (args.complexity_check and not check_password_complexity(password)):
                        rejected_count += 1
                        continue

                    # If all is good, add the candidate to the viable candidate array
                    valid_passwords.append(password)

                    # Progress bar
                    # Updates every 1000 words checked, best info / performance ratio
                    if processed_count % 1000 == 0 or processed_count == total_count:
                        print(f'\rPasswords processed: {processed_count}/{total_count}', end='')

                # Catch unicode errors
                except UnicodeDecodeError:
                    rejected_count += 1
                    continue

    # Catch wordlist filepath errors
    except FileNotFoundError:
        print(f'\nError: The file {args.wordlist} was not found.')
        return

    # Stopwatch - stop
    elapsed_time = time.time() - start_time  # Calculate elapsed time

    # Display statistics if verbose flag supplied
    if args.verbose:
        print(f'\nTotal Passwords Processed: {processed_count}')
        print(f'Passwords Accepted: {len(valid_passwords)}')
        print(f'Passwords Rejected: {rejected_count}')
        print(f'Processing Time: {elapsed_time:.2f} seconds')

    # Output to file if output flag supplied
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(valid_passwords))
    elif args.verbose:
        print('\n'.join(valid_passwords))

if __name__ == '__main__':
    main()
