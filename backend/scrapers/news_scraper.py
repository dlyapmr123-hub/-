import requests
import json
import os
from datetime import datetime
from typing import List, Dict
import time

class NewsScraper:
    def __init__(self):
        self.sources = {
            'football': [
                'https://api.football-data.org/v4/matches',
                'https://www.thesportsdb.com/api/v1/json/3/eventsseason.php'
            ],
            'hockey': [
                'https://api-web.nhle.com/v1/schedule/now'
            ],
            'csgo': [
                'https://api.hltv.org/v1/matches'
            ]
        }
        
    def fetch_news(self) -> List[Dict]:
        """Сбор новостей со всех источников"""
        all_news = []
        
        # Футбольные новости
        try:
            # Здесь реальные API запросы
            # Для демо возвращаем тестовые данные
            football_news = [
                {
                    'title': 'Мбаппе пропустит матч с «Реалом» из-за травмы',
                    'source': 'L\'Equipe',
                    'time': '15 мин назад',
                    'icon': '⚽',
                    'sport': 'football',
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'title': '«Ливерпуль» предложил Салаху новый контракт',
                    'source': 'The Athletic',
                    'time': '3 часа назад',
                    'icon': '⚽',
                    'sport': 'football',
                    'timestamp': datetime.now().isoformat()
                }
            ]
            all_news.extend(football_news)
        except Exception as e:
            print(f"Ошибка получения футбольных новостей: {e}")
        
        # Хоккейные новости
        try:
            hockey_news = [
                {
                    'title': 'Овечкин вышел на третье место в истории НХЛ',
                    'source': 'NHL.com',
                    'time': '45 мин назад',
                    'icon': '🏒',
                    'sport': 'hockey',
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'title': 'ЦСКА обыграл СКА в дерби',
                    'source': 'Чемпионат',
                    'time': '5 часов назад',
                    'icon': '🏒',
                    'sport': 'hockey',
                    'timestamp': datetime.now().isoformat()
                }
            ]
            all_news.extend(hockey_news)
        except Exception as e:
            print(f"Ошибка получения хоккейных новостей: {e}")
        
        # CS:GO новости
        try:
            csgo_news = [
                {
                    'title': 'Team Spirit вышла в плей-офф IEM Katowice',
                    'source': 'HLTV',
                    'time': '2 часа назад',
                    'icon': '🎮',
                    'sport': 'csgo',
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'title': 'NAVI анонсировали изменения в составе',
                    'source': 'Cybersport',
                    'time': '6 часов назад',
                    'icon': '🎮',
                    'sport': 'csgo',
                    'timestamp': datetime.now().isoformat()
                }
            ]
            all_news.extend(csgo_news)
        except Exception as e:
            print(f"Ошибка получения CS:GO новостей: {e}")
        
        return all_news

if __name__ == "__main__":
    scraper = NewsScraper()
    news = scraper.fetch_news()
    
    # Сохраняем в файл
    with open('news_output.json', 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    
    print(f"Собрано новостей: {len(news)}")