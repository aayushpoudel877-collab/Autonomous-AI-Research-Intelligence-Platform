import urllib.request

def main():
    with urllib.request.urlopen('http://localhost:8000/api/v1/health',timeout=3) as r: print(r.read().decode())
if __name__=='__main__': main()
