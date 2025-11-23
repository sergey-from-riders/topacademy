#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Программа для получения курса валют с сайта Центробанка РФ
и пересчета 100 фунтов стерлингов в рубли
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime


def get_currency_rate(currency_code='GBP'):
    """
    Получает курс валюты с сайта Центробанка РФ
    
    Args:
        currency_code: Код валюты (по умолчанию GBP - фунт стерлингов)
    
    Returns:
        tuple: (номинал, курс, название валюты) или None в случае ошибки
    """
    # URL публичного API Центробанка РФ
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    
    try:
        # Делаем запрос к API
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Парсим XML ответ
        root = ET.fromstring(response.content)
        
        # Ищем нужную валюту по коду
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            if char_code == currency_code:
                nominal = int(valute.find('Nominal').text)
                value = float(valute.find('Value').text.replace(',', '.'))
                name = valute.find('Name').text
                return nominal, value, name
        
        return None
        
    except requests.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
    except ET.ParseError as e:
        print(f"Ошибка при парсинге XML: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


def convert_gbp_to_rub(gbp_amount=100):
    """
    Конвертирует фунты стерлингов в рубли по курсу ЦБ РФ
    
    Args:
        gbp_amount: Сумма в фунтах стерлингов (по умолчанию 100)
    
    Returns:
        float: Сумма в рублях или None в случае ошибки
    """
    # Получаем курс фунта стерлингов
    rate_info = get_currency_rate('GBP')
    
    if rate_info is None:
        print("Не удалось получить курс валюты")
        return None
    
    nominal, value, name = rate_info
    
    # Курс в API указан для nominal единиц валюты
    # Например, если nominal=1, то value - это курс за 1 фунт
    # Если nominal=10, то value - это курс за 10 фунтов
    rate_per_unit = value / nominal
    
    # Пересчитываем
    rub_amount = gbp_amount * rate_per_unit
    
    print(f"\nКурс валюты: {name}")
    print(f"Номинал: {nominal}")
    print(f"Курс ЦБ РФ: {value} рублей за {nominal} {name}")
    print(f"Курс за единицу: {rate_per_unit:.4f} рублей")
    print(f"\n{gbp_amount} GBP = {rub_amount:.2f} RUB")
    
    return rub_amount


if __name__ == '__main__':
    print("=" * 50)
    print("Конвертер валют: GBP -> RUB")
    print("Курс с сайта Центробанка РФ")
    print("=" * 50)
    
    # Конвертируем 100 фунтов стерлингов в рубли
    result = convert_gbp_to_rub(100)
    
    if result is not None:
        print("\nКонвертация выполнена успешно!")
    else:
        print("\nОшибка при выполнении конвертации")
