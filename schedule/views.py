from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import BadRequest
from django.shortcuts import render
from datetime import datetime
import json
from .models import Event

# Отображение календаря
def calendar_view(request):
    return render(request, 'schedule.html')

@csrf_exempt
def events(request):
    if request.method == 'GET':
        start = request.GET.get('start')
        end = request.GET.get('end')

        # Добавляем отладочный вывод
        print("Start:", start)
        print("End:", end)

        try:
            if start:
                start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
            if end:
                end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid date format. Use ISO 8601 format.'}, status=400)

        # Фильтрация событий
        events_query = Event.objects.all()
        if start and end:
            events_query = events_query.filter(start__gte=start_date, end__lte=end_date)

        events_list = [
            {
                'id': event.id,
                'title': event.title,
                'start': event.start.isoformat(),
                'end': event.end.isoformat() if event.end else None,
                'description': event.description,
                'resourceId': event.resourceId,
            } for event in events_query
        ]
        return JsonResponse(events_list, safe=False)

    # Обработка POST-запросов
    elif request.method == 'POST':
        try:
            # Парсим данные запроса
            data = json.loads(request.body)

            # Валидация входных данных
            if not all(key in data for key in ['title', 'start', 'resourceId']):
                return JsonResponse({'error': 'Missing required fields: title, start, resourceId.'}, status=400)

            # Создаем новое событие
            event = Event.objects.create(
                title=data['title'],
                start=datetime.fromisoformat(data['start']),
                end=datetime.fromisoformat(data['end']) if data.get('end') else None,
                description=data.get('description', ''),
                resourceId=data['resourceId']  # Поле модели resourceId
            )

            # Возвращаем успешный ответ
            return JsonResponse({
                'id': event.id,
                'title': event.title,
                'start': event.start.isoformat(),
                'end': event.end.isoformat() if event.end else None,
                'description': event.description,
                'resourceId': event.resourceId,
            }, status=201)

        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use ISO 8601 format.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # Если метод не поддерживается
    return JsonResponse({'error': 'Method not allowed'}, status=405)