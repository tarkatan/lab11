from sympy import mod_inverse

def is_point_on_curve(x, y, a, b, p):
    return (y ** 2) % p == (x ** 3 + a * x + b) % p

def point_addition(P, Q, a, p):
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 == -y2 % p:
        return (0, 0)

    if P != Q:
        m = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p
    else:
        m = ((3 * x1 ** 2 + a) * mod_inverse(2 * y1, p)) % p

    x3 = (m ** 2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

def scalar_multiplication(k, P, a, p):
    result = (0, 0)
    temp = P

    while k:
        if k % 2 == 1:
            result = point_addition(result, temp, a, p)
        temp = point_addition(temp, temp, a, p)
        k //= 2

    return result

# Parameters
p = 23
a = 1
b = 1
G = (17, 20)

# Check if G is on the curve
assert is_point_on_curve(G[0], G[1], a, b, p), "Base point G is not on the curve!"

# Private and public keys
private_key = 5  # Example private key
public_key = scalar_multiplication(private_key, G, a, p)

print(f"Private key: {private_key}")
print(f"Public key: {public_key}")

# Encryption
plaintext_point = (16, 5)  # Example plaintext point
k = 7  # Random ephemeral key

C1 = scalar_multiplication(k, G, a, p)
C2 = point_addition(plaintext_point, scalar_multiplication(k, public_key, a, p), a, p)

print(f"Ciphertext C1: {C1}")
print(f"Ciphertext C2: {C2}")

# Decryption
shared_secret = scalar_multiplication(private_key, C1, a, p)
decrypted_point = point_addition(C2, (shared_secret[0], -shared_secret[1] % p), a, p)

print(f"Decrypted point: {decrypted_point}")
