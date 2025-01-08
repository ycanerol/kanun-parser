import argparse
import re
import sys

available_texts = ['tck', 'trafik']
texts_directory = 'texts/'

def remove_newlines(text):
    return [t for t in text if t != '\n']


def main():
    parser = argparse.ArgumentParser(description="İlgili kanunlardan istenen madde, fıkra ve bentleri getiren bir komut satırı uygulaması")
    parser.add_argument("kanun", type=str, help="İstenen kanun")
    parser.add_argument("madde", type=int, help="Madde numarası")
    parser.add_argument("-f", "--fikra", type=str, help="Fıkra")
    parser.add_argument("-b", "--bend", type=str, help="Bend")
    args = parser.parse_args()

    if args.kanun not in available_texts:
        print(f"İstenen kanun {args.kanun}, veritabanında yok.")
        sys.exit(1)

    with open(texts_directory + args.kanun + '.txt', 'r') as kanun_file:
        text = kanun_file.readlines()
    text = remove_newlines(text)

    text = ''.join(text)

    try:
        match = re.search(rf"([^\n]+)\nMadde {args.madde}-.*?(?=\n[^\n]+\nMadde \d+-|\Z)", text, re.DOTALL)
        title = match.group().split('\n')[0]
        madde_no = f"Madde {args.madde}"
        # print(text[madde_start:madde_end])
    except AttributeError as e:
        print(f"İstenen madde {args.madde}, kanunda bulunamadı.")
        sys.exit(1)

    if args.fikra:
        try:
            match = re.search(rf"\({args.fikra}\) .*?(?=\n\(\d+\) |\Z)", match, re.DOTALL).group()
        except AttributeError as e:
            print(f"İstenen fıkra {args.fikra}, maddede bulunamadı.")
            sys.exit(1)

if __name__ == "__main__":
    main()
