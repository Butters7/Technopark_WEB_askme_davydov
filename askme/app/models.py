QUESTIONS = [
    {
        'id': i,
        'user_name': f'user {i}',
        'answers': i + 100,
        'count_of_likes': i + 200,
        'title': f'Question {i}',
        'text': f'Text {i}',
        'tag': 'python',
    } for i in range(100)
]


ANSWERS = [
    {
        'id': i,
        'useful': i + 1,
        'user_name': f'user {i}',
        'text': f'blablabla {i}',
    } for i in range(8)
]


BEST_MEMBERS = [
    {
        'id': i,
        'user_name': f'user {i}',
    } for i in range(5)
]


TAGS = [
    {'tag_name': 'python', 'id': 0, 'color': 'magenta'},
    {'tag_name': 'technopark', 'id': 1, 'color': 'green'},
    {'tag_name': 'mySQL', 'id': 2, 'color': 'blue'},
    {'tag_name': 'blender', 'id': 3, 'color': 'red'},
]


HOT = [
    {
    'id': i,
    'user_name': f'user {i}',
    'answers': i + 100,
    'count_of_likes': i + 200,
    'title': f'Question {i}',
    'text': f'Text {i}',
    'tag': 'python',
    } for i in range(9, 0, -1)
]
