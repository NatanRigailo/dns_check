import dns.resolver

# Função para imprimir em vermelho
def print_error(message):
    print(f"\033[91m{message}\033[0m")  # Vermelho

def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def resolve_dns(domain, nameservers, record_type="A"):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = nameservers
    try:
        answers = resolver.resolve(domain, record_type)
        return set(str(answer) for answer in answers)
    except Exception as e:
        print_error(f"Erro ao resolver {domain} usando {nameservers}: {e}")
        return set()

def compare_dns_sets(domains, ns_set1, ns_set2):
    for domain in domains:
        set1_results = resolve_dns(domain, ns_set1)
        set2_results = resolve_dns(domain, ns_set2)

        if set1_results == set2_results:
            print(f"{domain}: Entradas iguais nos dois conjuntos de nameservers")
        else:
            print(f"{domain}: Entradas diferentes entre os conjuntos de nameservers")

# Lendo domínios e nameservers de arquivos
domains_file = "dominios.txt"  # Substitua pelo caminho correto do arquivo
nameservers1_file = "nameservers1.txt"  # Substitua pelo caminho correto do arquivo
nameservers2_file = "nameservers2.txt"  # Substitua pelo caminho correto do arquivo

domains = read_file_to_list(domains_file)
nameservers_set1 = read_file_to_list(nameservers1_file)
nameservers_set2 = read_file_to_list(nameservers2_file)

# Convertendo endereços de nameservers em IPs, se necessário
ns_set1_ips = [dns.resolver.resolve(ns, "A")[0].to_text() for ns in nameservers_set1]
ns_set2_ips = [dns.resolver.resolve(ns, "A")[0].to_text() for ns in nameservers_set2]

compare_dns_sets(domains, ns_set1_ips, ns_set2_ips)
