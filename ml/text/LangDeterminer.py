from enum import Enum

russian_alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                    'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

english_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']

ukrainian_alphabet = ['а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з', 'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о',
                      'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ю', 'я']

armenian_alphabet = ['ա', 'բ', 'գ', 'դ', 'ե', 'զ', 'է', 'ը', 'թ', 'ժ', 'ի', 'լ', 'խ', 'ծ', 'կ', 'հ', 'ձ', 'ղ', 'ճ',
                     'մ', 'յ', 'ն', 'շ', 'ո', 'չ', 'պ', 'ջ', 'ռ', 'ս', 'վ', 'տ', 'ր', 'ց', 'ւ', 'փ', 'ք', 'օ', 'ֆ']

azerbaijan_alphabet = ['a', 'b', 'c', 'ç', 'd', 'e', 'ə', 'f', 'g', 'ğ', 'h', 'x', 'i', 'İ', 'j', 'k', 'q', 'l', 'm',
                       'n', 'o', 'ö', 'p', 'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z']

georgian_alphabet = ['ა', 'ბ', 'გ', 'დ', 'ე', 'ვ', 'ზ', 'თ', 'ი', 'კ', 'ლ', 'მ', 'ნ', 'ო', 'პ', 'ჟ', 'რ', 'ს', 'ტ',
                     'უ', 'ფ', 'ქ', 'ღ', 'ყ', 'შ', 'ჩ', 'ც', 'ძ', 'წ', 'ჭ', 'ხ', 'ჯ', 'ჰ']


class Lang(Enum):
    russian = 1
    english = 2
    ukrainian = 3
    armenian = 4
    azerbaijan = 5
    georgian = 6


def determine_language(text):
    russian = sum([text.count(letter) for letter in russian_alphabet])
    english = sum([text.count(letter) for letter in english_alphabet])
    ukrainian = sum([text.count(letter) for letter in ukrainian_alphabet])
    armenian = sum([text.count(letter) for letter in armenian_alphabet])
    azerbaijan = sum([text.count(letter) for letter in azerbaijan_alphabet])
    georgian = sum([text.count(letter) for letter in georgian_alphabet])
    max_counter = max(russian, english, ukrainian, armenian, azerbaijan, georgian)

    if russian == max_counter:
        return Lang.russian
    if english == max_counter:
        return Lang.english
    if ukrainian == max_counter:
        return Lang.ukrainian
    if armenian == max_counter:
        return Lang.armenian
    if azerbaijan == max_counter:
        return Lang.azerbaijan
    return Lang.georgian


if __name__ == "__main__":
    print(determine_language("фвыадлотдфлывоа"))
    print(determine_language("asdkfnlkjasdf"))
    print(determine_language("Міністр закордонних справ України Вадим Пристайк".lower()))
    print(determine_language("ռեպրեսիաները շարունակվում են".lower()))
    print(determine_language(
        "Rusiya Federasiyasının Prezidenti Vladimir Putin Azərbaycan Respublikasının Prezidenti İlham".lower()))
    print(determine_language("საქართველოს, აზერბაიჯანისა და თურქეთის".lower()))
