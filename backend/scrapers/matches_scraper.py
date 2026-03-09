import requests
import json
from datetime import datetime
from typing import List, Dict

class MatchesScraper:
    def __init__(self):
        pass
    
    def fetch_matches(self) -> List[Dict]:
        """Сбор предстоящих матчей"""
        matches = []
        
        # Футбольные матчи
        matches.extend([
            {
                'sport': 'football',
                'league': 'АПЛ',
                'team1': 'Ливерпуль',
                'team2': 'Манчестер Сити',
                'time': '19:45',
                'date': 'Сегодня'
            },
            {
                'sport': 'football',
                'league': 'Ла Лига',
                'team1': 'Реал Мадрид',
                'team2': 'Барселона',
                'time': '22:00',
                'date': 'Сегодня'
            },
            {
                'sport': 'football',
                'league': 'Серия А',
                'team1': 'Интер',
                'team2': 'Ювентус',
                'time': '21:45',
                'date': 'Сегодня'
            }
        ])
        
        # Хоккейные матчи
        matches.extend([
            {
                'sport': 'hockey',
                'league': 'НХЛ',
                'team1': 'Вашингтон',
                'team2': 'Питтсбург',
                'time': '02:00',
                'date': 'Сегодня'
            },
            {
                'sport': 'hockey',
                'league': 'КХЛ',
                'team1': 'Ак Барс',
                'team2': 'Салават Юлаев',
                'time': '17:00',
                'date': 'Сегодня'
            }
        ])
        
        # CS:GO матчи
        matches.extend([
            {
                'sport': 'csgo',
                'league': 'IEM Katowice',
                'team1': 'Team Spirit',
                'team2': 'FaZe Clan',
                'time': '14:30',
                'date': 'Сегодня'
            },
            {
                'sport': 'csgo',
                'league': 'ESL Pro League',
                'team1': 'NAVI',
                'team2': 'Vitality',
                'time': '16:00',
                'date': 'Сегодня'
            }
        ])
        
        return matches

if __name__ == "__main__":
    scraper = MatchesScraper()
    matches = scraper.fetch_matches()
    
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    
    print(f"Собрано матчей: {len(matches)}")