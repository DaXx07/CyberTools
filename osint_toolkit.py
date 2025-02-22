#!/usr/bin/env python3
import os
import socket
import sys
import re
import datetime
import urllib3
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import nmap
import requests
from tqdm import tqdm

import dns.resolver
from geopy.geocoders import Nominatim
import phonenumbers
from phonenumbers import carrier, geocoder
import shodan
import whois
import json
import asyncio
import aiohttp
import platform
import subprocess
from datetime import datetime
import time

# Initialize colorama with Windows support
init(autoreset=True)
# Set console to UTF-8 mode
os.system('chcp 65001')

class OSINTToolkit:
    def __init__(self):
        pass

    def banner(self):
        banner = """
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝   ██║   ██║   ██║██║   ██║██║     ███████╗
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗   ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝

                                [ Beta v1.0.0 ]

                              Made with <3 By DaXx
"""
        print(Fore.RED + banner + Style.RESET_ALL)
        print(Fore.RED + "[!] CYBERTOOLS ne vous demandera jamais vos informations personnels." + Style.RESET_ALL)
        print("\n")

    def display_menu(self):
        menu = [
            # Premier groupe d'options (outils existants et nouveaux)
            "[1] > Tool Info",
            "[2] > Domain Info",
            "[3] > IP Tools",
            "[4] > Phone Lookup",
            "[5] > Email Lookup",
            "[6] > Username Tracker",
            "[7] > Port Scanner",
            "[8] > Web Analyzer",
            "[9] > Network Tools",
            
            # Deuxième groupe d'options (Discord et nouveaux outils)
            "[10] > Discord Token Info",
            "[11] > Discord Webhook Tools",
            "[12] > Discord Server Info",
            "[13] > Discord Raid Tools",
            "[14] > OSINT Framework",
            "[15] > Dox Generator",
            "[16] > Hash Cracker",
            "[17] > Proxy Tools",
            "[18] > Next Page (1/2)"
        ]
        
        # Create two columns
        col1 = menu[:9]
        col2 = menu[9:]
        
        # Box dimensions
        box_width = 35
        box_spacing = 5
        
        # Draw boxes with red borders
        box_top = "+" + "-" * (box_width - 2) + "+"
        
        # Create the box lines for both columns
        box1_lines = []
        box2_lines = []
        
        # Generate lines for first box
        box1_lines.append(Fore.RED + box_top + Style.RESET_ALL)
        for item in col1:
            box1_lines.append(Fore.RED + "|" + Style.RESET_ALL + f" {item:<{box_width-4}}" + Fore.RED + "|" + Style.RESET_ALL)
        box1_lines.append(Fore.RED + box_top + Style.RESET_ALL)
        
        # Generate lines for second box
        box2_lines.append(Fore.RED + box_top + Style.RESET_ALL)
        for item in col2:
            box2_lines.append(Fore.RED + "|" + Style.RESET_ALL + f" {item:<{box_width-4}}" + Fore.RED + "|" + Style.RESET_ALL)
        box2_lines.append(Fore.RED + box_top + Style.RESET_ALL)
        
        # Print boxes side by side
        for i in range(max(len(box1_lines), len(box2_lines))):
            line1 = box1_lines[i] if i < len(box1_lines) else " " * box_width
            line2 = box2_lines[i] if i < len(box2_lines) else " " * box_width
            print(f"{line1}" + " " * box_spacing + f"{line2}")

        return input("\n" + Fore.RED + ">> " + Style.RESET_ALL)

    def domain_info(self, domain):
        """Récupère les informations sur un nom de domaine"""
        print(Fore.GREEN + "\n[+] Analyse du domaine en cours...")
        try:
            # Whois
            w = whois.whois(domain)
            print(Fore.YELLOW + "\n[*] Informations WHOIS:")
            print(f"Registrar: {w.registrar}")
            print(f"Date de création: {w.creation_date}")
            print(f"Date d'expiration: {w.expiration_date}")
            
            # DNS
            print(Fore.YELLOW + "\n[*] Enregistrements DNS:")
            for qtype in ['A', 'MX', 'NS', 'TXT']:
                try:
                    answers = dns.resolver.resolve(domain, qtype)
                    print(f"\n{qtype} Records:")
                    for rdata in answers:
                        print(f"  {rdata}")
                except:
                    continue
                    
        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors de l'analyse du domaine: {str(e)}")

    def ip_info(self, ip):
        """Récupère les informations sur une adresse IP"""
        print(Fore.GREEN + "\n[+] Analyse de l'IP en cours...")
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            
            if data['status'] == 'success':
                print(Fore.YELLOW + "\n[*] Informations sur l'IP:")
                print(f"Pays: {data['country']}")
                print(f"Région: {data['regionName']}")
                print(f"Ville: {data['city']}")
                print(f"ISP: {data['isp']}")
                print(f"Organisation: {data['org']}")
                print(f"Latitude: {data['lat']}")
                print(f"Longitude: {data['lon']}")
        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors de l'analyse de l'IP: {str(e)}")

    def phone_info(self, phone_number):
        """Analyse un numéro de téléphone"""
        print(Fore.GREEN + "\n[+] Analyse du numéro de téléphone en cours...")
        try:
            number = phonenumbers.parse(phone_number)
            
            print(Fore.YELLOW + "\n[*] Informations sur le numéro:")
            print(f"Pays: {geocoder.description_for_number(number, 'fr')}")
            print(f"Opérateur: {carrier.name_for_number(number, 'fr')}")
            print(f"Valide: {phonenumbers.is_valid_number(number)}")
            print(f"Possible: {phonenumbers.is_possible_number(number)}")
            
        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors de l'analyse du numéro: {str(e)}")

    def port_scan(self, target):
        """Scan des ports avec Nmap"""
        print(Fore.GREEN + "\n[+] Scan des ports en cours...")
        try:
            scanner = nmap.PortScanner()
            scanner.scan(target, '21-443')
            
            for host in scanner.all_hosts():
                print(Fore.YELLOW + f"\n[*] Hôte : {host}")
                for proto in scanner[host].all_protocols():
                    ports = scanner[host][proto].keys()
                    for port in ports:
                        state = scanner[host][proto][port]['state']
                        service = scanner[host][proto][port]['name']
                        print(f"Port {port}/{proto}: {state} ({service})")
                        
        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors du scan des ports: {str(e)}")

    def discord_id_lookup(self, discord_id):
        """Récupère les informations sur un ID Discord"""
        print(Fore.GREEN + "\n[+] Analyse de l'ID Discord en cours...")
        try:
            # Vérifier si l'ID est valide (nombre uniquement)
            if not discord_id.isdigit():
                raise ValueError("L'ID Discord doit contenir uniquement des chiffres")
                
            # Faire la requête à l'API Discord
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(f"https://discord.com/api/v9/users/{discord_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                print(Fore.YELLOW + "\n[*] Informations sur l'utilisateur Discord:")
                print(f"Username: {data.get('username', 'N/A')}")
                print(f"Discriminator: {data.get('discriminator', 'N/A')}")
                print(f"ID: {data.get('id', 'N/A')}")
                print(f"Avatar Hash: {data.get('avatar', 'N/A')}")
                if data.get('banner'):
                    print(f"Banner Hash: {data['banner']}")
                print(f"Creation Date: {self.snowflake_to_date(discord_id)}")
            else:
                print(Fore.RED + "\n[-] Utilisateur non trouvé ou API inaccessible")
                
        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors de l'analyse de l'ID Discord: {str(e)}")

    def email_lookup(self, email):
        """Récupère les informations sur une adresse email"""
        print(Fore.GREEN + "\n[+] Analyse de l'adresse email en cours...")
        try:
            # Vérifier si l'email est valide
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError("Format d'email invalide")

            # Vérifier le format MX du domaine
            domain = email.split('@')[1]
            print(Fore.YELLOW + "\n[*] Informations sur l'email:")
            print(f"Domaine: {domain}")
            
            # Vérifier les enregistrements MX
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                print("\nServeurs MX:")
                for mx in mx_records:
                    print(f"  Priorité: {mx.preference} - Serveur: {mx.exchange}")
            except:
                print("Aucun enregistrement MX trouvé")

            # Vérifier si le domaine a des enregistrements SPF
            try:
                spf_records = dns.resolver.resolve(domain, 'TXT')
                print("\nEnregistrements SPF:")
                for record in spf_records:
                    for string in record.strings:
                        if b'v=spf1' in string:
                            print(f"  {string.decode()}")
            except:
                print("Aucun enregistrement SPF trouvé")

        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors de l'analyse de l'email: {str(e)}")

    def analyze_url(self, url):
        """Analyse une URL pour trouver des informations sur le site web"""
        print(Fore.GREEN + "\n[+] Analyse de l'URL en cours...")
        try:
            # Normaliser l'URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            # Configuration des headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            print(Fore.YELLOW + "\n[*] Informations générales:")
            print(f"Domaine: {parsed_url.netloc}")
            print(f"Protocole: {parsed_url.scheme}")

            # Vérifier le site principal
            try:
                response = requests.get(url, headers=headers, verify=False, timeout=10)
                print(f"Code de statut: {response.status_code}")
                print(f"Server: {response.headers.get('Server', 'Non spécifié')}")
                
                # Analyser les en-têtes de sécurité
                print(Fore.YELLOW + "\n[*] En-têtes de sécurité:")
                security_headers = {
                    'Strict-Transport-Security': 'HSTS',
                    'Content-Security-Policy': 'CSP',
                    'X-Frame-Options': 'X-Frame',
                    'X-XSS-Protection': 'XSS Protection',
                    'X-Content-Type-Options': 'Content Type Options'
                }
                
                for header, name in security_headers.items():
                    value = response.headers.get(header, 'Non présent')
                    print(f"{name}: {value}")

                # Extraire les métadonnées
                soup = BeautifulSoup(response.text, 'html.parser')
                print(Fore.YELLOW + "\n[*] Métadonnées:")
                title = soup.title.string if soup.title else "Non trouvé"
                print(f"Titre: {title}")
                
                meta_description = soup.find('meta', attrs={'name': 'description'})
                if meta_description:
                    print(f"Description: {meta_description.get('content', 'Non trouvé')}")

                # Vérifier robots.txt
                print(Fore.YELLOW + "\n[*] Analyse robots.txt:")
                robots_url = urljoin(base_url, '/robots.txt')
                try:
                    robots_response = requests.get(robots_url, headers=headers, verify=False, timeout=5)
                    if robots_response.status_code == 200:
                        print("robots.txt trouvé:")
                        print(robots_response.text[:500] + "..." if len(robots_response.text) > 500 else robots_response.text)
                    else:
                        print("robots.txt non trouvé")
                except:
                    print("Impossible d'accéder au robots.txt")

                # Vérifier sitemap.xml
                print(Fore.YELLOW + "\n[*] Analyse sitemap:")
                sitemap_urls = [
                    urljoin(base_url, '/sitemap.xml'),
                    urljoin(base_url, '/sitemap_index.xml')
                ]
                
                sitemap_found = False
                for sitemap_url in sitemap_urls:
                    try:
                        sitemap_response = requests.get(sitemap_url, headers=headers, verify=False, timeout=5)
                        if sitemap_response.status_code == 200:
                            print(f"Sitemap trouvé à: {sitemap_url}")
                            sitemap_found = True
                            # Parser le sitemap pour compter les URLs
                            soup = BeautifulSoup(sitemap_response.text, 'xml')
                            urls = soup.find_all('url')
                            if urls:
                                print(f"Nombre d'URLs dans le sitemap: {len(urls)}")
                            break
                    except:
                        continue
                
                if not sitemap_found:
                    print("Aucun sitemap.xml trouvé")

                # Vérifier les technologies (headers basiques)
                print(Fore.YELLOW + "\n[*] Technologies détectées:")
                tech_headers = {
                    'X-Powered-By': 'Backend',
                    'Server': 'Serveur Web',
                    'X-AspNet-Version': 'Version ASP.NET',
                    'X-Generator': 'Générateur',
                }
                
                for header, desc in tech_headers.items():
                    if header in response.headers:
                        print(f"{desc}: {response.headers[header]}")

            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"\n[-] Erreur lors de l'accès au site: {str(e)}")

        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors de l'analyse de l'URL: {str(e)}")

    def ip_pinger(self, target):
        """Ping une adresse IP et affiche les résultats"""
        print(Fore.GREEN + "\n[+] Démarrage du ping vers " + target)
        
        try:
            # Détermine la commande ping selon le système d'exploitation
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '4', target]
            
            print(Fore.YELLOW + "\n[*] Envoi de 4 paquets...")
            
            # Exécute la commande ping
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            # Décode et affiche les résultats
            output = stdout.decode('cp850' if platform.system().lower() == 'windows' else 'utf-8')
            
            # Analyse les résultats
            if process.returncode == 0:
                print(Fore.GREEN + "\n[+] Host joignable!")
                print(Fore.CYAN + "\nRésultats du ping:")
                print(Style.RESET_ALL + output)
            else:
                print(Fore.RED + "\n[-] Host injoignable ou erreur lors du ping")
                if stderr:
                    print(Fore.RED + "\nErreur:" + Style.RESET_ALL)
                    print(stderr.decode('cp850' if platform.system().lower() == 'windows' else 'utf-8'))
                
        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors du ping: {str(e)}")

    def url_pinger(self, url):
        """Vérifie la disponibilité d'une URL et mesure le temps de réponse"""
        print(Fore.GREEN + "\n[+] Test de disponibilité de l'URL...")
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            print(Fore.YELLOW + "\n[*] Envoi de 4 requêtes...")
            
            results = []
            errors = 0
            total_time = 0
            
            for i in range(4):
                try:
                    start_time = datetime.now()
                    response = requests.get(url, timeout=5, verify=False)
                    end_time = datetime.now()
                    
                    response_time = (end_time - start_time).total_seconds() * 1000
                    total_time += response_time
                    results.append(response_time)
                    
                    print(Fore.GREEN + f"[+] Requête {i+1}: {response.status_code} - {response_time:.0f}ms")
                    
                except requests.RequestException as e:
                    errors += 1
                    print(Fore.RED + f"[-] Requête {i+1}: Échec - {str(e)}")
                
                time.sleep(1)  # Attendre 1 seconde entre chaque requête
            
            print(Fore.YELLOW + "\n[*] Résultats:")
            if results:
                print(f"Temps minimum: {min(results):.0f}ms")
                print(f"Temps maximum: {max(results):.0f}ms")
                print(f"Temps moyen: {(total_time / (4-errors)):.0f}ms")
            print(f"Requêtes réussies: {4-errors}/4")
            
        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors du test de l'URL: {str(e)}")

    def webhook_deleter(self):
        """Supprime un webhook Discord"""
        print(Fore.GREEN + "\n[+] Suppression de webhook Discord")
        
        try:
            webhook_url = input(f"{Fore.GREEN}Entrez l'URL du webhook à supprimer: {Style.RESET_ALL}")
            
            print(Fore.YELLOW + "\n[*] Tentative de suppression...")
            
            response = requests.delete(webhook_url)
            
            if response.status_code == 204:
                print(Fore.GREEN + "\n[+] Webhook supprimé avec succès!")
            else:
                print(Fore.RED + f"\n[-] Erreur lors de la suppression: {response.status_code}")
                if response.text:
                    print(f"Détails: {response.text}")
                    
        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors de la suppression du webhook: {str(e)}")

    def snowflake_to_date(self, discord_id):
        """Convertit un Discord Snowflake ID en date de création"""
        try:
            timestamp = ((int(discord_id) >> 22) + 1420070400000) / 1000
            return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return "Date inconnue"

    def webhook_spammer(self):
        """Spam un webhook Discord avec des messages personnalisés"""
        print(Fore.GREEN + "\n[+] Configuration du Webhook Spammer")
        try:
            webhook_url = input("Entrez l'URL du webhook Discord: ")
            message = input("Message à envoyer: ")
            username = input("Nom d'utilisateur à utiliser (laissez vide pour défaut): ") or "OSINT Toolkit"
            avatar_url = input("URL de l'avatar (laissez vide pour défaut): ") or "https://i.imgur.com/AfFp7pu.png"
            try:
                count = int(input("Nombre de messages à envoyer: "))
            except ValueError:
                print(Fore.RED + "Nombre invalide, utilisation de 1 par défaut")
                count = 1
            
            try:
                delay = float(input("Délai entre les messages (en secondes): "))
            except ValueError:
                print(Fore.RED + "Délai invalide, utilisation de 1 seconde par défaut")
                delay = 1

            print(Fore.YELLOW + "\n[*] Démarrage du spam...")

            async def send_webhook():
                async with aiohttp.ClientSession() as session:
                    webhook = {
                        "content": message,
                        "username": username,
                        "avatar_url": avatar_url
                    }

                    success_count = 0
                    error_count = 0

                    for i in range(count):
                        try:
                            async with session.post(webhook_url, json=webhook) as response:
                                if response.status == 204:
                                    success_count += 1
                                    print(Fore.GREEN + f"[+] Message {i+1}/{count} envoyé avec succès")
                                else:
                                    error_count += 1
                                    print(Fore.RED + f"[-] Erreur lors de l'envoi du message {i+1}: {response.status}")
                                
                                if i < count - 1:  # Ne pas attendre après le dernier message
                                    await asyncio.sleep(delay)

                        except Exception as e:
                            error_count += 1
                            print(Fore.RED + f"[-] Erreur lors de l'envoi du message {i+1}: {str(e)}")
                            if i < count - 1:
                                await asyncio.sleep(delay)

                    print(Fore.YELLOW + f"\n[*] Résumé:")
                    print(f"Messages envoyés avec succès: {success_count}")
                    print(f"Erreurs: {error_count}")

            # Exécuter la fonction asynchrone
            asyncio.run(send_webhook())

        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur lors du spam webhook: {str(e)}")

    def clear_screen(self):
        """Nettoie l'écran"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu(self):
        while True:
            self.clear_screen()
            self.banner()
            choice = self.display_menu()

            if choice == "1":
                print("\nTool Information:")
                print("CYBERTOOLS - A comprehensive OSINT and security toolkit")
                print("Version: 1.0")
                print("Author: Alex")
                input("\nPress Enter to continue...")
            
            elif choice == "2":
                domain = input("\nEnter domain name: ")
                self.domain_info(domain)
                input("\nPress Enter to continue...")
            
            elif choice == "3":
                ip = input("\nEnter IP address: ")
                self.ip_info(ip)
                input("\nPress Enter to continue...")
            
            elif choice == "4":
                phone = input("\nEnter phone number (with country code): ")
                self.phone_info(phone)
                input("\nPress Enter to continue...")
            
            elif choice == "5":
                email = input("\nEnter email address: ")
                self.email_lookup(email)
                input("\nPress Enter to continue...")
            
            elif choice == "6":
                username = input("\nEnter username: ")
                self.username_tracker(username)
                input("\nPress Enter to continue...")
            
            elif choice == "7":
                target = input("\nEnter target IP or domain: ")
                self.port_scan(target)
                input("\nPress Enter to continue...")
            
            elif choice == "8":
                url = input("\nEnter URL to analyze: ")
                self.analyze_url(url)
                input("\nPress Enter to continue...")
            
            elif choice == "9":
                self.network_tools()
                input("\nPress Enter to continue...")
            
            elif choice == "10":
                token = input("\nEnter Discord token: ")
                self.discord_id_lookup(token)
                input("\nPress Enter to continue...")
            
            elif choice == "11":
                print("\n1. Webhook Spammer")
                print("2. Webhook Deleter")
                webhook_choice = input("Choose an option (1-2): ")
                if webhook_choice == "1":
                    self.webhook_spammer()
                elif webhook_choice == "2":
                    self.webhook_deleter()
                input("\nPress Enter to continue...")
            
            elif choice == "12":
                print("\nDiscord Server Info:")
                print("Not implemented yet")
                input("\nPress Enter to continue...")
            
            elif choice == "13":
                self.discord_raid_tools()
                input("\nPress Enter to continue...")
            
            elif choice == "14":
                print("\nOpening OSINT Framework website...")
                os.system("start https://osintframework.com")
                input("\nPress Enter to continue...")
            
            elif choice == "15":
                self.dox_generator()
                input("\nPress Enter to continue...")
            
            elif choice == "16":
                self.hash_cracker()
                input("\nPress Enter to continue...")
            
            elif choice == "17":
                self.proxy_tools()
                input("\nPress Enter to continue...")
            
            elif choice == "18":
                print("\nThank you for using CYBERTOOLS!")
                sys.exit(0)
            
            else:
                print("\nInvalid option! Please try again.")
                input("\nPress Enter to continue...")

    def username_tracker(self, username):
        """Track a username across multiple platforms"""
        print(Fore.YELLOW + "\n[*] Recherche du nom d'utilisateur sur différentes plateformes..." + Style.RESET_ALL)
        
        platforms = {
            "GitHub": f"https://github.com/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "Facebook": f"https://facebook.com/{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "LinkedIn": f"https://linkedin.com/in/{username}"
        }
        
        for platform, url in platforms.items():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(Fore.GREEN + f"[+] {platform}: Compte trouvé - {url}")
                else:
                    print(Fore.RED + f"[-] {platform}: Compte non trouvé")
            except:
                print(Fore.RED + f"[-] {platform}: Erreur lors de la vérification")

    def network_tools(self):
        """Network analysis tools"""
        while True:
            print(Fore.YELLOW + "\nNetwork Tools:")
            print("1. IP Pinger")
            print("2. URL Pinger")
            print("3. Traceroute")
            print("4. DNS Lookup")
            print("5. Retour" + Style.RESET_ALL)
            
            choice = input("\nChoisissez une option (1-5): ")
            
            if choice == "1":
                target = input("Entrez l'IP à pinger: ")
                self.ip_pinger(target)
            elif choice == "2":
                url = input("Entrez l'URL à pinger: ")
                self.url_pinger(url)
            elif choice == "3":
                target = input("Entrez l'adresse cible: ")
                os.system(f"tracert {target}")
            elif choice == "4":
                domain = input("Entrez le domaine: ")
                try:
                    answers = dns.resolver.resolve(domain, 'A')
                    for rdata in answers:
                        print(Fore.GREEN + f"[+] IP Address: {rdata.address}")
                except Exception as e:
                    print(Fore.RED + f"[-] Erreur: {str(e)}")
            elif choice == "5":
                break

    def discord_raid_tools(self):
        """Discord raid tools"""
        while True:
            print(Fore.YELLOW + "\nDiscord Raid Tools:")
            print("1. Mass DM")
            print("2. Server Joiner")
            print("3. Channel Flooder")
            print("4. Role Mass Mention")
            print("5. Retour" + Style.RESET_ALL)
            
            choice = input("\nChoisissez une option (1-5): ")
            
            if choice == "5":
                break
            else:
                print(Fore.RED + "\n[-] Cette fonctionnalité n'est pas encore implémentée")
                input("Appuyez sur Entrée pour continuer...")

    def dox_generator(self):
        """Generate a dox report"""
        print(Fore.YELLOW + "\n[*] Dox Generator")
        target = input("Entrez le nom de la cible: ")
        
        print("\nCollecte d'informations en cours...")
        report = f"""
=== RAPPORT DOX ===
Cible: {target}
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==================
"""
        print(Fore.GREEN + "\n[+] Rapport généré avec succès")
        print(report)

    def hash_cracker(self):
        """Hash cracking tool"""
        print(Fore.YELLOW + "\n[*] Hash Cracker")
        hash_type = input("Type de hash (md5/sha1/sha256): ")
        hash_value = input("Hash à cracker: ")
        
        print(Fore.RED + "\n[-] Cette fonctionnalité n'est pas encore complètement implémentée")
        print("Utilisez des outils comme hashcat ou john the ripper pour le moment.")

    def proxy_tools(self):
        """Proxy management tools"""
        while True:
            print(Fore.YELLOW + "\nProxy Tools:")
            print("1. Vérifier une liste de proxies")
            print("2. Scraper des proxies")
            print("3. Tester la vitesse des proxies")
            print("4. Retour" + Style.RESET_ALL)
            
            choice = input("\nChoisissez une option (1-4): ")
            
            if choice == "4":
                break
            else:
                print(Fore.RED + "\n[-] Cette fonctionnalité n'est pas encore implémentée")
                input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        toolkit = OSINTToolkit()
        toolkit.menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nProgramme interrompu par l'utilisateur.")
        sys.exit(0)
