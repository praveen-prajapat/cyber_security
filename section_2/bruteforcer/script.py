from pwn import *

def check_password(password):
    p = process('./bruteforcer')
    p.recvuntil("Enter your password :").decode()
    p.sendline(password)
    response = p.recvall().decode().strip()
    p.close()
    return response

def binary_search(wordlist):
    left = 0
    right = len(wordlist) - 1
    
    while left <= right:
        mid = (left + right) // 2
        password = wordlist[mid].strip()
        print(mid)
        print(f"Trying password: {password}")  
        result = check_password(password)
        print(f"Response: {result}") 
        
        if 'flag' in result:
            return result 
        elif 'too low' in result:
            left = mid + 1
        elif 'too high' in result:
            right = mid - 1
        else:
            raise ValueError(f"Unexpected response from bruteforcer: {result}")

def main():
    with open('sorted_wordlist.txt', 'r') as f:
        wordlist = f.readlines()
    print(len(wordlist))
    flag = binary_search(wordlist)
    print(f"flag{flag}")

if __name__ == '__main__':
    main()
