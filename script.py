from random import choice
from datacenter.models import Schoolkid, Lesson
from datacenter.models import Mark, Chastisement, Commendation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

praise_text = (
    'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!',
    'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!',
    'Очень хороший ответ!', 'Талантливо!', 'Ты сегодня прыгнул выше головы!',
    'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!',
    'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
    'Это как раз то, что нужно!', 'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!',
    'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!'
)


def get_schoolkid_from_name(name):
    try:
        student = Schoolkid.objects.get(full_name=name)
        return student
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(
            f'ФИО {name} нет в базе.Необходимо ввести полностью ФИО'
        )
    except MultipleObjectsReturned:
        raise MultipleObjectsReturned(
            'Найдено несколько полозователей'
        )


def fix_marks(name):
    student = get_schoolkid_from_name(name)
    Mark.objects.filter(schoolkid=student, points__in=[2, 3]).update(points=5)


def remove_chastisements(name):
    student = get_schoolkid_from_name(name)
    comments = Chastisement.objects.filter(schoolkid=student)
    comments.delete()


def create_commendation(name, subject, praise_text):
    schoolkid = get_schoolkid_from_name(name)
    lesson = Lesson.objects.filter(
        subject__title=subject, year_of_study='6',
        group_letter='А'
    ).order_by('?').first()
    if lesson:
        if not Commendation.objects.filter(
            created=lesson.date, schoolkid=schoolkid
        ):
            Commendation.objects.create(
                text=choice(praise_text),
                created=lesson.date,
                schoolkid=schoolkid,
                teacher=lesson.teacher,
                subject=lesson.subject
            )

    else:
        raise IndexError(
            f'Предмет {subject} В базе не найден. '
            f'Проверьте правильность написания'
        )
