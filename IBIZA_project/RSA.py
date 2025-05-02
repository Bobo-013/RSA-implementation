import random

#Gyorshatványozás -> alap, hatványkitevő, moduló
def modular_exponentiation(a, k, m):
    result = 1
    a = a % m
    while k > 0:
        if k % 2 == 1:
            result = result * a % m
        k = k // 2
        a = (a * a) % m
    return result

#2 körös Miller-Rabin prímszám vizsgálás
def miller_rabin(n):
    if n < 2 or n % 2 == 0:
        return False
    if n == 2:
        return True

    s = 0
    d = n-1
    a = random.randrange(3, n - 2)
    while d % 2 == 0:
        s += 1
        d //= 2
    x = modular_exponentiation(a, d, n)
    if x == 1:
        return True

    for _ in range(s):
        if x == n - 1:
            return True
        x = (x * x) % n
    return False

#Prím szám generálása, miller_rabin felhasználásával
def generate_prime(bits=1024):
    while True:
        candidate = random.getrandbits(bits)
        candidate |= 1
        if miller_rabin(candidate):
            return candidate

#Kibővített euklideszi algoritmus
#output: leggnagyobb közös osztó, x és y
def extended_euclid(a,b):
    x0,x1,y0,y1,k = 1,0,0,1,1

    while b!=0:
        r = a % b
        q = a // b
        a = b
        b = r

        x = x1
        y = y1
        x1 = x1 * q + x0
        y1 = y1 * q + y0
        x0,y0= x,y
        k = -k

    x = k * x0
    y = -k * y0
    gcd = a
    return(gcd,x,y)

#Kulcs generálás generate_prime felhasználásával, valalmint d kiszámítása extended_euclid segítségével
#output: p, q, n, phi(n), e = 65537, d
def generate_keys(bits=1024):
    p = generate_prime(bits)
    q = generate_prime(bits)

    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537

    gcd,_, _, = extended_euclid(phi_n,e)

    if gcd == 1:
        _, _, d = extended_euclid(phi_n, e)
        if d < 0:
            d += phi_n
    return p, q, n, phi_n, e, d

#Kódolás gyorshatványozással, csak számot tud feldolgozni, publikus kulcsot használva
#output: kódolt üzenet
def encrypt(message, e, n):
    return modular_exponentiation(message, e, n)

#Visszafejtés kínai maradék tételt alkalmazva a titkos kulccsal
#output: eredeti üzenet
def decrypt(cipher, d, p, q):
    y1, y2 = 0, 0
    m = p * q
    m1 = m / p
    m2 = m / q

    d_p = d % (p -1)
    d_q = d % (q -1)

    c1 = modular_exponentiation(cipher, d_p, p)
    c2 = modular_exponentiation(cipher, d_q, q)

    gcd, _, _ = extended_euclid(m1, m2)
    if int(gcd) == 1:
        _, y1, y2 = extended_euclid(m1, m2)

    return ((c1 * y1 * m1) + (c2 * y2 * m2)) % m

#RSA aláírás gyorshatványozással a titkos kulcsot használva
def sign(message, d, n):
    return modular_exponentiation(message, d, n)

#Aláírás érvényesítése publikus kulccsal és gyorshatványozással
def verify(message, signature, e, n):
    is_valid = modular_exponentiation(signature, e, n)
    return is_valid == message


if __name__ == '__main__':
    bits = int(input('Enter the number of bits: '))
    p, q, n, phi_n, e, d= generate_keys(bits)
    #print(p, q, n, phi_n, e, d)
    message = int(input('Enter message: '))
    cipher = encrypt(message, e, n)
    print("cipher = ", cipher)
    print("message = ", decrypt(cipher, d, p, q))

    signature = sign(message, d, n)
    print("signature = ", signature)

    is_valid = verify(message, signature, e, n)
    print(is_valid)






