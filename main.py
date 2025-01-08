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
        # Capture the madde, including the previous line with the title.
        # The text until the next madde will be matched.
        # This introduces edge cases for madde at the end of secions which needs to be handled
        match = re.search(rf"([^\n]+)\nMadde {args.madde}-.*?(?=\n[^\n]+\nMadde \d+-|\Z)", text, re.DOTALL).group()
        title = match.split('\n')[0]
        madde_no = f"Madde {args.madde}"

        # Check if this is the final madde of a section
        # Section headers are all caps
        section_end_check = re.search(r"^[A-ZÇĞİÖŞÜ\s]+$", match, re.MULTILINE)
        if section_end_check:
            match = match[:section_end_check.start()]

        if not args.fikra:
            # Strip the "Madde X- " text if we are not extracting the fikra, to avoid repetition
            match = match[match.find('-')+2:]
    except AttributeError as e:
        print(f"İstenen madde {args.madde}, kanunda bulunamadı.")
        sys.exit(1)

    if args.fikra:
        try:
            match = re.search(rf"\({args.fikra}\) .*?(?=\n\(\d+\) |\Z)", match, re.DOTALL).group()
        except AttributeError as e:
            print(f"İstenen fıkra {args.fikra}, maddede bulunamadı.")
            sys.exit(1)
        if args.bend:
            try:
                match = re.search().group()
            except AttributeError as e:
                print(f"İstenen bend {args.bend}, fıkrada bulunamadı.")
                sys.exit(1)
    print(title, madde_no, match, sep='\n', end='')

if __name__ == "__main__":
    main()
