import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
import sys
import argparse
from datetime import datetime

def upload_to_firebase(data_type, file_path):
    """Загрузка данных в Firestore"""
    
    # Получаем сервисный аккаунт из переменной окружения
    service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT', '{}'))
    
    if not service_account_info:
        print("❌ Ошибка: FIREBASE_SERVICE_ACCOUNT не найден")
        print("Добавьте секрет в GitHub: https://github.com/ваш-проект/settings/secrets/actions")
        sys.exit(1)
    
    # Инициализация Firebase
    try:
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase инициализирован")
    except Exception as e:
        print(f"❌ Ошибка инициализации Firebase: {e}")
        sys.exit(1)
    
    # Читаем данные
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"📄 Загружено {len(data)} записей из {file_path}")
    except Exception as e:
        print(f"❌ Ошибка чтения файла {file_path}: {e}")
        sys.exit(1)
    
    if data_type == 'news':
        # Очищаем старые новости (старше 1 дня)
        news_ref = db.collection('news')
        old_news = news_ref.stream()
        deleted = 0
        for doc in old_news:
            doc.reference.delete()
            deleted += 1
        print(f"🗑️ Удалено {deleted} старых новостей")
        
        # Загружаем новые
        for item in data:
            # Добавляем timestamp для сортировки
            if 'timestamp' not in item:
                item['timestamp'] = datetime.now().isoformat()
            news_ref.add(item)
        print(f"✅ Загружено {len(data)} новостей")
        
    elif data_type == 'predictions':
        # Очищаем старые прогнозы
        pred_ref = db.collection('predictions')
        old_pred = pred_ref.stream()
        deleted = 0
        for doc in old_pred:
            doc.reference.delete()
            deleted += 1
        print(f"🗑️ Удалено {deleted} старых прогнозов")
        
        # Загружаем новые
        iron_count = 0
        for item in data:
            # Добавляем isIron для удобства
            item['isIron'] = item.get('probability', 0) > 85
            if item['isIron']:
                iron_count += 1
            pred_ref.add(item)
        print(f"✅ Загружено {len(data)} прогнозов (из них {iron_count} железных)")
        
        # Обновляем статистику
        stats_ref = db.collection('statistics').document('overall')
        stats = stats_ref.get()
        
        # Получаем текущие выигрыши из истории
        history_ref = db.collection('history').stream()
        won = 0
        lost = 0
        for doc in history_ref:
            h = doc.to_dict()
            if h.get('result') == 'win':
                won += 1
            elif h.get('result') == 'loss':
                lost += 1
        
        if stats.exists:
            current_stats = stats.to_dict()
            current_stats['total'] = len(data)
            current_stats['won'] = won
            current_stats['lost'] = lost
            current_stats['accuracy'] = round((won / max(1, len(data))) * 100) if len(data) > 0 else 0
            current_stats['profit'] = current_stats['accuracy'] - 50
            current_stats['analyzedMatches'] = current_stats.get('analyzedMatches', 0) + len(data)
            current_stats['ironToday'] = iron_count
            current_stats['lastUpdate'] = datetime.now().isoformat()
            
            stats_ref.set(current_stats)
            print(f"📊 Статистика обновлена: точность {current_stats['accuracy']}%, профит {current_stats['profit']}%")
        else:
            stats_ref.set({
                'total': len(data),
                'won': won,
                'lost': lost,
                'accuracy': 0,
                'profit': -50,
                'analyzedMatches': len(data),
                'ironToday': iron_count,
                'lastUpdate': datetime.now().isoformat()
            })
            print("📊 Статистика создана")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', required=True, choices=['news', 'predictions'])
    parser.add_argument('--file', required=True)
    
    args = parser.parse_args()
    upload_to_firebase(args.type, args.file)